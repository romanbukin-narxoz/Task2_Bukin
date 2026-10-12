"""Reproducible spam-classification measurement; sample mode is not research evidence."""
import os
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[key] = '1'
import argparse
import csv
import hashlib
import json
import platform
import time
from collections import Counter
from importlib.metadata import version
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

ROOT = Path(__file__).resolve().parents[1]

def run(config_path):
    config = json.loads(config_path.read_text(encoding='utf-8'))
    tfidf_params = dict(config['tfidf'])
    tfidf_params['ngram_range'] = tuple(tfidf_params['ngram_range'])
    data_path = ROOT / config['data_path']
    with data_path.open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    if not rows or not {'id', 'text', 'label'} <= rows[0].keys():
        raise ValueError('CSV must contain id,text,label columns and nonempty data.')
    ids, seen = set(), {}
    for row in rows:
        text = ' '.join(row['text'].lower().split())
        if not text or not row['id'] or row['id'] in ids or row['label'] not in ('ham', 'spam'):
            raise ValueError('Use unique nonempty IDs, nonempty text, and ham/spam labels.')
        if text in seen:
            raise ValueError('Duplicate normalized text found; deduplicate before splitting.')
        ids.add(row['id'])
        seen[text] = row['label']
    texts = np.array([r['text'] for r in rows])
    labels = np.array([int(r['label'] == 'spam') for r in rows])
    if min(Counter(labels).values()) < 2 or len(set(labels)) != 2:
        raise ValueError('At least two examples of each class are required.')
    train, test = train_test_split(np.arange(len(rows)), test_size=config['test_size'],
                                  stratify=labels, random_state=config['split_seed'])
    results, predictions = [], []
    for seed in config['seeds']:
        rng = np.random.default_rng(seed)
        groups = [rng.permutation(train[labels[train] == c]) for c in (0, 1)]
        for fraction in config['train_fractions']:
            if not 0 < fraction <= 1:
                raise ValueError('Training fractions must be in (0,1].')
            selected = np.concatenate([g[:max(1, int(len(g) * fraction))] for g in groups])
            models = {
                'naive_bayes': MultinomialNB(**config['models']['naive_bayes']),
                'logistic_regression': LogisticRegression(random_state=seed, **config['models']['logistic_regression']),
                'random_forest': RandomForestClassifier(random_state=seed, n_jobs=1, **config['models']['random_forest'])}
            for name, estimator in models.items():
                pipeline = make_pipeline(TfidfVectorizer(**tfidf_params), estimator)
                start = time.perf_counter()
                pipeline.fit(texts[selected], labels[selected])
                fit_ms = (time.perf_counter() - start) * 1000
                start = time.perf_counter()
                predicted = pipeline.predict(texts[test])
                predict_ms = (time.perf_counter() - start) * 1000 / len(test)
                tn, fp, fn, tp = confusion_matrix(labels[test], predicted, labels=[0, 1]).ravel()
                fpr = float(fp / (fp + tn))
                result = dict(mode=config['mode'], model=name, seed=seed, train_fraction=fraction,
                              n_train=len(selected), n_test=len(test), accuracy=accuracy_score(labels[test], predicted),
                              precision=precision_score(labels[test], predicted, zero_division=0),
                              recall=recall_score(labels[test], predicted, zero_division=0),
                              f1=f1_score(labels[test], predicted, zero_division=0), false_positive_rate=fpr,
                              tn=int(tn), fp=int(fp), fn=int(fn), tp=int(tp), fit_ms=fit_ms,
                              predict_ms_per_email=predict_ms,
                              fpr_guardrail_pass=fpr <= config['max_fpr'])
                results.append(result)
                for idx, pred in zip(test, predicted):
                    predictions.append(dict(model=name, seed=seed, train_fraction=fraction,
                                            id=rows[idx]['id'], true_label=int(labels[idx]), predicted_label=int(pred)))
    output = ROOT / config['output_dir']
    output.mkdir(parents=True, exist_ok=True)
    for filename, records in [('metrics.csv', results), ('predictions.csv', predictions)]:
        with (output / filename).open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)
    manifest = dict(config=config, python=platform.python_version(), platform=platform.platform(),
                    processor=platform.processor(), data_sha256=hashlib.sha256(data_path.read_bytes()).hexdigest(),
                    versions={name: version(name) for name in ('numpy', 'scipy', 'scikit-learn', 'joblib', 'threadpoolctl')},
                    train_ids=[rows[i]['id'] for i in train], test_ids=[rows[i]['id'] for i in test])
    (output / 'run_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(f"OK: {len(results)} benchmark rows saved to {output}")
    if config['mode'] == 'smoke':
        print('SYNTHETIC SAMPLE ONLY: these scores cannot support research conclusions.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=Path, default=ROOT / 'config.json')
    args = parser.parse_args()
    run(args.config.resolve())

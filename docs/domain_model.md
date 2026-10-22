# Mathematical model of spam detection

The pipeline classifies an email as ham (0) or spam (1). Naive Bayes is the baseline; Logistic Regression and Random Forest are the alternatives. These definitions apply to the actual implementation in src/benchmark.py.

## Variables and data flow

For email text $t_i$, the target is $y_i\in\{0,1\}$. TF-IDF fitted on training emails alone produces $x_i\in\mathbb{R}^d$, with $d\leq5000$. A stratified fixed holdout is shared by all models. Training subsets are nested within each seed and paired across models. Test data never fit the vocabulary or model.

The sample uses a 60/40 split (6 train and 4 test emails); the research configuration uses 80/20. Fractions 25%, 50%, 100% of each training class are rounded down with a minimum of one example, so the sample has actual training sizes 2, 2, 6. The first two fractions are identical within a seed and are not separate effective sample sizes.

## Logistic Regression loss

$$p_i=\sigma(w^T x_i+b),\quad \sigma(z)=\frac{1}{1+e^{-z}}.$$

For the configured L2 liblinear estimator, using the augmented weight vector $\tilde w$ that includes the regularized synthetic intercept feature:

$$J(\tilde w)=\frac12\|\tilde w\|_2^2+C\sum_{i=1}^{n}[-y_i\log p_i-(1-y_i)\log(1-p_i)],\quad C=1.$$

This is a training objective; F1 below is an evaluation metric, not the optimized loss.

## Multinomial Naive Bayes baseline

$$\hat y=\arg\max_{c\in\{0,1\}}\left[\log P(c)+\sum_{j=1}^{d}x_j\log\theta_{cj}\right].$$

$$\theta_{cj}=\frac{\sum_{i:y_i=c}x_{ij}+\alpha}{\sum_{k=1}^{d}\sum_{i:y_i=c}x_{ik}+\alpha d},\quad\alpha=1.$$

The model uses nonnegative TF-IDF features as weighted counts.

## Random Forest

One hundred trees use bootstrap samples and Gini impurity $G=1-\sum_c p_c^2$ for splitting. Predicted class probabilities are averaged across trees and the most probable class is selected. This model does not optimize the Logistic Regression loss.

## Evaluation metrics and guardrail

$$F_1=\frac{2TP}{2TP+FP+FN},\qquad FPR=\frac{FP}{FP+TN}\leq0.05.$$

$$ErrorRate=\frac{FP+FN}{TP+TN+FP+FN}.$$

TP and FN refer to spam; TN and FP refer to ham. Undefined precision or F1 uses zero, matching the benchmark. Each stratified holdout contains both classes, so the FPR denominator is nonzero. Fit time includes TF-IDF training and classifier training. Prediction time includes TF-IDF transformation and classifier prediction, divided by test-email count (ms/email). It is a batch average, not the p95 of individual request latency.

## Uncertainty and interpretation

For each model and training fraction, calculate mean, sample SD, median and p95 across five seed runs. Resample these five values with replacement 5000 times using seed 42, calculate the mean each time, and take the 2.5th and 97.5th percentiles. The result is a descriptive seed-bootstrap interval conditional on the same holdout. It does not estimate uncertainty over new emails. Reusing one test set makes seed runs dependent for generalization claims. In the sample, only two ham test emails make FPR extremely coarse (0, 0.5, 1); even FPR zero cannot validate a 5% population limit. At full training size NB/LR may be identical across seeds; a zero-width CI is not certainty of generalization. Timing intervals summarize these executions, not different machines or sustained-load behavior.

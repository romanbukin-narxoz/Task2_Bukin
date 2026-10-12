# Research dataset registration
Status: pending selection before Week 7. No real research dataset is included.

Fill in before running the main experiment:
- Corpus name, original source URL, version and retrieval date
- Licence and whether redistribution is permitted
- Language, total count and spam/ham class counts
- Extraction and cleaning steps, exact and near-duplicate removal
- Whether messages share threads or senders that require a grouped split
- SHA256 of the final CSV (also recorded automatically in the run manifest)

Store the prepared id,text,label CSV at data/private/emails.csv.
The default research config assumes independent messages and a stratified 80/20 split.
If a corpus has related threads or near duplicates, resolve groups and revise the split
before running; the current script does not implement grouped splitting.
Never upload private emails or unlicensed corpora to the public repository.

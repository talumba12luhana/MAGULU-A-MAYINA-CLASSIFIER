import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import joblib

print("Loading dataset...")
df = pd.read_csv('chichewa_noun_dataset.csv')
df = df[['singular nouns', 'class']].dropna()
df['singular nouns'] = df['singular nouns'].str.lower().str.strip()
df['class'] = df['class'].str.lower().str.strip()

# Typo map from previous analysis
TYPO_MAP = {
    "mumi": "mu-mi",
    "i--zi": "i-zi",
    "lima": "li-ma",
    "u-": "u-ma",
    "chii-zi": "chi-zi",
    "chizi": "chi-zi",
    "chu-zi": "chi-zi",
    "ch-zi": "chi-zi"
}
df['class'] = df['class'].replace(TYPO_MAP)

X = df['singular nouns']
y = df['class']

print("Training pipeline using scikit-learn 1.5.0...")
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(analyzer='char', ngram_range=(1, 3))),
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
])

pipeline.fit(X, y)

print("Saving model to chichewa_noun_classifier.pkl...")
joblib.dump(pipeline, 'chichewa_noun_classifier.pkl')
print("Done! Ready for Vercel.")

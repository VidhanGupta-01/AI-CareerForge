import pandas as pd
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

print("Loading data...")
df = pd.read_csv('Resume.csv')

def clean_text(text):
    text = str(text).lower()
    return re.sub(r'[^a-z0-9\s]', '', text)

print("Cleaning data...")
df['Clean_Resume'] = df['Resume_str'].apply(clean_text)

print("Training model (this takes a few seconds)...")
model = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=3000, stop_words='english')),
    ('clf', LogisticRegression(max_iter=1000))
])

model.fit(df['Clean_Resume'], df['Category'])

joblib.dump(model, 'resume_classifier.pkl')
print("DONE! Model saved as 'resume_classifier.pkl'")

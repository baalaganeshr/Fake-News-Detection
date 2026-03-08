"""
Retrain the model with the current scikit-learn version.
Replicates the exact training pipeline from the notebook.
"""
import pandas as pd
import re
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn import metrics

nltk.download('stopwords', quiet=True)
ps = PorterStemmer()

# Load datasets
print("Loading datasets...")
true = pd.read_csv('../dataset/True.csv')
fake = pd.read_csv('../dataset/Fake.csv')

# Assign labels: true=1, fake=0 (same as notebook)
true['label'] = 1
fake['label'] = 0

# Use first 5000 of each (same as notebook)
frames = [true.loc[:5000][:], fake.loc[:5000][:]]
df = pd.concat(frames)
df = df.dropna()
df2 = df.copy()
df2.reset_index(inplace=True)

print(f"Dataset shape: {df2.shape}")

# Preprocessing - stemming and stopword removal
print("Preprocessing text (this may take a minute)...")
corpus = []
stop_words = set(stopwords.words('english'))
for i in range(len(df2)):
    review = re.sub('[^a-zA-Z]', ' ', df2['text'][i])
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review if word not in stop_words]
    review = ' '.join(review)
    corpus.append(review)

# TF-IDF Vectorization (same params as notebook)
print("Vectorizing...")
tfidf_v = TfidfVectorizer(max_features=5000, ngram_range=(1, 3))
X = tfidf_v.fit_transform(corpus).toarray()
y = df2['label']

# Train/test split (same params as notebook)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Train PassiveAggressiveClassifier (same as notebook)
print("Training model...")
classifier = PassiveAggressiveClassifier(max_iter=1000)
classifier.fit(X_train, y_train)

# Evaluate
pred = classifier.predict(X_test)
accuracy = metrics.accuracy_score(y_test, pred)
print(f"Accuracy: {accuracy:.3f}")
print(f"Confusion Matrix:\n{metrics.confusion_matrix(y_test, pred)}")

# Save model and vectorizer
print("Saving model2.pkl and tfidfvect2.pkl...")
pickle.dump(classifier, open('model2.pkl', 'wb'))
pickle.dump(tfidf_v, open('tfidfvect2.pkl', 'wb'))

print("Done! Model retrained and saved successfully.")

import pickle
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()
model = pickle.load(open('model2.pkl', 'rb'))
tfidfvect = pickle.load(open('tfidfvect2.pkl', 'rb'))

def predict(text):
    review = re.sub('[^a-zA-Z]', ' ', text)
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
    review = ' '.join(review)
    review_vect = tfidfvect.transform([review]).toarray()
    raw = model.predict(review_vect)
    return raw[0]

# Real news samples
real1 = "WASHINGTON (Reuters) - The head of a conservative Republican faction in the U.S. Congress, who voted this month for a huge expansion of the national debt to pay for tax cuts, called himself a fiscal conservative on Sunday and urged budget restraint in 2018."
real2 = "WASHINGTON (Reuters) - Transgender people will be allowed for the first time to enlist in the U.S. military starting on Monday as ordered by federal courts, the Pentagon said on Friday."

# Fake news samples
fake1 = "Donald Trump just couldn t wish all Americans a Happy New Year and leave it at that. Instead, he had to give a shout out to his enemies, haters and the very dishonest fake news media."
fake2 = "House Intelligence Committee Chairman Devin Nunes is going to have a bad day. He s been under the assumption that the Christopher Steele dossier was what prompted the Russia investigation."

print("=== Model raw predictions ===")
print(f"Real news 1: model.predict = {predict(real1)}  (expected: should map to REAL)")
print(f"Real news 2: model.predict = {predict(real2)}  (expected: should map to REAL)")
print(f"Fake news 1: model.predict = {predict(fake1)}  (expected: should map to FAKE)")
print(f"Fake news 2: model.predict = {predict(fake2)}  (expected: should map to FAKE)")
print()
print("Current app logic: FAKE if predict==0, REAL if predict==1")
print("If real news gives 0 and fake gives 1, labels are INVERTED")

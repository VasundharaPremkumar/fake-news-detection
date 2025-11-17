import pandas as pd
import numpy as np
df_fake = pd.read_csv("../data/train.csv")
df_real = pd.read_csv("../data/Truedata.csv")
# print(df.columns)#quick check abt the useful and not soo useful columns

#lets keep text and title together and subject as another separate attribute
df_fake['contents']=df_fake['title'].fillna('')+" "+df_fake['text'].fillna('')
df_real['contents']=df_real['title'].fillna('')+" "+df_real['text'].fillna('')
#keeping only contents and subject
# (we'll add labels and then keep only contents+label)
print("fake shape:", df_fake.shape, " real shape:", df_real.shape)

'''lower() → makes everything lowercase

re.sub(r'[^a-zA-Z\s]', '', text) → removes all characters except letters and spaces

re.sub(r'\s+', ' ', text) → fixes extra spaces

.apply() → applies the function to every row'''

#if i were to do the cleaning the data for one row then there was no necessity of using the functions
# should  make sure that the code would be structured and does not crash
import re
def clean_data(text):
    text=text.lower()
    text=re.sub(r'[^a-zA-Z\s]',' ',text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# apply cleaning to both datasets
df_fake['clean_content']=df_fake['contents'].apply(clean_data)
df_real['clean_content']=df_real['contents'].apply(clean_data)

# add labels: fake -> 1, real -> 0
df_fake['label'] = 1
df_real['label'] = 0

# keep only cleaned content and label
df_fake = df_fake[['clean_content','label']].copy()
df_real = df_real[['clean_content','label']].copy()

# combine both
df = pd.concat([df_fake, df_real], ignore_index=True)
# shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print(df.shape)
print(df['label'].value_counts())


#(A) SAVE MERGED CLEANED DATASET 
df.to_csv("../data/merged.csv", index=False)
print("Merged cleaned dataset saved as ../data/merged.csv")


# quick check on whether it is working fine
# print(df['clean_content'].head())

'''What is TF-IDF in easy words?

TF = how often a word appears in this document.

IDF = how rare that word is across all documents (rare words get more weight).

TF-IDF = bigger number for words that appear a lot in one article but not in many other articles.

Result: each article becomes a long list of numbers — one number per word (feature).'''
from sklearn.feature_extraction.text import TfidfVectorizer
# spilltinf into test and train datasets
from sklearn.model_selection import train_test_split

# ---------- CORRECT SEQUENCE: split FIRST, then fit TF-IDF on training text ----------
# create X and y from merged dataframe (raw text strings for now)
X_text = df['clean_content']   # raw cleaned text strings
y = df['label']

# split into train/test BEFORE fitting TF-IDF (avoids data leakage)
X_train_text, X_test_text, y_train, y_test = train_test_split(
    X_text, y, test_size=0.2, random_state=42, stratify=y
)

print("Train size:", len(X_train_text))
print("Test size:", len(X_test_text))

tfidf = TfidfVectorizer(
    max_df=0.8,         # ignore words that appear in more than 80% documents (common words)
    min_df=5,           # ignore very rare words (appear < 5 times)
    stop_words='english', # remove the, is, and, etc
    ngram_range=(1,2),  # consider single words + pairs
)

# fit on training text only (no leakage)
tfidf.fit(X_train_text)

# convert train and test text into numeric matrices
X_train = tfidf.transform(X_train_text)
X_test  = tfidf.transform(X_test_text)

print("TF-IDF shapes -> X_train:", X_train.shape, " X_test:", X_test.shape)

# now X_train, X_test, y_train, y_test are ready for training a model
from sklearn.linear_model import LogisticRegression
model=LogisticRegression(max_iter=500, class_weight='balanced')
model.fit(X_train,y_train)

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
y_predict=model.predict(X_test)
acc=accuracy_score(y_predict,y_test)
print("\n Test accuracy is ",acc)#printing the accuracy
print("Classification report:")
print(classification_report(y_test, y_predict, digits=4))
print("Confusion matrix:\n", confusion_matrix(y_test, y_predict))

import joblib

joblib.dump(tfidf, "../models/tfidf_vectorizer.joblib")
joblib.dump(model, "../models/fakenews_model.joblib")
print("Saved model and TF-IDF into models folder!")

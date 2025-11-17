# src/predict.py
import joblib

# local copy of your cleaning function (keeps predict independent of fakenews.py)
import re
def clean_data(text):
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# load saved model and tfidf (paths you used earlier)
tfidf_path = "../models/tfidf_vectorizer.joblib"
model_path = "../models/fakenews_model.joblib"

tfidf = joblib.load(tfidf_path)
model = joblib.load(model_path)

print("Model and TF-IDF loaded. Type text and press Enter (Ctrl+C to quit).")

while True:
    try:
        raw = input("\nEnter news text: ")
        if raw.strip() == "":
            print("Please enter some text.")
            continue
        cleaned = clean_data(raw)
        vec = tfidf.transform([cleaned])
        pred = model.predict(vec)[0]
        prob = None
        if hasattr(model, "predict_proba"):
            prob = float(max(model.predict_proba(vec)[0]))
        if pred == 1:
            print("PREDICTION: FAKE NEWS ", f"(confidence: {prob:.2%})" if prob is not None else "")
        else:
            print("PREDICTION: REAL NEWS ", f"(confidence: {prob:.2%})" if prob is not None else "")
    except KeyboardInterrupt:
        print("\nExiting.")
        break

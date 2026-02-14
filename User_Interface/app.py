from flask import Flask, render_template, request, jsonify
import joblib
import re

app = Flask(__name__)

# Load the trained model and vectorizer
tfidf = joblib.load('/mnt/user-data/uploads/tfidf_vectorizer.joblib')
model = joblib.load('/mnt/user-data/uploads/fakenews_model.joblib')

def clean_data(text):
    """Clean and preprocess text data"""
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@app.route('/')
def home():
    """Render the main page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    try:
        data = request.get_json()
        news_text = data.get('text', '')
        
        if not news_text.strip():
            return jsonify({
                'error': 'Please enter some text to analyze'
            }), 400
        
        # Clean the text
        cleaned_text = clean_data(news_text)
        
        # Vectorize
        vectorized = tfidf.transform([cleaned_text])
        
        # Predict
        prediction = model.predict(vectorized)[0]
        
        # Get probability scores
        probabilities = model.predict_proba(vectorized)[0]
        confidence = float(max(probabilities)) * 100
        
        # Determine result
        is_fake = bool(prediction == 1)
        label = "FAKE NEWS" if is_fake else "REAL NEWS"
        
        # Additional analysis
        real_prob = float(probabilities[0]) * 100
        fake_prob = float(probabilities[1]) * 100
        
        return jsonify({
            'prediction': label,
            'is_fake': is_fake,
            'confidence': round(confidence, 2),
            'real_probability': round(real_prob, 2),
            'fake_probability': round(fake_prob, 2),
            'original_text': news_text,
            'word_count': len(news_text.split())
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/sample', methods=['GET'])
def get_sample():
    """Provide sample news texts for testing"""
    samples = {
        'fake': "BREAKING: Scientists discover that drinking 10 glasses of water instantly cures all diseases! Doctors hate this simple trick that pharmaceutical companies don't want you to know about!",
        'real': "The World Health Organization announced today that a new variant of the virus has been detected in several countries. Health officials are monitoring the situation closely and recommend continued adherence to public health guidelines."
    }
    return jsonify(samples)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

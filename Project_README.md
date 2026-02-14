# 🛡️ Fake News Detection - AI-Powered Web Application

A modern, neon-themed web application for detecting fake news using Machine Learning (Logistic Regression) with a beautiful dark UI.

## 🌟 Features

- **AI-Powered Detection**: Uses Logistic Regression trained on thousands of news articles
- **Beautiful Dark Neon UI**: Modern, responsive design with stunning animations
- **Real-time Analysis**: Instant predictions with confidence scores
- **Educational Content**: Awareness information about fake news
- **Sample Testing**: Built-in fake and real news samples
- **Probability Visualization**: Interactive probability bars showing real vs fake likelihood

## 📋 Requirements

```
Python 3.7+
Flask
joblib
scikit-learn
pandas
numpy
```

## 🚀 Installation

1. **Install Dependencies**
```bash
pip install flask joblib scikit-learn pandas numpy
```

2. **File Structure**
Ensure you have the following structure:
```
project/
├── app.py
├── fakenews_model.joblib
├── tfidf_vectorizer.joblib
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

3. **Run the Application**
```bash
python app.py
```

4. **Access the Application**
Open your browser and navigate to:
```
http://localhost:5000
```

## 🎮 Usage

### Method 1: Use Sample Data
1. Click "Try Fake News Sample" or "Try Real News Sample"
2. Click "Analyze News" button
3. View the results with confidence scores

### Method 2: Enter Your Own Text
1. Paste or type news article text in the text area
2. Click "Analyze News" button
3. View detailed analysis results

### Keyboard Shortcut
- Press `Ctrl+Enter` (or `Cmd+Enter` on Mac) to quickly analyze

## 📊 How It Works

### Machine Learning Model
- **Algorithm**: Logistic Regression
- **Feature Extraction**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Training Data**: Thousands of verified fake and real news articles
- **Output**: Binary classification (Real/Fake) with probability scores

### Text Processing Pipeline
1. **Input**: Raw news article text
2. **Cleaning**: Lowercase conversion, special character removal, whitespace normalization
3. **Vectorization**: TF-IDF transformation
4. **Prediction**: Logistic Regression classification
5. **Output**: Prediction label + confidence scores

## 🎨 UI Features

### Dark Neon Theme
- Cyan, Pink, Purple, and Green neon accents
- Animated background elements
- Smooth transitions and hover effects
- Responsive design for all devices

### Components
- **Warning Banner**: Awareness about fake news spread
- **Input Section**: Text area with word counter
- **Results Display**: 
  - Verdict with icon
  - Confidence badge
  - Probability bars
  - Statistics cards
  - Educational tips

## 🔍 Sample Outputs

### Fake News Detection
```
Prediction: FAKE NEWS DETECTED ⚠️
Confidence: 95.7%
Real Probability: 4.3%
Fake Probability: 95.7%
```

### Real News Detection
```
Prediction: LIKELY REAL NEWS ✓
Confidence: 92.3%
Real Probability: 92.3%
Fake Probability: 7.7%
```

## ⚠️ Disclaimer

This tool provides probability-based predictions using machine learning. It should be used as ONE of many resources to verify information. Always:

- Cross-verify with multiple trusted sources
- Check the original source and publication date
- Look for author credentials
- Be critical of sensational headlines
- Fact-check before sharing

## 🛠️ Technical Details

### Flask Routes
- `GET /` - Main page
- `POST /predict` - Prediction API endpoint
- `GET /sample` - Get sample texts for testing

### API Response Format
```json
{
  "prediction": "FAKE NEWS",
  "is_fake": true,
  "confidence": 95.7,
  "real_probability": 4.3,
  "fake_probability": 95.7,
  "original_text": "...",
  "word_count": 45
}
```

## 🎯 Model Performance

The model was trained on a dataset of verified fake and real news articles with:
- High accuracy on test data
- Balanced class weights to handle imbalanced datasets
- TF-IDF features capturing important word patterns
- Logistic Regression for interpretable results

## 🌐 Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Opera

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

## 🔐 Security

- No data is stored on the server
- All analysis happens in real-time
- No user tracking or cookies

## 🤝 Contributing

Feel free to enhance the application by:
- Improving the UI/UX
- Adding more features
- Enhancing the model
- Adding more educational content

## 📄 License

This project is for educational purposes.

## 🙏 Acknowledgments

- Machine Learning model based on Logistic Regression
- UI inspired by modern cyberpunk/neon aesthetics
- Built with Flask, HTML5, CSS3, and JavaScript

---

**Made with ❤️ for fighting misinformation**

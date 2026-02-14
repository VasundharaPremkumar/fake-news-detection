// Global sample texts
let sampleTexts = {};

// Word count updater
const newsTextArea = document.getElementById('newsText');
const wordCountDisplay = document.getElementById('wordCount');

newsTextArea.addEventListener('input', function() {
    const text = this.value.trim();
    const words = text ? text.split(/\s+/).length : 0;
    wordCountDisplay.textContent = `${words} words`;
});

// Load sample news function
async function loadSample(type) {
    try {
        const response = await fetch('/sample');
        sampleTexts = await response.json();
        
        if (type === 'fake') {
            newsTextArea.value = sampleTexts.fake;
        } else if (type === 'real') {
            newsTextArea.value = sampleTexts.real;
        }
        
        // Trigger word count update
        newsTextArea.dispatchEvent(new Event('input'));
        
        // Scroll to textarea
        newsTextArea.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } catch (error) {
        console.error('Error loading sample:', error);
        alert('Failed to load sample text. Please try again.');
    }
}

// Analyze news function
async function analyzeNews() {
    const newsText = newsTextArea.value.trim();
    
    // Validation
    if (!newsText) {
        alert('Please enter some text to analyze.');
        return;
    }
    
    if (newsText.split(/\s+/).length < 5) {
        alert('Please enter at least 5 words for accurate analysis.');
        return;
    }
    
    // Show loading, hide results
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    
    loading.classList.add('active');
    results.style.display = 'none';
    
    // Scroll to loading
    loading.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: newsText })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Analysis failed');
        }
        
        const data = await response.json();
        
        // Hide loading
        loading.classList.remove('active');
        
        // Display results
        displayResults(data);
        
        // Scroll to results
        setTimeout(() => {
            results.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
        
    } catch (error) {
        loading.classList.remove('active');
        console.error('Error:', error);
        alert(`Error: ${error.message}`);
    }
}

// Display results function
function displayResults(data) {
    const results = document.getElementById('results');
    const verdict = document.getElementById('verdict');
    const verdictIcon = document.getElementById('verdictIcon');
    const verdictLabel = document.getElementById('verdictLabel');
    const confidenceBadge = document.getElementById('confidenceBadge');
    
    const realProb = document.getElementById('realProb');
    const fakeProb = document.getElementById('fakeProb');
    const realBar = document.getElementById('realBar');
    const fakeBar = document.getElementById('fakeBar');
    
    const wordCountStat = document.getElementById('wordCountStat');
    const accuracyStat = document.getElementById('accuracyStat');
    
    const educationalInfo = document.getElementById('educationalInfo');
    
    // Set verdict
    if (data.is_fake) {
        verdict.className = 'verdict fake';
        verdictIcon.textContent = '⚠️';
        verdictLabel.textContent = 'FAKE NEWS DETECTED';
    } else {
        verdict.className = 'verdict real';
        verdictIcon.textContent = '✓';
        verdictLabel.textContent = 'LIKELY REAL NEWS';
    }
    
    // Set confidence
    confidenceBadge.textContent = `${data.confidence}% Confidence`;
    
    // Set probabilities
    realProb.textContent = `${data.real_probability}%`;
    fakeProb.textContent = `${data.fake_probability}%`;
    
    // Animate probability bars
    setTimeout(() => {
        realBar.style.width = `${data.real_probability}%`;
        fakeBar.style.width = `${data.fake_probability}%`;
    }, 100);
    
    // Set stats
    wordCountStat.textContent = data.word_count;
    accuracyStat.textContent = `${data.confidence}%`;
    
    // Educational information
    const educationalContent = data.is_fake ? `
        <h4>🚨 Red Flags Detected</h4>
        <ul>
            <li>Sensational or exaggerated language patterns detected</li>
            <li>Content structure shows characteristics common in misinformation</li>
            <li>Consider checking multiple trusted news sources</li>
            <li>Look for official statements or verified sources</li>
        </ul>
    ` : `
        <h4>✓ Credibility Indicators</h4>
        <ul>
            <li>Text patterns align with verified news sources</li>
            <li>Professional language structure detected</li>
            <li>Still recommended to verify from multiple sources</li>
            <li>Check publication date and author credentials</li>
        </ul>
    `;
    
    educationalInfo.innerHTML = educationalContent;
    
    // Show results
    results.style.display = 'block';
}

// Enter key support for textarea
newsTextArea.addEventListener('keydown', function(e) {
    // Ctrl+Enter or Cmd+Enter to analyze
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        analyzeNews();
    }
});

// Load samples on page load
window.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch('/sample');
        sampleTexts = await response.json();
    } catch (error) {
        console.error('Error preloading samples:', error);
    }
});

from flask import Flask, request, jsonify
import joblib
import numpy as np
from scipy.sparse import hstack
import string

app = Flask(__name__)

# 1. Load the "Brain" (Model and Vectorizer)
model = joblib.load('final_hybrid_phishing_model.pkl')
tfidf = joblib.load('final_tfidf_vectorizer.pkl')

# 2. Re-define the cleaning logic (must match training)
def clean_text(text):
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Note: For production, ensure nltk stopwords are available
    return text

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    email_body = data.get('email', '')
    
    # 3. Process the input
    cleaned = clean_text(email_body)
    urls = email_body.count('http')
    exclamations = email_body.count('!')
    
    # Simple urgency check for the API
    urgency_list = ['urgent', 'immediately', 'suspended', 'verify', 'security']
    urgency = sum(1 for word in urgency_list if word in cleaned)
    
    # 4. Transform and Predict
    text_vector = tfidf.transform([cleaned])
    heuristics = np.array([[urls, exclamations, urgency]])
    final_input = hstack([text_vector, heuristics])
    
    probability = model.predict_proba(final_input)[0][1]
    prediction = 1 if probability > 0.15 else 0 # Keeping your tuned threshold
    
    return jsonify({
        'prediction': int(prediction),
        'confidence': round(float(probability * 100), 2),
        'status': 'Phishing' if prediction == 1 else 'Safe'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
from flask import Flask, request, jsonify
import joblib
import numpy as np
from scipy.sparse import hstack
import string
import gradio as gr
import threading

app = Flask(__name__)

# 1. Load the "Brain" (Model and Vectorizer)
model = joblib.load('final_hybrid_phishing_model.pkl')
tfidf = joblib.load('final_tfidf_vectorizer.pkl')

# 2. Re-define the cleaning logic
def clean_text(text):
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Internal logic shared by both Flask and Gradio
def perform_prediction(email_body):
    cleaned = clean_text(email_body)
    urls = email_body.count('http')
    exclamations = email_body.count('!')
    
    urgency_list = ['urgent', 'immediately', 'suspended', 'verify', 'security']
    urgency = sum(1 for word in urgency_list if word in cleaned)
    
    text_vector = tfidf.transform([cleaned])
    heuristics = np.array([[urls, exclamations, urgency]])
    final_input = hstack([text_vector, heuristics])
    
    probability = model.predict_proba(final_input)[0][1]
    prediction = 1 if probability > 0.15 else 0
    return prediction, probability

# --- FLASK ROUTES ---
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    email_body = data.get('email', '')
    
    prediction, probability = perform_prediction(email_body)
    
    return jsonify({
        'prediction': int(prediction),
        'confidence': round(float(probability * 100), 2),
        'status': 'Phishing' if prediction == 1 else 'Safe'
    })

# --- GRADIO UI SETUP ---
def gradio_interface(email_content):
    prediction, probability = perform_prediction(email_content)
    status = " PHISHING DETECTED" if prediction == 1 else " SAFE EMAIL"
    confidence = round(float(probability * 100), 2)
    
    result = f"Analysis: {status}\nConfidence Score: {confidence}%"
    return result

demo = gr.Interface(
    fn=gradio_interface,
    inputs=gr.Textbox(lines=7, label="Paste Email Body", placeholder="Enter email text here..."),
    outputs=gr.Textbox(label="AI Detection Result"),
    title="ShieldAI: Phishing Detector",
    description="This AI model uses a Hybrid Random Forest approach to detect phishing attempts based on text patterns and structural heuristics.",
    theme="soft"
)

# Function to run Flask in a separate thread
def run_flask():
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # 1. Start Flask in the background
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # 2. Start Gradio in the foreground
    # share=True creates a public link so you can show your professor/friends!
    demo.launch(share=True)
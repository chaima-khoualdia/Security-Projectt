# ShieldAI: End-to-End Phishing Detection System

## 1. Project Overview
This project implements an end-to-end **hybrid phishing detection** system. Given the body of an email, it outputs:
- `prediction`: `1` (Phishing) or `0` (Safe)
- `confidence`: probability score scaled to a percentage

The system combines:
- **Text semantics** via a TF-IDF vectorizer
- **Hand-crafted heuristic features** from the email body
- A trained **Random Forest** classifier that consumes both feature types

The project exposes:
- A **Flask REST API** (`POST /predict`)
- A **Gradio UI** for interactive testing

---

## 2. Inference Pipeline (How the Detection Works)
When an email body is submitted, the app performs the following steps:

### 2.1 Text cleaning / normalization
The input text is:
- converted to lowercase
- stripped of punctuation

### 2.2 Heuristic feature extraction
From the *raw* email body, the app computes:
- `urls = email_body.count('http')`
- `exclamations = email_body.count('!')`

Then it computes an `urgency` score based on substring membership in the **cleaned** text:
```python
urgency_list = ['urgent', 'immediately', 'suspended', 'verify', 'security']
urgency = sum(1 for word in urgency_list if word in cleaned_text)

```

So the heuristic vector is: `[urls, exclamations, urgency]`

### 2.3 TF-IDF vectorization + feature fusion

```python
text_vector = tfidf.transform([cleaned])
heuristics = np.array([[urls, exclamations, urgency]])
final_input = hstack([text_vector, heuristics])

```

### 2.4 Classification + decision threshold

```python
probability = model.predict_proba(final_input)[0][1]
prediction = 1 if probability > 0.15 else 0

```

The threshold is 0.15 to prefer higher recall (more phishing flagged).

---

## 3. REST API: POST /predict

### Request

* **Method:** POST
* **Content-Type:** application/json
* **Body** must include an email field:

```json
{
  "email": "Paste the full email body text here..."
}

```

If email is missing, the code uses an empty string.

### Response

The API returns:

```json
{
  "prediction": 1,
  "confidence": 20.0,
  "status": "Phishing"
}

```

* `status` is "Phishing" when prediction == 1, otherwise "Safe"
* `confidence` = probability * 100, rounded to 2 decimals

### Example (cURL)

```bash
curl -X POST [http://127.0.0.1:5000/predict](http://127.0.0.1:5000/predict) \
  -H "Content-Type: application/json" \
  -d '{"email": "Urgent! Your account is compromised. Click [http://secure-verify.com](http://secure-verify.com) now!"}'

```

---

## 4. Gradio UI

Running `app.py` also starts a Gradio interface. You paste an email body into a textbox and receive a single output text string in the format:

```text
Analysis: PHISHING DETECTED
Confidence Score: XX.XX%

```

(When safe, it shows `Analysis: SAFE EMAIL`.)

The Gradio app is launched with:

```python
demo.launch(share=True)

```

---

## 5. Required Runtime Files

`app.py` loads these artifacts from the project root:

* `final_hybrid_phishing_model.pkl`
* `final_tfidf_vectorizer.pkl`

---

## 6. Dependencies

Install required packages (for `app.py`):

```bash
pip install flask joblib numpy scipy scikit-learn gradio

```

---

## 7. How to Run

Start the server:

```bash
python app.py

```

* Flask runs on port 5000
* Gradio UI runs at launch (and uses `share=True`)

---

## 8. Security / Reliability Note

This system is a probabilistic classifier. Output should be treated as an aid for defensive review, not as absolute truth. Always use additional security controls and human verification for high-impact actions.

```
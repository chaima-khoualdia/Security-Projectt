#  AI-Powered Phishing Security Project: End-to-End Detection System

## 1. Project Overview & Core Concepts
Phishing remains one of the most prevalent cyber threats, leveraging social engineering to deceive users into disclosing sensitive information. This project implements a **Hybrid Machine Learning Detection System** that analyzes both the semantic content of an email and its structural metadata.

### Main Components
*   **NLP Processor:** Utilizes TF-IDF (Term Frequency-Inverse Document Frequency) to convert raw text into weighted numerical vectors, capturing the linguistic "signature" of phishing attempts.
*   **Heuristic Feature Extractor:** A custom logic layer that identifies key security indicators:
    *   **URL Count:** Tracking the presence of hyperlinks.
    *   **Exclamation Density:** Measuring high-pressure punctuation usage.
    *   **Urgency Keywords:** Identifying triggers like "immediately," "suspended," or "verify."
*   **Classification Head:** A **Random Forest Classifier** that fuses NLP vectors with heuristic data to provide a final risk assessment.

### Functional Flow
1.  **Ingestion:** The system receives a raw email string via a REST API endpoint.
2.  **Preprocessing:** Text is normalized (lowercasing, punctuation removal).
3.  **Feature Fusion:** Sparse text matrices are horizontally stacked with dense heuristic arrays.
4.  **Inference:** The model calculates the probability of a threat.
5.  **Decision Logic:** A tuned threshold of **0.15** is applied to prioritize **Recall**, ensuring even subtle "low-confidence" threats are flagged.

---

## 2. Market Analysis: Existing Solutions
Existing phishing defense mechanisms typically rely on two pillars:
*   **Blacklisting:** Comparing URLs against databases of known malicious sites. 
    *   *Limitation:* Ineffective against "Zero-Day" attacks or fresh domains.
*   **Static Keyword Filtering:** Looking for specific "spam" words.
    *   *Limitation:* Easily bypassed by changing the wording or using images.
*   **Proposed Solution:** This project addresses these gaps by using **Behavioral Modeling**. By training on 450,000+ real-world emails (Enron and Kaggle datasets), the model learns the *pattern* of a scam rather than just a list of bad words.

---

## 3. High-Level Design (HLD)
The system architecture is designed for low-latency inference and easy integration into existing mail servers or Progressive Web Apps (PWAs).



### System Components & Data Exchange
| Component | Function | Exchanged Data |
| :--- | :--- | :--- |
| **Client** | User Interface (e.g., PWA) | Sends raw email body via POST request. |
| **Flask API** | Backend Controller | Routes data and handles JSON serialization. |
| **ML Engine** | Vectorizer & Model | Returns `Prediction` (0/1) and `Confidence` (%). |

---

## 4. Tools & Development Phases
### Tech Stack
*   **Language:** Python 3.x
*   **Core Libraries:** Scikit-learn, Pandas, Numpy, Joblib, Scipy.
*   **Backend:** Flask (WSGI Server).
*   **Environment:** Git Bash, Jupyter Notebook.

### Development Phases
1.  **EDA & Preprocessing:** Analysis of imbalanced datasets and text normalization.
2.  **Feature Engineering:** Development of the hybrid feature fusion logic (`predict_phishing_v3`).
3.  **Training & Optimization:** Tuning the Random Forest parameters and adjusting the classification threshold for high sensitivity.
4.  **Deployment:** Serialization of the model into `.pkl` format and deployment as a RESTful service.

---

## 5. Executable Deliverable
The primary deliverable is an **Active Phishing Detection API**.

### How to Run:
1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    ```
2.  **Install Dependencies:**
    ```bash
    pip install flask joblib scikit-learn scipy
    ```
3.  **Initialize the Server:**
    
```bash
    python app.py
    ```
4.  **Live Test (via Git Bash):**
    ```bash
    curl -X POST http://127.0.0.1:5000/predict \
         -H "Content-Type: application/json" \
         -d '{"email": "Urgent! Your account is compromised. Click http://secure-verify.com now!"}'
    ```

### Expected Output:
```json
{
  "status": "Phishing",
  "prediction": 1,
  "confidence": 20.0
}
```


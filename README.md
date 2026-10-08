# 🏦 Autonomous Credit Underwriting & Risk Prediction System

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Library-Scikit--Learn-orange.svg)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red.svg)](https://streamlit.io/)

---

## 📌 Executive Summary
Automated retail credit underwriting requires balancing portfolio expansion against default exposure. In institutional lending, approving a non-performing borrower (**Type I Error / False Positive**) incurs substantial capital write-offs, whereas rejecting a creditworthy borrower (**Type II Error / False Negative**) only incurs the opportunity cost of unrealised interest margin. 

This repository implements an end-to-end, explainable credit scoring engine designed to assess retail credit risk, optimise classification thresholds against asymmetric lending losses, and serve real-time decisions via an interactive deployment interface.

---

## ⚙️ Feature Engineering & Solvency Architecture

Rather than relying on unscaled raw inputs, the pipeline derives domain-specific solvency features prior to ingestion:

| Engineered Feature | Mathematical Formulation | Financial Rationale |
| :--- | :--- | :--- |
| **Total Household Solvency** | `ApplicantIncome + CoapplicantIncome` | Captures aggregate debt-servicing capacity across the domestic unit. |
| **Debt-to-Income (DTI)** | `(LoanAmount * 1000) / (Total_Income + 1)` | Evaluates overall capital leverage relative to earning power. |
| **Estimated Annuity (EMI)** | `(LoanAmount * 1000) / Loan_Amount_Term` | Approximates monthly principal amortization obligation. |
| **Annuity-to-Income Coverage** | `Estimated_EMI / ((Total_Income / 12) + 1)` | Measures liquidity stress by tracking monthly debt service against gross monthly inflow. |
| **Per-Capita Dependency Burden** | `Total_Income / (Dependents + 1)` | Adjusts gross income for domestic consumption drag. |

---

## 📈 Model Performance & Validation

Models were evaluated using an 80/20 train/test split stratified across the binary outcome `Loan_Status`. Performance metrics prioritise default detection precision alongside global discrimination power (ROC-AUC):

| Model Architecture | Accuracy | Precision (Default) | Recall (Default) | Macro F1 | ROC-AUC | Primary Limitation / Strength |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Balanced Random Forest (Selected)** | **80.83%** | **0.86** | **0.47** | **0.74** | **0.78** | **High precision against bad credit; catches high-risk defaults without false alarms.** |
| **Logistic Regression (Scaled)** | 81.67% | 0.81 | 0.45 | 0.73 | 0.77 | Fast convergence; assumes linear relationship across engineered ratios. |
| **Support Vector Classifier (SVC)** | 80.83% | 0.80 | 0.42 | 0.70 | 0.75 | Consistent boundary separation; slower on non-linear kernel transformations. |
| **K-Nearest Neighbors (k=5)** | 79.17% | 0.65 | 0.40 | 0.65 | 0.71 | Distance metrics degrade across sparse or mixed categorical features. |

> **Decision Threshold Policy:** The scoring engine applies an asymmetric probability threshold. Applicants with approval confidence $\ge$ 60% are automatically cleared, scores between 40% and 59% are flagged for **Manual Underwriter Review**, and scores < 40% are declined to mitigate default exposure.

---

## 🔍 Interpretability & Policy Guidance (XAI)
* **Credit History Primacy:** Historical debt repayment behaviour remains the dominant predictor of approval viability.
* **Solvency Buffers:** High loan amounts combined with elevated DTI ratios trigger automated routing for human manual underwriting when falling within borderline probability thresholds (0.40 – 0.55).

---

## 🏗️ System Architecture & Repository Structure

```text
Loan-Approval-Prediction/
├── app.py                              # Streamlit inference dashboard & UI logic
├── credit_underwriting_pipeline.pkl    # Serialized end-to-end model artifact
├── LoanApprovalPrediction.csv          # Raw empirical credit records
├── Loan_Approval_Prediction.ipynb      # Exploratory data analysis & model development
├── requirements.txt                    # Pinned deployment dependencies
└── README.md                           # System documentation

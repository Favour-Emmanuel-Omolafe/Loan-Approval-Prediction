# 🏦 Loan Approval Prediction using Machine Learning

An end-to-end machine learning project evaluating Random Forest, Logistic Regression, SVC, and KNN models to predict loan approval status based on applicant financial and credit history metrics.

---

## 📌 Executive Summary
* **Objective:** Built and evaluated classification models to automate credit risk assessment and predict loan approval status (`Loan_Status`) based on financial and demographic features.
* **Top Model Performance:** The **Random Forest Classifier** achieved the highest accuracy (**82.50%**) on unseen test data, matching a scaled **Logistic Regression** model (**82.08%**).
* **Key Drivers:** **Credit History** is the single primary driver for loan approvals, followed by the balance between **Applicant Income** and **Loan Amount**.

---

## 📊 Business Recommendations
1. **Automate High-Confidence Approvals:** Deploy the Random Forest model to instantly approve applicants with flawless credit history and low debt-to-income ratios.
2. **Predictive Data Imputation:** In production, replace mean/mode imputation with **KNN or predictive imputation** to avoid distorting risk profiles.
3. **Human Underwriting Flags:** Establish decision thresholds where high-risk or borderline applications (e.g., strong credit score but disproportionately large loan amount) are routed to human loan officers for secondary review.

---

## 🛠️ Machine Learning Pipeline
1. **Exploratory Data Analysis (EDA):** Visualization of categorical distributions and numerical feature correlations.
2. **Preprocessing:** Label Encoding for categorical variables, `StandardScaler` for continuous feature normalization.
3. **Model Training & Comparison:** Evaluated Random Forest, KNN, Support Vector Classifier (SVC), and Logistic Regression.
4. **Evaluation Metrics:** Evaluated accuracy, precision, recall, confusion matrix, and feature importances.

---

## 📈 Model Performance Matrix

| Algorithm | Testing Accuracy |
| :--- | :--- |
| **Random Forest Classifier** | **82.50%** |
| **Logistic Regression (Scaled)** | **82.08%** |
| **Support Vector Classifier (SVC)** | **69.17%** |
| **K-Nearest Neighbors (KNN)** | **63.75%** |

# 🌾 KrishiKalyanAI

KrishiKalyanAI is a machine learning-based web application designed to assist farmers in making data-driven decisions for crop selection and fertilizer usage.

## 🚀 Features

* Crop recommendation based on soil nutrients (N, P, K) and environmental conditions
* Fertilizer suggestion tailored to predicted crop needs
* Crop suitability indicator using a scoring system
* Simple and user-friendly interface

## 🧠 How It Works

The system uses trained Random Forest machine learning models to analyze input data such as:

* Nitrogen (N), Phosphorus (P), Potassium (K)
* Temperature, humidity, rainfall, and pH

Based on this data:

* A crop is predicted that best suits the given conditions
* A fertilizer recommendation is generated
* A suitability score is calculated to indicate how ideal the conditions are

## 📊 Suitability Calculation

The Krishi Kalyan Score is calculated by comparing:

* Available soil nutrients
* Ideal nutrient requirements for the predicted crop

Based on the score:

* 🟢 Above 70 → Ideal conditions
* 🟡 40–70 → Acceptable conditions
* 🟠 Below 40 → Not ideal conditions

## 🖥️ Usage

1. Enter soil and environmental parameters
2. Click on predict
3. View:

   * Recommended crop
   * Suggested fertilizer
   * Suitability score

## 🌐 Deployment

The application is deployed using Streamlit Cloud and can be accessed through a web browser without any installation.

## 📌 Note

Predictions are based on trained models and should be used as supportive guidance alongside expert agricultural advice.

---

✨ Empowering smart farming with AI

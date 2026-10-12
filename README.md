 🔐 PrivacyGuard AI – Privacy Policy Risk Analysis

📌 About the Project

PrivacyGuard AI is a web-based application that analyzes privacy policies and identifies potential privacy risks using Natural Language Processing (NLP) and Machine Learning (ML).

The application helps users understand how websites collect, share, and manage personal information.

 🎯 Objectives

* Analyze privacy policy text.
* Identify potential privacy risks.
* Classify policy statements into risk categories.
* Calculate an overall risk score.
* Display risk analysis results through charts and tables.
* Generate downloadable analysis reports.

 🛠️ Technologies Used

* Python
* Streamlit
* Natural Language Processing (NLP)
* Machine Learning
* Scikit-learn
* Pandas
* PyPDF
* BeautifulSoup
* Requests

 ✨ Features

* Text-based privacy policy analysis.
* PDF privacy policy extraction.
* Privacy policy analysis from URLs.
* Risk classification: Low, Medium, and High.
* Category-wise risk analysis.
* High-risk statement identification.
* Visual charts and downloadable CSV reports.

 📂 Project Structure

PrivacyGuard-AI/
├── app.py
├── requirements.txt
├── README.md
├── modules/
│   ├── __init__.py
│   ├── extractor.py
│   ├── nlp_processor.py
│   ├── risk_analyzer.py
│   └── report_generator.py
└── data/
    └── dataset.csv

 ⚙️ Installation and Setup

 1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL

 2. Open the project folder


cd PrivacyGuard-AI


 3. Create a virtual environment


python -m venv .venv


 4. Activate the environment on Windows


.venv\Scripts\activate


 5. Install dependencies


pip install -r requirements.txt


6. Run the application


streamlit run app.py


 📊 Expected Output

The application displays an overall privacy risk score, risk level, category-wise analysis, high-risk statements, and downloadable reports.

🎓 Project Type

Final Year BCA Project

⚠️ Disclaimer

This project provides an educational, automated assessment of privacy policy text. Its risk scores are indicative and should not be treated as legal advice or a definitive privacy compliance assessment.

Fake News Detection and Recommendation System
 Project Overview

In the digital era, the rapid spread of misinformation and fake news has become a major challenge. This project presents a comprehensive machine learning pipeline designed to detect fake news articles and recommend reliable, personalized news content to users.

The system integrates data preprocessing, supervised and unsupervised learning techniques, ensemble methods, and basic deep learning models. Additionally, it provides explainable AI insights to understand model decisions.



 Objectives

- To classify news articles as Real or Fake using machine learning models
- To analyze and cluster similar news articles
- To reduce data dimensionality for visualization and efficiency
- To improve prediction performance using ensemble techniques
- To build a content-based recommender system
- To provide explainable insights into model predictions
- To evaluate models using industry-standard performance metrics



 Key Features

-  Fake News Classification
-  Regression Analysis (engagement prediction)
-  Clustering of news articles
-  Dimensionality Reduction (PCA / t-SNE)
-  Ensemble Learning (Random Forest, Boosting)
-  Deep Learning Model (Neural Network / LSTM)
-  Personalized Recommendation System
-  Explainable AI (Feature Importance, SHAP/LIME)


 System Architecture

1. Data Collection
2. Data Preprocessing
3. Feature Extraction (TF-IDF / Embeddings)
4. Model Training
5. Model Evaluation
6. Recommendation Engine
7. Visualization & Explainability


 Technologies Used

- Programming Language: Python
- Libraries:
  - Pandas, NumPy
  - Scikit-learn
  - Matplotlib, Seaborn
  - TensorFlow / Keras
  - NLTK / spaCy


 Dataset

The dataset consists of labeled news articles categorized as real or fake.

Attributes include:

- Title
- Text
- Author
- Label (Real/Fake)

Note: Only a sample dataset is included in this repository due to size limitations.



 Workflow

1. Data Preprocessing

- Removing stopwords
- Tokenization
- Stemming / Lemmatization
- Handling missing values

2. Feature Engineering

- TF-IDF Vectorization
- Text embeddings

3. Supervised Learning

- Logistic Regression
- Naive Bayes
- Random Forest Classifier

4. Unsupervised Learning

- K-Means Clustering
- PCA / t-SNE for visualization

5. Ensemble Techniques

- Bagging
- Boosting (AdaBoost / Gradient Boosting)

6. Deep Learning

- Neural Network / LSTM for text classification

7. Recommender System

- Content-based filtering using similarity measures

8. Explainable AI

- Feature importance analysis
- SHAP / LIME explanations



 Model Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix
- ROC-AUC Curve



 Results

- Achieved high accuracy using ensemble models
- Improved performance compared to individual models
- Effective clustering of similar news topics
- Personalized recommendations based on user interests



How to Run the Project

Step 1: Clone the repository

git clone https://github.com/mounidharan2006/mlproject-fake-news-detection.git

Step 2: Navigate to project folder

cd fake-news-ml-project

Step 3: Install dependencies

pip install -r requirements.txt

Step 4: Run the project

python main.py

or open Jupyter Notebook and run cells



 Project Structure

MLPROJECT-FAKE NEWS DETECTION/
├── models/
│   ├── model.pkl            # Trained ML model file
│   └── vectorizer.pkl       # TF-IDF or CountVectorizer for text processing
├── static/
│   ├── logo.png             # Project logo/assets
│   ├── script.js            # Frontend logic and API calls
│   └── style.css            # Custom UI styling
├── templates/
│   ├── admin.html           # Admin management panel
│   ├── dashboard.html       # User results and analytics dashboard
│   ├── history.html         # Past prediction records
│   ├── index.html           # Main landing page / input form
│   ├── login.html           # User authentication page
│   └── register.html        # New user registration
├── app.py                   # Main Flask application entry point
├── README.md                # Project documentation
├── report_utils.py          # Utility functions for generating reports
└── users.db                 # SQLite database for user/history storage




 Future Work

- Integration with real-time news APIs
- Deployment as a web/mobile application
- Multilingual fake news detection
- Advanced deep learning models (BERT, Transformers)


👤 Author

Mounidharan R


 

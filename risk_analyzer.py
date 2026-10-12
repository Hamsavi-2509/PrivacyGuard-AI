import pandas as pd

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.linear_model import (
    LogisticRegression
)

from sklearn.pipeline import Pipeline

from sklearn.model_selection import (
    train_test_split
)

from sklearn.metrics import (
    accuracy_score
)


# =========================================================
# DATASET PATH
# =========================================================

DATASET_PATH = "data/dataset.csv"


# =========================================================
# TRAIN MODEL
# =========================================================

def train_model():
    """Train and evaluate the privacy-policy classification model."""

    data = pd.read_csv(
        DATASET_PATH
    )

    # Remove missing values
    data = data.dropna(
        subset=[
            "text",
            "category"
        ]
    )

    # Split dataset
    X_train, X_test, y_train, y_test = (
        train_test_split(
            data["text"],
            data["category"],
            test_size=0.3,
            random_state=42,
            stratify=data["category"]
        )
    )


    # =====================================================
    # CREATE ML PIPELINE
    # =====================================================

    model = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2)
                )
            ),

            (
                "classifier",
                LogisticRegression(
                    max_iter=1000
                )
            )
        ]
    )


    # =====================================================
    # TRAIN MODEL
    # =====================================================

    model.fit(
        X_train,
        y_train
    )


    # =====================================================
    # TEST MODEL
    # =====================================================

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )


    print(
        f"Model Accuracy: "
        f"{accuracy * 100:.2f}%"
    )


    # =====================================================
    # RETRAIN USING COMPLETE DATASET
    # =====================================================

    model.fit(
        data["text"],
        data["category"]
    )


    return model, accuracy


# =========================================================
# PREDICT CATEGORY
# =========================================================

def predict_category(
    model,
    sentence
):
    """Predict the privacy category of a sentence."""

    prediction = model.predict(
        [sentence]
    )

    return prediction[0]


# =========================================================
# GET RISK LEVEL
# =========================================================

def get_risk_level(category):
    """Return the project-defined risk level."""

    risk_levels = {

        "Personal Data Collection":
            "Medium",

        "Third Party Sharing":
            "High",

        "Tracking and Cookies":
            "Medium",

        "Location Data":
            "High",

        "Data Retention":
            "Medium",

        "User Rights":
            "Low",

        "Data Security":
            "Low",

        "Data Breach":
            "High"
    }


    return risk_levels.get(
        category,
        "Medium"
    )


# =========================================================
# ANALYZE SENTENCES
# =========================================================

def analyze_sentences(
    model,
    sentences
):
    """Analyze all sentences in a privacy policy."""

    results = []

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue


        category = predict_category(
            model,
            sentence
        )


        risk = get_risk_level(
            category
        )


        results.append(
            {
                "sentence": sentence,
                "category": category,
                "risk": risk
            }
        )


    return results


# =========================================================
# CALCULATE OVERALL RISK
# =========================================================

def calculate_overall_risk(results):
    """Calculate the overall privacy risk score."""

    risk_values = {

        "Low": 25,

        "Medium": 60,

        "High": 90
    }


    if not results:

        return 0, "Low"


    total = 0


    for result in results:

        total += risk_values.get(
            result.get(
                "risk",
                "Medium"
            ),
            60
        )


    score = round(
        total / len(results)
    )


    if score >= 70:

        level = "High"

    elif score >= 40:

        level = "Medium"

    else:

        level = "Low"


    return score, level
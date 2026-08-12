# predictive/ml/grid_search.py

import json
import os
import sys
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import f1_score, accuracy_score, balanced_accuracy_score, roc_auc_score
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE, RandomOverSampler

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main_pro.settings")
import django
django.setup()

from predictive.features.feature_builder import build_features
from predictive.ml.generate_dataset import generate_synthetic_data

MODEL_DIR = "predictive/ml"
MODEL_PATH = os.path.join(MODEL_DIR, "model_optimized.pkl")

def prepare_dataset(minority_ratio=0.2):
    """Charge données réelles + génère données synthétiques + fusionne."""
    real_data = pd.DataFrame(build_features())
    synthetic_data = generate_synthetic_data(300, minority_ratio=minority_ratio)
    df = pd.concat([real_data, synthetic_data], ignore_index=True)
    return df

def balance_dataset(X, y):
    """Équilibre les classes avec SMOTE si possible, sinon fallback ROS."""
    imputer = SimpleImputer(strategy="median")
    X_imputed = imputer.fit_transform(X)

    try:
        smote = SMOTE(random_state=42, k_neighbors=1)
        X_resampled, y_resampled = smote.fit_resample(X_imputed, y)
    except ValueError:
        ros = RandomOverSampler(random_state=42)
        X_resampled, y_resampled = ros.fit_resample(X_imputed, y)

    return X_resampled, y_resampled

def run_grid_search(minority_ratio=0.2):
    df = prepare_dataset(minority_ratio=minority_ratio)
    X = df.drop(columns=["target", "machine_id"], errors="ignore")
    y = df["target"]

    X_resampled, y_resampled = balance_dataset(X, y)

    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled
    )

    rf = RandomForestClassifier(random_state=42)

    param_grid = {
        "n_estimators": [100, 200, 500],
        "max_depth": [None, 8, 20],
        "min_samples_split": [2, 5, 10],
        "class_weight": [None, "balanced", "balanced_subsample"],
    }

    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        scoring="f1",
        cv=5,
        n_jobs=-1,
        verbose=2
    )

    grid_search.fit(X_train, y_train)

    print("Meilleurs paramètres :", grid_search.best_params_)
    print("Meilleur score F1 (CV) :", grid_search.best_score_)


    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)

    print("Accuracy (test) :", accuracy_score(y_test, y_pred))
    print("Balanced Accuracy (test) :", balanced_accuracy_score(y_test, y_pred))
    print("F1 (test) :", f1_score(y_test, y_pred))
    print("ROC-AUC (test) :", roc_auc_score(y_test, best_model.predict_proba(X_test)[:, 1]))

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)
    print("✅ Modèle optimisé sauvegardé dans", MODEL_PATH)

    # Export JSON
    best_params = grid_search.best_params_
    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(os.path.join(MODEL_DIR, "best_params.json"), "w") as f:
        json.dump(best_params, f, indent=4)

    print("✅ Paramètres optimisés sauvegardés dans predictive/ml/best_params.json")

    return best_params

#if __name__ == "__main__":
    #run_grid_search(minority_ratio=0.2)

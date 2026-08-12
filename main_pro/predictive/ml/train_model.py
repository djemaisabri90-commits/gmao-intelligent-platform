"""
import json
import os
import sys
import joblib
import pandas as pd
import numpy as np
from django.utils import timezone
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    balanced_accuracy_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from imblearn.over_sampling import SMOTE, RandomOverSampler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main_pro.settings")
import django
django.setup()

from predictive.models import TrainingLog
from predictive.features.feature_builder import build_features
from predictive.ml.generate_dataset import generate_synthetic_data


def sanitize_for_json(obj):
    import numpy as np
    if isinstance(obj, dict):
        return {str(k): sanitize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize_for_json(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.ndarray,)):
        return obj.tolist()
    return obj


MODEL_DIR = "predictive/ml"
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
FEATURES_PATH = os.path.join(MODEL_DIR, "features.pkl")


def prepare_dataset(minority_ratio=0.2):
    #Charge données réelles + génère données synthétiques + fusionne.
    print("📊 Chargement données réelles...")
    real_data = pd.DataFrame(build_features())

    if not real_data.empty:
        print(f"🔍 Audit : {len(real_data)} lignes réelles détectées.")
        if "target" in real_data.columns:
            print("🎯 Distribution Target (Réel) :\n", real_data["target"].value_counts())
    else:
        print("⚠️ Attention : build_features() a renvoyé un set vide !")

    print("🧪 Génération données simulées...")
    synthetic_data = generate_synthetic_data(1000, minority_ratio=minority_ratio)

    df = pd.concat([real_data, synthetic_data], ignore_index=True)
    print(f"Dataset total: {len(df)} lignes")
    print(df["target"].value_counts())
    return df


def normalize_report(report):
    #Nettoie le rapport scikit-learn pour être aligné avec le frontend
    return {
        "accuracy": report.get("accuracy"),
        "macro avg": report.get("macro avg"),
        "weighted avg": report.get("weighted avg"),
        "classes": {k: v for k, v in report.items() if k.isdigit()},
    }


def evaluate_with_validation(df):
    Compare ROS vs SMOTE sur un jeu de validation externe avec plusieurs algorithmes
    X = df.drop(columns=["target", "machine_id"], errors="ignore")
    y = df["target"]

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    imputer = SimpleImputer(strategy="median")
    X_train_imputed = imputer.fit_transform(X_train)
    X_val_imputed = imputer.transform(X_val)

    results = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    algorithms = {
        "RandomForest": RandomForestClassifier(
            n_estimators=200, max_depth=8, class_weight="balanced", random_state=42
        ),
        "LogisticRegression": LogisticRegression(
            max_iter=1000, class_weight="balanced", random_state=42
        ),
        "SVM": SVC(class_weight="balanced", random_state=42)
    }

    # Variante 1 : ROS
    ros = RandomOverSampler(random_state=42)
    X_ros, y_ros = ros.fit_resample(X_train_imputed, y_train)

    for name, model in algorithms.items():
        cv_scores = cross_val_score(model, X_ros, y_ros, cv=cv, scoring="f1")
        model.fit(X_ros, y_ros)
        y_pred = model.predict(X_val_imputed)
        results[f"ROS_{name}"] = {
            "report": normalize_report(classification_report(y_val, y_pred, output_dict=True)),
            "cv_scores": cv_scores.tolist(),
            "cv_mean": cv_scores.mean(),
        }

    # Variante 2 : SMOTE
    try:
        smote = SMOTE(random_state=42, k_neighbors=5)
        X_smote, y_smote = smote.fit_resample(X_train_imputed, y_train)
    except ValueError:
        X_smote, y_smote = ros.fit_resample(X_train_imputed, y_train)

    for name, model in algorithms.items():
        cv_scores = cross_val_score(model, X_smote, y_smote, cv=cv, scoring="f1")
        model.fit(X_smote, y_smote)
        y_pred = model.predict(X_val_imputed)
        results[f"SMOTE_{name}"] = {
            "report": normalize_report(classification_report(y_val, y_pred, output_dict=True)),
            "cv_scores": cv_scores.tolist(),
            "cv_mean": cv_scores.mean(),
        }

    return results


def balance_dataset(X, y):
    #Équilibre les classes avec SMOTE si possible, sinon fallback ROS.
    if y.nunique() < 2:
        raise ValueError("Dataset non exploitable (target unique)")
    if y.value_counts().min() < 2:
        raise ValueError("Classe minoritaire trop petite pour SMOTE")

    imputer = SimpleImputer(strategy="median")
    X_imputed = imputer.fit_transform(X)

    try:
        smote = SMOTE(random_state=42, k_neighbors=5)
        return smote.fit_resample(X_imputed, y)
    except ValueError:
        print("⚠️ Fallback ROS")
        ros = RandomOverSampler(random_state=42)
        return ros.fit_resample(X_imputed, y)


def load_best_params():
    path = os.path.join(MODEL_DIR, "best_params.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {
        "n_estimators": 200,
        "max_depth": 8,
        "class_weight": "balanced",
        "random_state": 42,
    }


def train(user=None, minority_ratio=0.2):
    df = prepare_dataset(minority_ratio=minority_ratio)
    X = df.drop(columns=["target", "machine_id"], errors="ignore")
    y = df["target"]

    validation_results = evaluate_with_validation(df)
    print("📊 Résultats validation externe:")
    for method, result in validation_results.items():
        acc = result["report"].get("accuracy", 0)
        f1_val = result["report"]["weighted avg"]["f1-score"]
        print(method, "→ Accuracy:", round(acc, 3), "F1:", round(f1_val, 3))

    X_train_raw, X_test, y_train_raw, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    initial_distribution = df["target"].value_counts().to_dict()
    X_train_resampled, y_train_resampled = balance_dataset(X_train_raw, y_train_raw)

    best_params = load_best_params()
    model = RandomForestClassifier(**best_params)
    imputer = SimpleImputer(strategy="median")
    X_test_imputed = imputer.fit_transform(X_test)

    print("🧠 Training RandomForest...")
    model.fit(X_train_resampled, y_train_resampled)
    y_pred = model.predict(X_test_imputed)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1_w = f1_score(y_test, y_pred, average="weighted", zero_division=0)
    f1_macro = f1_score(y_test, y_pred, average="macro", zero_division=0)
    balanced_acc = balanced_accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred).tolist()

    # Logistic Regression
    log_reg = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
    log_reg.fit(X_train_resampled, y_train_resampled)
    y_pred_lr = log_reg.predict(X_test_imputed)
    report_lr = classification_report(y_test, y_pred_lr, output_dict=True)
    validation_results["LogisticRegression"] = {
        "report": normalize_report(report_lr),
        "cv_scores": cross_val_score(log_reg, X_train_resampled, y_train_resampled, cv=5, scoring="f1").tolist(),
        "cv_meanParfait Sabri 👌 — voici une version **régénérée et complète** de ton fichier, corrigée pour intégrer correctement **RandomForest, LogisticRegression et SVM** dans le pipeline, avec ROS et SMOTE, et sans fautes de placement de variables.

"""
import json
import os
import sys
import joblib
import pandas as pd
import numpy as np
from django.utils import timezone
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    balanced_accuracy_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from imblearn.over_sampling import SMOTE, RandomOverSampler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main_pro.settings")
import django
django.setup()

from predictive.models import TrainingLog
from predictive.features.feature_builder import build_features
from predictive.ml.generate_dataset import generate_synthetic_data


def sanitize_for_json(obj):
    import numpy as np
    if isinstance(obj, dict):
        return {str(k): sanitize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize_for_json(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.ndarray,)):
        return obj.tolist()
    return obj


MODEL_DIR = "predictive/ml"
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
FEATURES_PATH = os.path.join(MODEL_DIR, "features.pkl")


def prepare_dataset(minority_ratio=0.2):
    """Charge données réelles + génère données synthétiques + fusionne."""
    print("📊 Chargement données réelles...")
    real_data = pd.DataFrame(build_features())

    if not real_data.empty:
        print(f"🔍 Audit : {len(real_data)} lignes réelles détectées.")
        if "target" in real_data.columns:
            print("🎯 Distribution Target (Réel) :\n", real_data["target"].value_counts())
    else:
        print("⚠️ Attention : build_features() a renvoyé un set vide !")

    print("🧪 Génération données simulées...")
    synthetic_data = generate_synthetic_data(1000, minority_ratio=minority_ratio)

    df = pd.concat([real_data, synthetic_data], ignore_index=True)
    print(f"Dataset total: {len(df)} lignes")
    print(df["target"].value_counts())
    return df


def normalize_report(report):
    """Nettoie le rapport scikit-learn pour être aligné avec le frontend."""
    return {
        "accuracy": report.get("accuracy"),
        "macro avg": report.get("macro avg"),
        "weighted avg": report.get("weighted avg"),
        "classes": {k: v for k, v in report.items() if k.isdigit()},
    }


def evaluate_with_validation(df):
    """Compare ROS vs SMOTE sur un jeu de validation externe avec plusieurs algorithmes."""
    X = df.drop(columns=["target", "machine_id"], errors="ignore")
    y = df["target"]

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    imputer = SimpleImputer(strategy="median")
    X_train_imputed = imputer.fit_transform(X_train)
    X_val_imputed = imputer.transform(X_val)

    results = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    algorithms = {
        "RandomForest": RandomForestClassifier(
            n_estimators=200, max_depth=8, class_weight="balanced", random_state=42
        ),
        "LogisticRegression": LogisticRegression(
            max_iter=1000, class_weight="balanced", random_state=42
        ),
        "SVM": SVC(class_weight="balanced", random_state=42)
    }

    # Variante 1 : ROS
    ros = RandomOverSampler(random_state=42)
    X_ros, y_ros = ros.fit_resample(X_train_imputed, y_train)

    for name, model in algorithms.items():
        cv_scores = cross_val_score(model, X_ros, y_ros, cv=cv, scoring="f1")
        model.fit(X_ros, y_ros)
        y_pred = model.predict(X_val_imputed)
        results[f"ROS_{name}"] = {
            "report": normalize_report(classification_report(y_val, y_pred, output_dict=True)),
            "cv_scores": cv_scores.tolist(),
            "cv_mean": cv_scores.mean(),
        }

    # Variante 2 : SMOTE
    try:
        smote = SMOTE(random_state=42, k_neighbors=5)
        X_smote, y_smote = smote.fit_resample(X_train_imputed, y_train)
    except ValueError:
        X_smote, y_smote = ros.fit_resample(X_train_imputed, y_train)

    for name, model in algorithms.items():
        cv_scores = cross_val_score(model, X_smote, y_smote, cv=cv, scoring="f1")
        model.fit(X_smote, y_smote)
        y_pred = model.predict(X_val_imputed)
        results[f"SMOTE_{name}"] = {
            "report": normalize_report(classification_report(y_val, y_pred, output_dict=True)),
            "cv_scores": cv_scores.tolist(),
            "cv_mean": cv_scores.mean(),
        }

    return results


def balance_dataset(X, y):
    """Équilibre les classes avec SMOTE si possible, sinon fallback ROS."""
    if y.nunique() < 2:
        raise ValueError("Dataset non exploitable (target unique)")
    if y.value_counts().min() < 2:
        raise ValueError("Classe minoritaire trop petite pour SMOTE")

    imputer = SimpleImputer(strategy="median")
    X_imputed = imputer.fit_transform(X)

    try:
        smote = SMOTE(random_state=42, k_neighbors=5)
        return smote.fit_resample(X_imputed, y)
    except ValueError:
        print("⚠️ Fallback ROS")
        ros = RandomOverSampler(random_state=42)
        return ros.fit_resample(X_imputed, y)


def load_best_params():
    path = os.path.join(MODEL_DIR, "best_params.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {
        "n_estimators": 200,
        "max_depth": 8,
        "class_weight": "balanced",
        "random_state": 42,
    }


def train(user=None, minority_ratio=0.2):
    df = prepare_dataset(minority_ratio=minority_ratio)
    X = df.drop(columns=["target", "machine_id"], errors="ignore")
    y = df["target"]

    validation_results = evaluate_with_validation(df)
    print("📊 Résultats validation externe:")
    for method, result in validation_results.items():
        acc = result["report"].get("accuracy", 0)
        f1_val = result["report"]["weighted avg"]["f1-score"]
        print(method, "→ Accuracy:", round(acc, 3), "F1:", round(f1_val, 3))

    X_train_raw, X_test, y_train_raw, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    initial_distribution = df["target"].value_counts().to_dict()
    X_train_resampled, y_train_resampled = balance_dataset(X_train_raw, y_train_raw)

    best_params = load_best_params()
    model = RandomForestClassifier(**best_params)
    imputer = SimpleImputer(strategy="median")
    X_test_imputed = imputer.fit_transform(X_test)

    print("🧠 Training RandomForest...")
    model.fit(X_train_resampled, y_train_resampled)
    y_pred = model.predict(X_test_imputed)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1_w = f1_score(y_test, y_pred, average="weighted", zero_division=0)
    f1_macro = f1_score(y_test, y_pred, average="macro", zero_division=0)
    balanced_acc = balanced_accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred).tolist()

    # Logistic Regression
    log_reg = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
    log_reg.fit(X_train_resampled, y_train_resampled)
    y_pred_lr = log_reg.predict(X_test_imputed)
    report_lr = classification_report(y_test, y_pred_lr, output_dict=True)
    validation_results["LogisticRegression"] = {
        "report": normalize_report(report_lr),
        "cv_scores": cross_val_score(log_reg, X_train_resampled, y_train_resampled, cv=5, scoring="f1").tolist(),
                "cv_mean": cross_val_score(log_reg, X_train_resampled, y_train_resampled, cv=5, scoring="f1").mean(),
    }

    # SVM
    svm_clf = SVC(class_weight="balanced", random_state=42)
    svm_clf.fit(X_train_resampled, y_train_resampled)
    y_pred_svm = svm_clf.predict(X_test_imputed)
    report_svm = classification_report(y_test, y_pred_svm, output_dict=True)
    validation_results["SVM"] = {
        "report": normalize_report(report_svm),
        "cv_scores": cross_val_score(svm_clf, X_train_resampled, y_train_resampled, cv=5, scoring="f1").tolist(),
        "cv_mean": cross_val_score(svm_clf, X_train_resampled, y_train_resampled, cv=5, scoring="f1").mean(),
    }

    # Sauvegarde en base
    TrainingLog.objects.create(
        dataset_size=len(df),
        class_distribution=initial_distribution,
        balanced_distribution=sanitize_for_json(dict(pd.Series(y_train_resampled).value_counts())),
        accuracy=float(round(acc, 3)),
        precision=float(round(prec, 3)),
        recall=float(round(rec, 3)),
        f1_score=float(round(f1_w, 3)),
        macro_f1=float(round(f1_macro, 3)),
        balanced_accuracy=float(round(balanced_acc, 3)),
        user=user,
        success=True,
        validation_metrics=sanitize_for_json(validation_results),
        confusion_matrix=sanitize_for_json(cm),
        minority_ratio=float(minority_ratio),
        hyperparameters=sanitize_for_json(best_params),
    )

    print("✅ Modèle sauvegardé dans", MODEL_PATH)

    return {
        "success": True,
        "dataset_size": int(len(df)),
        "class_distribution": sanitize_for_json(initial_distribution),
        "balanced_distribution": sanitize_for_json(dict(pd.Series(y_train_resampled).value_counts())),
        "accuracy": float(round(acc, 3)),
        "precision": float(round(prec, 3)),
        "recall": float(round(rec, 3)),
        "f1_score": float(round(f1_w, 3)),
        "macro_f1": float(round(f1_macro, 3)),
        "balanced_accuracy": float(round(balanced_acc, 3)),
        "confusion_matrix": sanitize_for_json(cm),
        "validation_metrics": sanitize_for_json(validation_results),
        "hyperparameters": sanitize_for_json(best_params),
        "user": {
            "id": int(user.id) if user else None,
            "username": user.username if user else None,
        },
        "trained_at": timezone.now().isoformat(),
    }

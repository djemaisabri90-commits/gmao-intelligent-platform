# predictive/ml/predict.py

import joblib
import os
import numpy as np
from datetime import timedelta, date
from predictive.features.feature_builder import build_features_for_machine
from maintenance.models import Machine

MODEL_PATH = "predictive/ml/model.pkl"

def predict_machine(machine: Machine):
    if not os.path.exists(MODEL_PATH):
        return {"error": "Modèle non entraîné"}

    model = joblib.load(MODEL_PATH)

    # 1. Charger la liste des colonnes utilisée lors de l'entraînement
    FEATURES_PATH = "predictive/ml/features.pkl"
    model_columns = joblib.load(FEATURES_PATH)

    # 2. Extraire les caractéristiques de la machine
    features = build_features_for_machine(machine)

    # 3. Aligner les données dans l'ordre strict du modèle
    X_input = []
    for col in model_columns:
        # On récupère la valeur, si absente on met 0
        X_input.append(features.get(col, 0))

    # 4. Prédiction (avec la probabilité de la classe 1)
    risk = model.predict_proba([X_input])[0][1]

    # 🔮 estimation simple de la date de panne
    # règle heuristique : plus le risque est élevé, plus la panne est proche
    days_offset = max(1, int((1 - risk) * 30)) # Minimum 1 jour pour éviter le 0
    predicted_date = date.today() + timedelta(days=days_offset)

    return {
        "id": machine.id,
        "nom": machine.nom,
        "etat": machine.etat,
        "risk": float(np.round(risk, 3)),  # ex: 0.732 arrondissement 3 chiffres apres virgule
        "predicted_failure_date": predicted_date.isoformat(),
    }

def predict_all_machines():
    results = []
    for machine in Machine.objects.all():
        results.append(predict_machine(machine))
    return results

# predictive/urls.py

from django.urls import path
from predictive.views import (
    export_log_csv, export_log_json, export_log_xlsx, features_dataset,
    latest_train_history, list_features,
    machine_risk_list, machine_risk_detail,
    train_ai_model, train_history, train_history_detail)

# run_ai, ... ancien modèle

urlpatterns = [
    
    # 🔍 liste des risques pour toutes les machines
    path("machine-risk/", machine_risk_list, name="machine-risk-list"),

    # 🎯 risque pour une machine spécifique
    path("machine-risk/<int:machine_id>/", machine_risk_detail, name="machine-risk-detail"),

    # 🤖 exécution IA (admin/expert)
    #path("run/", run_ai, name="run-ai"), ... ancien modèle

    # entrainer depuis UI
    path("train/", train_ai_model, name="train-ai-model"),

    # stocker log en base = historique
    path("train-history/", train_history, name="train-history"),

    # lire features.pkl return list colonnes utilisées à l’entraînement
    path("features/", list_features, name="list_features"),

    path("features_data/", features_dataset, name="data_features"),

    # dernier log d'entraînement
    path("train-history/latest/", latest_train_history, name="latest_train_history"),

    # détailler un log par version
    path("train-history/<int:version>/", train_history_detail),

    # Exporter métriques
    path("export/<int:version>/json/", export_log_json, name="export_log_json"),
    path("export/<int:version>/csv/", export_log_csv, name="export_log_csv"),
    path("export/<int:version>/xlsx/", export_log_xlsx, name="export_log_xlsx"),
]


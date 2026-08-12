from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, JsonResponse
import csv, json, openpyxl
from predictive.ml.train_model import train
from predictive.models import TrainingLog
from predictive.serializers import TrainingLogSerializer
#from predictive.services.ai_services import generate_ai_workorders
from maintenance.models import Machine
from predictive.ml.predict import predict_machine, predict_all_machines


import os
import joblib
"""
#ancien modele
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def run_ai(request):
    # 🔒 accès réservé admin
    if request.user.role not in ["admin", "expert"]:
        return Response({"error": "Accès refusé"}, status=403)

    results = generate_ai_workorders()

    return Response({
        "message": "IA exécutée",
        "created_workorders": results
    })

#ancien modele == réutilisable
@api_view(["GET"])
def machine_risk_list(request):
    results = []

    for machine in Machine.objects.all():
        risk = predict_machine(machine)

        results.append({
            "id": machine.id,
            "nom": machine.nom,
            "etat": machine.etat,  # dérivé des WorkOrders
            "risk": risk
        })

    return Response(results)

#ancien modele == réutilisable
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def machine_risk_detail(request, machine_id):
    try:
        machine = Machine.objects.get(pk=machine_id)
    except Machine.DoesNotExist:
        return Response({"error": "Machine introuvable"}, status=404)

    risk = predict_machine(machine)

    return Response({
        "id": machine.id,
        "nom": machine.nom,
        "etat": machine.etat,  # dérivé des WorkOrders
        "risk": risk
    })
"""
# New
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def train_ai_model(request):
    # 🔒 accès réservé admin OU expert
    if request.user.role not in ["admin", "expert"]:
        return Response({"error": "Accès refusé"}, status=403)

    # scratch
    #scratch = request.GET.get("scratch", "false").lower() == "true"
    user = request.user if request.user.is_authenticated else None
    # ✅ lire scratch depuis query ou body
    scratch = (
        request.GET.get("scratch", None) or request.data.get("scratch", False)
    )
    scratch = str(scratch).lower() == "true"

    # ✅ lire minority_ratio depuis body (par défaut 0.2)
    try:
        minority_ratio = float(request.data.get("minority_ratio", 0.2))
    except (TypeError, ValueError):
        minority_ratio = 0.2

    if scratch:
        # 🚀 Pipeline complet depuis zéro
        result = train(user=user, minority_ratio=minority_ratio)
        if not result.get("success", False):
            return Response({"error": result.get("error", "Erreur inconnue")}, status=500)
        return Response({
            "message": "✅ Modèle réentraîné depuis zéro avec succès",
            "log": result
        }, status=200)
    else:
        # 🔄 Ancienne logique (réentraînement basé sur logs existants)
        # Ici tu peux garder ton code actuel ou simplifier
        #result = train(user=request.user)
        
        result = train(user=user, minority_ratio=minority_ratio)

        if not result.get("success", False):
            return Response({"error": result.get("error", "Erreur inconnue")}, status=500)

        return Response({
            "message": "✅ Modèle réentraîné avec succès(minority_ratio={minority_ratio})",
            "log": result
        }, status=200)

# New
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def train_history(request):
    if request.user.role not in ["admin", "expert"]:
        return Response({"error": "Accès refusé"}, status=403)

    logs = TrainingLog.objects.all().order_by("-trained_at")[:10]  # derniers 10 entraînements
    """
    results = [
        {
            "trained_at": log.trained_at,
            "dataset_size": log.dataset_size,
            "class_distribution": log.class_distribution,
            "accuracy": log.accuracy,
            "precision": log.precision,
            "recall": log.recall,
            "f1_score": log.f1_score,
        }
        for log in logs
    ]

    return Response(results)
    """
    serializer = TrainingLogSerializer(logs, many=True)
    return Response(serializer.data)



FEATURES_PATH = "predictive/ml/features.pkl"

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_features(request):
    if not os.path.exists(FEATURES_PATH):
        return Response({"error": "Aucune feature sauvegardée. Lancez un entraînement."}, status=404)

    feature_names = joblib.load(FEATURES_PATH)
    return Response({"features": feature_names})

from predictive.features.feature_builder import build_features

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def features_dataset(request):
    dataset = build_features()
    return Response(dataset)  # DRF sérialise automatiquement en JSON


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def latest_train_history(request):
    if request.user.role not in ["admin", "expert"]:
        return Response({"error": "Accès refusé"}, status=403)

    log = TrainingLog.objects.all().order_by("-trained_at").first()
    if not log:
        return Response({"error": "Aucun entraînement trouvé"}, status=404)

    serializer = TrainingLogSerializer(log)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def train_history_detail(request, version):
    if request.user.role not in ["admin", "expert"]:
        return Response({"error": "Accès refusé"}, status=403)

    try:
        log = TrainingLog.objects.get(model_version=version)
    except TrainingLog.DoesNotExist:
        return Response({"error": "Log introuvable"}, status=404)

    serializer = TrainingLogSerializer(log)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_log_json(request, version):
    if request.user.role not in ["admin", "expert"]:
        return Response({"error": "Accès refusé"}, status=403)
    try:
        log = TrainingLog.objects.get(model_version=version)
        data = {
            "model_version": log.model_version,
            "trained_at": log.trained_at.strftime("%d/%m/%Y %H:%M"),
            "user": log.user.username if log.user else None,
            "accuracy": log.accuracy,
            "precision": log.precision,
            "recall": log.recall,
            "f1_score": log.f1_score,
            "dataset_size": log.dataset_size,
            "status": "Succès" if log.success else "Échec",
        }
        return JsonResponse(data, safe=False)
    except TrainingLog.DoesNotExist:
        return JsonResponse({"error": "Log introuvable"}, status=404)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_log_csv(request, version):
    if request.user.role not in ["admin", "expert"]:
        return Response({"error": "Accès refusé"}, status=403)
    try:
        log = TrainingLog.objects.get(model_version=version)
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="training_log_v{version}.csv"'
        writer = csv.writer(response)
        writer.writerow(["Model Version","Trained At","User","Accuracy","Precision","Recall","F1 Score","Dataset Size","Status"])
        writer.writerow([
            log.model_version,
            log.trained_at.strftime("%d/%m/%Y %H:%M"),
            log.user.username if log.user else None,
            log.accuracy,
            log.precision,
            log.recall,
            log.f1_score,
            log.dataset_size,
            "Succès" if log.success else "Échec",
        ])
        return response
    except TrainingLog.DoesNotExist:
        return JsonResponse({"error": "Log introuvable"}, status=404)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_log_xlsx(request, version):
    if request.user.role not in ["admin", "expert"]:
        return Response({"error": "Accès refusé"}, status=403)
    try:
        log = TrainingLog.objects.get(model_version=version)

        # Créer un workbook Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Training Log"

        # En-têtes
        headers = ["Model Version", "Trained At", "User", "Accuracy", "Precision", "Recall", "F1 Score", "Dataset Size", "Status"]
        ws.append(headers)

        # Données
        ws.append([
            log.model_version,
            log.trained_at.strftime("%d/%m/%Y %H:%M"),
            log.user.username if log.user else None,
            log.accuracy,
            log.precision,
            log.recall,
            log.f1_score,
            log.dataset_size,
            "Succès" if log.success else "Échec",
        ])

        # Réponse HTTP avec fichier XLSX
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="log_v{version}.xlsx"'
        wb.save(response)
        return response

    except TrainingLog.DoesNotExist:
        return JsonResponse({"error": "Log introuvable"}, status=404)


# 🔮 Risque pour toutes les machines
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def machine_risk_list(request):
    if request.user.role not in ["admin", "expert"]:
        return Response({"error": "Accès refusé"}, status=403)
    
    results = predict_all_machines()
    return Response(results)

# 🔮 Risque pour une machine spécifique
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def machine_risk_detail(request, machine_id: int):
    if request.user.role not in ["admin", "expert"]:
        return Response({"error": "Accès refusé"}, status=403)
    
    try:
        machine = Machine.objects.get(pk=machine_id)
    except Machine.DoesNotExist:
        return Response({"error": "Machine introuvable"}, status=404)

    result = predict_machine(machine)
    return Response(result)
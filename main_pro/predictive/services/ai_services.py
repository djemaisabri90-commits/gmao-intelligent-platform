import sys
import os
import django

# lancement d'entraînement :
# python -m predictive.ml.train_model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main_pro.settings")
django.setup()

from maintenance.models import Machine, WorkOrder
from predictive.ml.predict import predict_machine
from django.utils import timezone

THRESHOLD = 0.8  # 🔥 seuil critique

def generate_ai_workorders():
    created = []

    for machine in Machine.objects.all():
        risk = predict_machine(machine)

        if risk >= THRESHOLD:
            # ⚠️ éviter duplication : vérifier WorkOrders en cours ou en attente
            exists = WorkOrder.objects.filter(
                machine=machine
            ).filter(
                interventions__etat__in=["en_attente", "en_cours", "termine"]
            ).exists()

            if exists:
                continue

            wo = WorkOrder.objects.create(
                machine=machine,
                type="predictive",
                priorite="high",
                description=f"⚠️ IA: risque de panne élevé ({risk*100:.0f}%)",
                date_creation=timezone.now(),
            )

            created.append({
                "machine": machine.nom,
                "risk": risk,
                "workorder_id": wo.id
            })

    return created

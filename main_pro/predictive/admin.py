from django.contrib import admin, messages
from django.utils.html import format_html
import csv
import openpyxl
import requests
import json
from django.http import HttpResponse
from predictive.models import TrainingLog
from django.conf import settings
from django.urls import path
from django.shortcuts import redirect

@admin.register(TrainingLog)
class TrainingLogAdmin(admin.ModelAdmin):
    list_display = ("model_version", "trained_at", "user", "accuracy", "precision", "recall", "f1_score", "status_badge")
    list_filter = ("success", "trained_at", "user")
    search_fields = ("user__username",)
    actions = ["retrain_model", "export_last_10", "export_last_10_csv", "export_last_10_xlsx"]

    def status_badge(self, obj):
        if obj.success:
            return format_html('<span style="color: white; background: green; padding: 2px 6px; border-radius: 4px;">SUCCESS</span>')
        return format_html('<span style="color: white; background: red; padding: 2px 6px; border-radius: 4px;">FAILED</span>')

    status_badge.short_description = "Status"

    # url scratch
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
            "retrain-from-scratch/",
            self.admin_site.admin_view(self.retrain_from_scratch),
            name="traininglog-retrain-from-scratch",
            ),
            #path("<int:log_id>retrain-from-scratch/", self.admin_site.admin_view(self.retrain_from_scratch), name="retrain-from-scratch"),
        ]
        return custom_urls + urls
    # on doit supprimer queryset de signature / ajouter log_id
    def retrain_from_scratch(self, request, log_id=None):
        """Nouvelle action : relance le pipeline complet avec token + headers"""
        try:
            token = "260fb4baef0f1c2cd397fa9301212bfa7f3e4caf"  # ⚠️ à remplacer par ton vrai token
            headers = {"Authorization": f"Token {token}"}
            response = requests.post("http://127.0.0.1:8000/predictive/train/?scratch=true", headers=headers)
            if response.status_code == 200:
                messages.success(request, "✅ Modèle réentraîné depuis zéro avec succès")
            else:
                messages.error(request, f"❌ Erreur lors du réentraînement depuis zéro : {response.status_code}")
        except Exception as e:
            messages.error(request, f"❌ Exception : {str(e)}")
        return redirect("..")  # retour à la liste admin
    #retrain_from_scratch.short_description = "Réentraîner le modèle depuis zéro"

    def retrain_model(self, request, queryset):
        try:
            # ⚠️ URL locale de ton API Django
            # headers = {"Authorization": f"Token {settings.TRAIN_API_TOKEN}"}
            token = "260fb4baef0f1c2cd397fa9301212bfa7f3e4caf"  # ⚠️ à remplacer par ton vrai token
            headers = {"Authorization": f"Token {token}"}
            response = requests.post("http://127.0.0.1:8000/predictive/train/", headers=headers)
            if response.status_code == 200:
                messages.success(request, "✅ Modèle réentraîné avec succès")
            else:
                messages.error(request, f"❌ Erreur lors du réentraînement : {response.status_code}")
        except Exception as e:
            messages.error(request, f"❌ Exception : {str(e)}")

    retrain_model.short_description = "Réentraîner le modèle maintenant" 

    
    def export_last_10(self, request, queryset):
        try:
            #headers = {"Authorization": f"Token {settings.TRAIN_API_TOKEN}"}
            token = "260fb4baef0f1c2cd397fa9301212bfa7f3e4caf"  # ⚠️ à remplacer par ton vrai token
            headers = {"Authorization": f"Token {token}"}
            response = requests.get("http://127.0.0.1:8000/predictive/train-history/", headers=headers)
            if response.status_code == 200:
                data = response.json()[:10]  # 🔧 limiter aux 10 derniers

                # 🔧 Adapter validation_metrics pour ne garder que les métriques clés
                for log in data:
                    if "validation_metrics" in log and log["validation_metrics"]:
                        vm = log["validation_metrics"]
                        log["validation_metrics"] = {
                            method: {
                            "accuracy": round(vm[method]["accuracy"], 3),
                            "f1_score": round(vm[method]["weighted avg"]["f1-score"], 3)
                            }
                        for method in vm
                        }

                response_json = json.dumps(data, indent=4)
                return HttpResponse(
                    response_json,
                    content_type="application/json",
                    headers={"Content-Disposition": 'attachment; filename="training_logs.json"'}
                )
            else:
                messages.error(request, f"❌ Erreur lors de l’export : {response.status_code}")
        except Exception as e:
            messages.error(request, f"❌ Exception : {str(e)}")
    export_last_10.short_description = "Exporter les 10 derniers en JSON"
    
    def view_latest_model(self, request, queryset):
        try:
            response = requests.get("http://127.0.0.1:8000/predictive/train-history/latest/")
            if response.status_code == 200:
                latest = response.json()
                messages.info(
                    request,
                    f"📊 Dernier modèle v{latest['model_version']} — "
                    f"Accuracy: {latest['accuracy']} | "
                    f"Precision: {latest['precision']} | "
                    f"Recall: {latest['recall']} | "
                    f"F1: {latest['f1_score']} | "
                    f"Dataset: {latest['dataset_size']}"
                )
            else:
                messages.error(request, f"❌ Erreur lors de la récupération : {response.status_code}")
        except Exception as e:
            messages.error(request, f"❌ Exception : {str(e)}")
    view_latest_model.short_description = "Voir dernier modèle"

    def export_last_10_csv(self, request, queryset):
        try:
            headers = {"Authorization": f"Token {settings.TRAIN_API_TOKEN}"}
            response = requests.get("http://127.0.0.1:8000/predictive/train-history/", headers=headers)
            if response.status_code == 200:
                data = response.json()[:10]
                response_csv = HttpResponse(content_type="text/csv")
                response_csv["Content-Disposition"] = 'attachment; filename="training_logs.csv"'
                writer = csv.writer(response_csv)
                # En-têtes
                writer.writerow(["Model Version", "Trained At", "User", "Accuracy", "Precision", "Recall", "F1 Score", "Dataset Size", "Status"])
                # Lignes
                for log in data:
                    writer.writerow([
                        log.get("model_version"),
                        log.get("trained_at"),
                        log.get("user"),
                        log.get("accuracy"),
                        log.get("precision"),
                        log.get("recall"),
                        log.get("f1_score"),
                        log.get("dataset_size"),
                        log.get("status"),
                    ])
                return response_csv
            else:
                messages.error(request, f"❌ Erreur lors de l’export CSV : {response.status_code}")
        except Exception as e:
            messages.error(request, f"❌ Exception : {str(e)}")
    export_last_10_csv.short_description = "Exporter les 10 derniers en CSV"

    def export_last_10_xlsx(self, request, queryset):
        try:
            headers = {"Authorization": f"Token {settings.TRAIN_API_TOKEN}"}
            response = requests.get("http://127.0.0.1:8000/predictive/train-history/", headers=headers)
            if response.status_code == 200:
                data = response.json()[:10]

                # Créer un workbook Excel
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Training Logs"

                # En-têtes
                headers_row = ["Model Version", "Trained At", "User", "Accuracy", "Precision", "Recall", "F1 Score", "Dataset Size", "Status"]
                ws.append(headers_row)

                # Données
                for log in data:
                    ws.append([
                        log.get("model_version"),
                        log.get("trained_at"),
                        log.get("user"),
                        log.get("accuracy"),
                        log.get("precision"),
                        log.get("recall"),
                        log.get("f1_score"),
                        log.get("dataset_size"),
                        log.get("status"),
                    ])

                # Réponse HTTP avec fichier XLSX
                response_xlsx = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                response_xlsx["Content-Disposition"] = 'attachment; filename="training_logs.xlsx"'
                wb.save(response_xlsx)
                return response_xlsx
            else:
                messages.error(request, f"❌ Erreur lors de l’export XLSX : {response.status_code}")
        except Exception as e:
            messages.error(request, f"❌ Exception : {str(e)}")
    export_last_10_xlsx.short_description = "Exporter les 10 derniers en Excel (XLSX)"

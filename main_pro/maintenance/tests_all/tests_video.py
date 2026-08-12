"""
ceci la dernière étape de la phase de test
j'ai testé les endpoints pour la prédiction et le reporting(Deux applications au dessous de l'application mère maintenance)
pour un test complet pour mon application globale --- maintenance --- j'ai implémenté
---- des tests unitaires pour le bon de travail, la machine, l'intervention, la vidéo, le signal, les permissions, les api's vidéos
J'éspère Madame Monsieur mon travail vous paîra !!! merciii... :)
"""


from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from maintenance.models import Machine, Utilisateur, WorkOrder, Intervention, Video, VideoAnnotation
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime

class VideoCrudTests(TestCase):
    def setUp(self):
        # Créer un utilisateur + authentification
        self.user = User.objects.create_user(username="videouser", password="videopass")
        self.utilisateur = Utilisateur.objects.create(user=self.user, role="support_video")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Créer une machine, un WorkOrder et une Intervention
        self.machine = Machine.objects.create(nom="MachineVideo")
        self.workorder = WorkOrder.objects.create(
            machine=self.machine,
            technicien=self.utilisateur,
            description="WO pour test vidéo",
            type="diagnostic",
            priorite="medium",
            statut="en_attente"
        )
        self.intervention = Intervention.objects.create(
            workorder=self.workorder,
            technicien=self.utilisateur,
            date_debut=datetime.now(),
            actions_realisees="Diagnostic"
        )

        # Fichier vidéo fictif
        self.test_file = SimpleUploadedFile("test.mp4", b"fake video content", content_type="video/mp4")

        # Créer une vidéo
        self.video = Video.objects.create(
            workorder=self.workorder,
            intervention=self.intervention,
            uploaded_by=self.utilisateur,
            titre="Vidéo initiale",
            description="Description initiale",
            url_fichier=self.test_file,
            type_video="diagnostic"
        )

    def test_create_video_via_api(self):
        url = reverse("maintenance:video-list")
        payload = {
            "workorder": self.workorder.id,
            "intervention": self.intervention.id,
            
            "titre": "Nouvelle vidéo",
            "description": "Créée via API",
            "url_fichier": SimpleUploadedFile("new.mp4", b"new content", content_type="video/mp4"),
            "type_video": "preuve"
        }
        response = self.client.post(url, payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Video.objects.count(), 2)
        self.assertEqual(Video.objects.last().uploaded_by, self.utilisateur)

    def test_update_video_via_api(self):
        url = reverse("maintenance:video-detail", args=[self.video.id])
        payload = {"titre": "Vidéo mise à jour"}
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.video.refresh_from_db()
        self.assertEqual(self.video.titre, "Vidéo mise à jour")

    def test_delete_video_via_api(self):
        url = reverse("maintenance:video-detail", args=[self.video.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Video.objects.count(), 0)

    def test_create_video_annotation_via_api(self):
        url = reverse("maintenance:videoannotation-list")
        payload = {
            "video": self.video.id,
            "user": self.utilisateur.id,
            "timestamp": 12.5,
            "commentaire": "Annotation via API"
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VideoAnnotation.objects.count(), 1)

    def test_update_video_annotation_via_api(self):
        annotation = VideoAnnotation.objects.create(
            video=self.video,
            user=self.utilisateur,
            timestamp=5.0,
            commentaire="Ancienne annotation"
        )
        url = reverse("maintenance:videoannotation-detail", args=[annotation.id])
        payload = {"commentaire": "Annotation mise à jour"}
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        annotation.refresh_from_db()
        self.assertEqual(annotation.commentaire, "Annotation mise à jour")

    def test_delete_video_annotation_via_api(self):
        annotation = VideoAnnotation.objects.create(
            video=self.video,
            user=self.utilisateur,
            timestamp=8.0,
            commentaire="Annotation à supprimer"
        )
        url = reverse("maintenance:videoannotation-detail", args=[annotation.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(VideoAnnotation.objects.count(), 0)

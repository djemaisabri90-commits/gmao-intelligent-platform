# maintenance/tests/test_utilisateur.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from maintenance.models import Utilisateur, Categorie

class UtilisateurModelTest(TestCase):
    def setUp(self):
        self.categorie = Categorie.objects.create(
            nom="electrique", description="Maintenance électrique"
        )

    def test_technicien_with_category_is_valid(self):
        user = Utilisateur(username="tech1", role="technicien", categorie=self.categorie)
        # clean() ne doit pas lever d'erreur
        user.clean()

    def test_technicien_without_category_is_invalid(self):
        user = Utilisateur(username="tech2", role="technicien", categorie=None)
        with self.assertRaises(ValidationError):
            user.clean()

    def test_non_technicien_with_category_is_invalid(self):
        user = Utilisateur(username="admin1", role="admin", categorie=self.categorie)
        with self.assertRaises(ValidationError):
            user.clean()

    def test_non_technicien_without_category_is_valid(self):
        user = Utilisateur(username="expert1", role="expert", categorie=None)
        # clean() ne doit pas lever d'erreur
        user.clean()

import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    """Client DRF pour les tests API"""
    return APIClient()

@pytest.fixture
def technicien_user(db):
    """Utilisateur avec rôle technicien"""
    return User.objects.create_user(
        username="tech1",
        password="password123",
        role="technicien"
    )

@pytest.fixture
def machine(db):
    from maintenance.models import Machine
    return Machine.objects.create(nom="Machine Test")

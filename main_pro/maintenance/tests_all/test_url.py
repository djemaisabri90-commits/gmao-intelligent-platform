import pytest
from django.urls import get_resolver
"""
def test_list_all_routes():
    resolver = get_resolver()
    for name, pattern in resolver.reverse_dict.items():
        if isinstance(name, str):  # ignorer les patterns internes
            print(f"{name} -> {pattern[0][0]}")
"""

# maintenance/test_url.py
import pytest
from django.urls import get_resolver

@pytest.mark.django_db
def test_list_all_routes(capfd):
    resolver = get_resolver()
    for name, pattern in resolver.reverse_dict.items():
        if isinstance(name, str):
            print(f"{name} -> {pattern[0][0]}")

    out, _ = capfd.readouterr()

    print("\n--- Liste des routes disponibles ---")
    print(out)

    # ✅ Vérifie les routes maintenance
    assert "intervention-detail" in out
    assert "workorder-detail" in out
    assert "machine-list" in out

    # ✅ Vérifie les routes predictive
    assert "train-ai-model" in out
    assert "machine-risk-detail" in out
    assert "run-ai" in out

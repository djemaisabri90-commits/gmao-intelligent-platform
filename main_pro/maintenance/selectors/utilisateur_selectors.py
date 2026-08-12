"""from maintenance.models import Utilisateur


def get_utilisateurs():
    return Utilisateur.objects.select_related("auth_token")


def get_utilisateur(utilisateur_id):
    return Utilisateur.objects.select_related(
        "auth_token"
        ).filter(id=utilisateur_id).first()
"""

# maintenance/selectors/utilisateur_selectors.py

from maintenance.models import Utilisateur


def get_utilisateurs(with_relations=True):
    """
    Retourne tous les utilisateurs, avec relations préchargées si demandé.
    """
    qs = Utilisateur.objects.all().order_by("username")
    if with_relations:
        qs = qs.select_related("categorie")
    return qs


def get_utilisateur(utilisateur_id, with_relations=True):
    """
    Retourne un utilisateur par ID, avec relations préchargées si demandé.
    """
    qs = Utilisateur.objects.all()
    if with_relations:
        qs = qs.select_related("categorie")
    return qs.filter(id=utilisateur_id).first()

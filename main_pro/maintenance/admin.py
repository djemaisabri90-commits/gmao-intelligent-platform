"""
from django.contrib import admin
from .models import Machine, Signalement, Utilisateur, Categorie, WorkOrder, Intervention, Rapport, Piece, PieceUtilisee, Log, AuditLog

admin.site.register([Machine, Signalement, Utilisateur, Categorie, Intervention, Rapport, Piece, PieceUtilisee, Log, AuditLog])
"""

# maintenance/admin.py

from django.contrib import admin

import csv
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse

from django.core.exceptions import ValidationError
from .models import (
    Machine, Signalement, Utilisateur, Categorie,
    WorkOrder, Intervention, Rapport,
    Piece, PieceUtilisee, Log, AuditLog
)
"""
# ✅ Admin personnalisé pour Utilisateur
@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):



    list_display = ("username", "role", "password", "categorie", "telephone", "must_change_password", "is_active")
    fields = ("username", "role", "password", "categorie", "telephone", "must_change_password", "is_active")
    list_filter = ("role", "categorie", "password")
    search_fields = ("username", "telephone")

# ✅ Admin personnalisé pour Categorie
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("nom", "description")
    search_fields = ("nom",)

# ✅ Enregistrement des autres modèles avec configuration par défaut
admin.site.register([
    Machine, Signalement, WorkOrder, Intervention,
    Rapport, Piece, PieceUtilisee, Log, AuditLog
])

"""

@admin.action(description="Exporter les codes d'activation en CSV")
def export_activation_tokens(modeladmin, request, queryset):
    """
    Action d'administration pour exporter les utilisateurs sélectionnés 
    avec leurs codes d'activation au format CSV. Sécurisée pour les tests pytest.
    """
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="codes_activation_gmao.csv"'
    
    # Gestion du BOM UTF-8 pour la compatibilité avec Excel
    response.write(b'\xef\xbb\xbf')
    
    writer = csv.writer(response)
    writer.writerow(['Identifiant (Username)', 'Nom', 'Prénom', 'Rôle', 'Catégorie', 'Code d\'activation', 'Doit changer de passe'])
    
    for user in queryset:
        # 🛡️ Sécurité Tests : Évite un crash si la catégorie est absente ou si get_nom_display échoue
        categorie_nom = "N/A"
        if getattr(user, 'role', None) == "technicien" and getattr(user, 'categorie', None):
            try:
                categorie_nom = user.categorie.get_nom_display()
            except AttributeError:
                categorie_nom = str(user.categorie)

        # 🛡️ Sécurité Tests : Récupération robuste du libellé du rôle
        role_label = user.get_role_display() if hasattr(user, 'get_role_display') else getattr(user, 'role', 'N/A')
        
        writer.writerow([
            user.username,
            user.last_name,
            user.first_name,
            role_label,
            categorie_nom,
            getattr(user, 'activation_token', ''),
            "Oui" if getattr(user, 'must_change_password', True) else "Non"
        ])
        
    return response


# ✅ UN UNIQUE ADMIN POUR UTILISATEUR (Hérite de UserAdmin pour la sécurité Django)
@admin.register(Utilisateur)
class CustomUserAdmin(UserAdmin):
    # 1. Ajout de l'action d'export CSV
    actions = [export_activation_tokens]
    
    # 2. Colonnes affichées dans la liste des utilisateurs (inclut vos champs métiers)
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'categorie', 'telephone', 'must_change_password', 'activation_token', 'is_active', 'is_staff')
    
    # 3. Filtres latéraux pour trier rapidement
    list_filter = ('role', 'must_change_password', 'is_staff', 'is_superuser', 'categorie')
    
    # 4. Barre de recherche (permet de chercher un ouvrier par son nom, téléphone ou son token)
    search_fields = ('username', 'first_name', 'last_name', 'email', 'telephone', 'activation_token')
    
    # 5. Organisation des formulaires de modification (Détail de l'utilisateur)
    fieldsets = tuple(UserAdmin.fieldsets) + (
        ('Informations Métier GMAO', {
            'fields': ('role', 'categorie', 'telephone'),
        }),
        ('Sécurité & Activation Automatique', {
            'fields': ('must_change_password', 'activation_token'),
        }),
    )
    
    # 6. Organisation du formulaire de création d'un utilisateur
    add_fieldsets = tuple(UserAdmin.add_fieldsets) + (
        ('Informations Métier GMAO', {
            'fields': ('role', 'categorie', 'telephone', 'must_change_password'),
        }),
    )


# ✅ Admin personnalisé pour Categorie
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("nom", "description")
    search_fields = ("nom",)


# ✅ Enregistrement des autres modèles avec configuration par défaut
admin.site.register([
    Machine, Signalement, WorkOrder, Intervention,
    Rapport, Piece, PieceUtilisee, Log, AuditLog
])
"""
    class IsExpertOrResponsable(BasePermission):
    
    # Permission : accès réservé aux experts et responsables
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        role = getattr(request.user.utilisateur, "role", None)
        return role in ["expert", "responsable"]

    class IsTechnicien(BasePermission):
    
    # Permission : accès réservé aux techniciens
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        role = getattr(request.user.utilisateur, "role", None)
        return role == "technicien"

    class IsSupportVideo(BasePermission):
    
    # Permission : accès réservé au support vidéo
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        role = getattr(request.user.utilisateur, "role", None)
        return role == "support_video"

# j'ajuste mieux les permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"


class IsTechnicien(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "technicien"


class IsExpert(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "expert"
    

# j'ajuste encore les permissions
# permissions combinées
class IsAdminOrExpert(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ["admin", "expert"]


class IsTechnicienOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ["technicien", "admin"]

class IsOwnerTechnicien(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == "technicien"
            and obj.technicien == request.user
        )
    
#Permissions intelligentes par module
#bonde travail
class WorkOrderPermission(BasePermission):

    def has_permission(self, request, view):
        # accès global
        return request.user.role in ["admin", "technicien", "expert"]

    def has_object_permission(self, request, view, obj):

        # Admin → tout faire
        if request.user.role == "admin":
            return True

        # Technicien → seulement assigné
        if request.user.role == "technicien":
            return obj.assigned_to == request.user

        # Expert → lecture + validation
        if request.user.role == "expert":
            return True

        return False
    
#Intervention
class InterventionPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.role in ["admin", "technicien", "expert"]

    def has_object_permission(self, request, view, obj):

        # Admin → accès total
        if request.user.role == "admin":
            return True

        # Technicien → ses interventions seulement
        if request.user.role == "technicien":
            return obj.technicien == request.user

        # Expert → lecture + validation
        if request.user.role == "expert":
            return True

        return False
    
#Signalement
class SignalementPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.role in ["admin", "technicien", "expert"]

    def has_object_permission(self, request, view, obj):

        # Technicien → ses signalements
        if request.user.role == "technicien":
            return obj.created_by == request.user

        # Admin + Expert → tout voir
        if request.user.role in ["admin", "expert"]:
            return True

        return False
"""
# maintenance/base/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


# =========================================================
# 🔹 BASE GENERIQUE
# =========================================================

class RolePermission(BasePermission):
    """
    Permission générique basée sur les rôles
    """
    allowed_roles = []

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in self.allowed_roles
        )


# =========================================================
# 🔹 ROLES SIMPLES
# =========================================================

class IsAdmin(RolePermission):
    allowed_roles = ["admin"]

class IsOperateur(RolePermission):
    allowed_roles = ["operateur"]

class IsTechnicien(RolePermission):
    allowed_roles = ["technicien"]


class IsExpert(RolePermission):
    allowed_roles = ["expert"]


class IsAdminOrExpert(RolePermission):
    allowed_roles = ["admin", "expert"]

class IsTechnicienOrExpert(RolePermission):
    allowed_roles = ["technicien", "expert"]

class IsTechnicienOrAdmin(RolePermission):
    allowed_roles = ["technicien", "admin"]



# =========================================================
# 📋 WORKORDER PERMISSION
# =========================================================

class WorkOrderPermission(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["admin", "technicien", "expert"]
        )

    def has_object_permission(self, request, view, obj):

        # 🔒 Bloqué si déjà validé
        if obj.date_validation is not None:
            return request.method in SAFE_METHODS

        # 👑 Admin → accès total
        if request.user.role == "admin":
            return True

        # 🔧 Technicien → seulement assigné
        if request.user.role == "technicien":
            return obj.technicien == request.user

        # 🧠 Expert → lecture + validation
        if request.user.role == "expert":
            if request.method in SAFE_METHODS:
                return True

            # autoriser validation (PATCH)
            return view.action == "validate"

        return False


# =========================================================
# 🛠️ INTERVENTION PERMISSION
# =========================================================

class InterventionPermission(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["admin", "technicien", "expert"]
        )

    def has_object_permission(self, request, view, obj):

        # 🔒 Intervention validée → lecture seule
        if obj.statut == "valide":
            return request.method in SAFE_METHODS

        # 👑 Admin → accès total
        if request.user.role == "admin":
            return True

        # 🔧 Technicien → ses interventions uniquement
        if request.user.role == "technicien":
            return obj.technicien == request.user
            


        # 🧠 Expert → lecture + validation
        if request.user.role == "expert":
            if request.method in SAFE_METHODS:
                return True

            return view.action == "validate"

        return False


# =========================================================
# 🚨 SIGNALEMENT PERMISSION
# =========================================================

class SignalementPermission(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["admin", "technicien", "expert", "operateur"]
        )

    def has_object_permission(self, request, view, obj):
        """
        # 👑 Admin → accès total
        if request.user.role == "admin":
            return True
        
        # 👑 Admin + expert → accès total
        if request.user.role in ["admin", "expert"]:
            return True
        """
        # operateur -> signalements
        if request.user.role == "operateur":
            return obj.created_by == request.user
        
        # 🔧 Technicien → ses signalements
        if request.user.role == "technicien":
            return obj.created_by == request.user
        
        # 🧠 Expert → lecture + traitement
        if request.user.role == "expert":
            if request.method in SAFE_METHODS:
                return True

            return view.action in ["traiter"]

        return False


# =========================================================
# 🔹 PERMISSIONS PAR ACTION (OPTIONNEL MAIS PUISSANT)
# =========================================================

class ActionBasedPermission(BasePermission):
    """
    Permet de définir permissions selon action DRF
    """

    permission_map = {
        # "create": [IsTechnicien],
        # "destroy": [IsAdmin],
    }

    def has_permission(self, request, view):
        if view.action in self.permission_map:
            return any(
                permission().has_permission(request, view)
                for permission in self.permission_map[view.action]
            )
        return True
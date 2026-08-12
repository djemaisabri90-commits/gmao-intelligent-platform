# après l_adaptatioon des selectors + views + serializers + service :
# étoile * cause= collision des noms+debug compliqué

from django.urls import path, include
# après avoir mettre auth/__init__
# - - > pas besion d'import explicite
#from maintenance.views.login_views import login
#from maintenance.views.register_views import register
from maintenance.views.auth import login, registration
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from maintenance.views import (
    MachineViewSet,
    WorkOrderViewSet,
    InterventionViewSet,
    UtilisateurViewSet,
    PieceViewSet,
    PieceUtiliseeViewSet,
    RapportViewSet,
    LogViewSet,
    AuditLogViewSet,
    SignalementViewSet,
    NotificationViewSet,
    CategorieViewSet,
    PasswordResetRequestViewSet,
)

router = DefaultRouter()

router.register("machines", MachineViewSet, basename="machine")
router.register("workorders", WorkOrderViewSet, basename="workorder")
router.register("interventions", InterventionViewSet, basename="intervention")
router.register("utilisateurs", UtilisateurViewSet, basename="utilisateur")
router.register("pieces", PieceViewSet, basename="piece")
router.register("pieces-utilisees", PieceUtiliseeViewSet, basename="pieceutilisee")
router.register("rapports", RapportViewSet, basename="rapport")
router.register("logs", LogViewSet, basename="log")
router.register("auditlogs", AuditLogViewSet, basename="auditlog")
router.register("signalements", SignalementViewSet, basename="signalements")

router.register(r'categories', CategorieViewSet, basename='categorie')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'password-reset-requests', PasswordResetRequestViewSet,
                basename='password-reset-requests')

#print("Loading maintenance/urls.py", id(router) if 'router' in dir() else 'no router yet')
#print("Router URLs count:", len(router.urls))
#for url in router.urls:
    #print(url.name, url.pattern)

# Router imbriqué pour les pièces utilisées dans une intervention
intervention_router = NestedDefaultRouter(router, r"interventions", lookup="intervention")
intervention_router.register(r"pieces", PieceUtiliseeViewSet, basename="intervention-pieces")

urlpatterns = [
    path('', include(router.urls)),
    path("", include(intervention_router.urls)),

    # Actions spécifiques sur interventions
    path("interventions/<int:pk>/start/", InterventionViewSet.start, name="start_intervention"),
    path("interventions/<int:pk>/finish/", InterventionViewSet.finish, name="finish_intervention"),
    path("interventions/<int:pk>/validate/", InterventionViewSet.validate, name="validate_intervention"),
    #path("interventions/<int:pk>/change-statut/", InterventionViewSet.changeStatut, name="change_statut_intervention"),
    
    # Authentification
    path("auth/register/", registration, name="register"),
    path("auth/login/", login, name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

               
             
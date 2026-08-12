# je vais ici importer toutes les vues.
from .machine_views import MachineViewSet
from .utilisateur_views import UtilisateurViewSet
from .workorder_views import WorkOrderViewSet
from .intervention_views import InterventionViewSet
from .piece_views import PieceViewSet
from .piece_utilisee_views import PieceUtiliseeViewSet
from .log_views import LogViewSet
from .audit_views import AuditLogViewSet
from .rapport_views import RapportViewSet
from .signalement_views import SignalementViewSet
from .notification_views import NotificationViewSet
from .categorie_views import CategorieViewSet
from .request_views import PasswordResetRequestViewSet
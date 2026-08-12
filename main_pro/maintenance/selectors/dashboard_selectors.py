from django.db.models import Count
from maintenance.models import Machine, WorkOrder, Intervention, Log


def get_dashboard_stats():

    machines_count = Machine.objects.count()

    machines_down = Machine.objects.filter(
        etat="PANNE"
    )

    machines_most_failures = Machine.objects.annotate(
        total_workorders=Count("workorder")
    ).order_by("-total_workorders")[:5]    

    workorders_open = WorkOrder.objects.filter(
        statut="en_cours"
    ).select_related(
        "machine",
        "technicien__user"
    )
    # j'ai ajouté attribut --staut--
    interventions_running = Intervention.objects.filter(
        statut="en_cours"
    ).select_related(
        "workorder",
        "technicien__user"
    )
    """
    # modèle Intervention n'a pas de statut
    # on va filtrer selon la date_debut et date_fin
    # déclencheur : intervention en cours:
    interventions_running = Intervention.objects.filter(
        date_debut__isnull=False,
        date_fin__isnul=False
    ).select_related(
        "workorder",
        "technicien__user"
    )  
    """
    # déclencheur : intervention terminée:
    interventions_termine= Intervention.objects.select_related(
        "workorder",
        "technicien__user"
    ).filter(
        date_fin__isnull=False
    )

    # déclencheur : intervention récente:
    interventions_recent = Intervention.objects.select_related(
        "workorder",
        "technicien__user"
    ).order_by("-date_debut")[:10]

    recent_logs = Log.objects.select_related(
        "utilisateur",
        "machine"
    ).order_by("-date")[:10]

    return {
        "machines_count": machines_count,
        "machines_down": machines_down,
        "machines_most_failures": machines_most_failures,
        "workorders_open": workorders_open,
        "interventions_running": interventions_running,
        "interventions_termine": interventions_termine,
        "recent_interventions": interventions_recent,
        "recent_logs": recent_logs,

    }

"""
# React Dashboard (exemple)

Ton frontend React pourra faire :

const response = await fetch("/api/dashboard/");
const data = await response.json();

setMachines(data.machines_count);
setWorkorders(data.workorders_open);
setInterventions(data.interventions_running);

"""
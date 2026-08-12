from maintenance.models import Log


def create_log(workorder, user, action, etat_intervention=None, metadata=None):
    """
    Crée un log enrichi lié à un WorkOrder et sa Machine.
    - workorder : objet WorkOrder concerné
    - user : utilisateur ayant déclenché l'action
    - action : description de l'action
    - etat_intervention : état calculé de l'intervention au moment du log
    - metadata : dictionnaire JSON optionnel (durée, pièces utilisées, etc.)
    """
    return Log.objects.create(
        workorder=workorder,
        machine=workorder.machine,
        user=user,
        action=action,
        etat_intervention=etat_intervention,
        metadata=metadata or {}
    )

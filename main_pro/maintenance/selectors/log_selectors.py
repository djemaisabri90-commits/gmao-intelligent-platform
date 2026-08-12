# maintenance/selectors/log_selectors.py

from maintenance.models import Log


def get_logs(with_relations=True):
    """
    Retourne tous les logs, avec relations préchargées si demandé.
    """
    qs = Log.objects.all().order_by("-date_action")
    if with_relations:
        qs = qs.select_related("workorder", "machine", "user")
    return qs


def get_logs_machine(machine_id, with_relations=True):
    """
    Retourne les logs liés à une machine spécifique.
    """
    qs = Log.objects.filter(machine_id=machine_id).order_by("-date_action")
    if with_relations:
        qs = qs.select_related("workorder", "machine", "user")
    return qs


def get_logs_workorder(workorder_id, with_relations=True):
    """
    Retourne les logs liés à un WorkOrder spécifique.
    """
    qs = Log.objects.filter(workorder_id=workorder_id).order_by("-date_action")
    if with_relations:
        qs = qs.select_related("workorder", "machine", "user")
    return qs


def get_logs_user(user_id, with_relations=True):
    """
    Retourne les logs liés à un utilisateur spécifique.
    """
    qs = Log.objects.filter(user_id=user_id).order_by("-date_action")
    if with_relations:
        qs = qs.select_related("workorder", "machine", "user")
    return qs

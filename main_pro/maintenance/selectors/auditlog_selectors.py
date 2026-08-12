# maintenance/selectors/auditlog_selectors.py

from maintenance.models import AuditLog


def get_audit_logs(with_relations=True):
    """
    Retourne un QuerySet de base pour AuditLog.
    - Précharge la relation user si demandé
    """
    qs = AuditLog.objects.all().order_by("-timestamp")
    if with_relations:
        qs = qs.select_related("user")
    return qs


def get_audit_logs_by_user(user_id):
    """
    Retourne les logs filtrés par utilisateur.
    """
    return get_audit_logs().filter(user_id=user_id)


def get_audit_logs_by_model(model_name):
    """
    Retourne les logs filtrés par modèle (ex: 'Intervention').
    """
    return get_audit_logs().filter(model=model_name)


def get_audit_logs_by_action(action):
    """
    Retourne les logs filtrés par action (ex: 'update', 'delete').
    """
    return get_audit_logs().filter(action=action)


def get_audit_logs_in_period(start_date=None, end_date=None):
    """
    Retourne les logs filtrés par période.
    """
    qs = get_audit_logs()
    if start_date:
        qs = qs.filter(timestamp__gte=start_date)
    if end_date:
        qs = qs.filter(timestamp__lte=end_date)
    return qs

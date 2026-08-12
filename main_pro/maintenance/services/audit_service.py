from maintenance.models import AuditLog


def audit_action(request, action, instance, changements=None):
    """
    Crée une entrée d'audit pour une action donnée.
    - request : objet HTTP (permet de récupérer user, IP, user_agent, endpoint, method)
    - action : type d'action (create, update, delete, validate, start, finish)
    - instance : objet concerné (ex: Intervention, WorkOrder, Machine)
    - changements : dict des modifications (avant/après)
    """
    user = request.user if request.user.is_authenticated else None

    AuditLog.objects.create(
        user=user,
        action=action,
        model=instance.__class__.__name__,
        object_id=instance.id,
        ip_address=get_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        endpoint=request.path,
        method=request.method,
        changements=changements or {}
    )


def get_audit_changes(old_instance, new_data):
    """
    Compare l'ancienne instance avec les nouvelles données
    et retourne un dict des changements.
    """
    changements = {}

    for field, value in new_data.items():
        old_value = getattr(old_instance, field, None)

        if old_value != value:
            changements[field] = {
                "old": str(old_value) if old_value is not None else None,
                "new": str(value) if value is not None else None,
            }

    return changements


def get_client_ip(request):
    """
    Récupère l'adresse IP du client depuis la requête.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

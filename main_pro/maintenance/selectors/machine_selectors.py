from django.db.models import Count
from maintenance.models import Machine


def get_machine_queryset(with_workorders=False):
    qs = Machine.objects.all()
    if with_workorders:
        qs = qs.prefetch_related('workorder_set')  # relation par défaut
    return qs


def get_machine_list(filters=None, with_workorders=False):
    qs = get_machine_queryset(with_workorders)
    if filters:
        qs = qs.filter(**filters)
    return qs.order_by('nom')


def get_machine_detail(machine_id, with_workorders=False):
    qs = get_machine_queryset(with_workorders)
    return qs.get(id=machine_id)


def get_machine_stats():
    """
    Retourne des statistiques globales sur les machines :
    - total
    - par état
    - par type
    - nombre de machines avec au moins un WorkOrder
    """
    total = Machine.objects.count()

    by_status = Machine.objects.values('etat').annotate(count=Count('id'))
    by_type = Machine.objects.values('type').annotate(count=Count('id'))

    # Compter les machines ayant au moins un WorkOrder
    with_workorders = Machine.objects.annotate(
        workorder_count=Count('workorder')
    ).filter(workorder_count__gt=0).count()

    return {
        'total': total,
        'by_status': {item['etat']: item['count'] for item in by_status},
        'by_type': {item['type']: item['count'] for item in by_type},
        'machines_with_workorders': with_workorders,
    }

# maintenance/selectors/workorder_selectors.py
from django.db import models

from django.db.models import Q, Count, Avg, ExpressionWrapper, F, DurationField
from maintenance.models import WorkOrder
from django.contrib.auth import get_user_model

User = get_user_model()


def get_workorder_queryset(with_relations=True):
    """
    Retourne un QuerySet de base pour WorkOrder.
    Optionnellement précharge les relations (select_related).
    """
    qs = WorkOrder.objects.all()
    if with_relations:
        qs = qs.select_related(
            'machine',
            'signalement',
            'expert',
            'cree_par'
        ).prefetch_related("techniciens")
    return qs


def get_workorder_list(filters=None, user=None, with_relations=True):
    """
    Retourne la liste des bons de travail avec filtres optionnels.
    - filters: dictionnaire de filtres (ex: {'priorite': 'high'})
    """
    qs = get_workorder_queryset(with_relations)

    if filters:
        qs = qs.filter(**filters)
    return qs.order_by('-date_creation')


def get_workorder_detail(workorder_id, with_relations=True):
    """
    Récupère un bon de travail par son id.
    Lève WorkOrder.DoesNotExist si non trouvé.
    """
    qs = get_workorder_queryset(with_relations)
    return qs.get(id=workorder_id)


def get_workorders_by_user(user, role_filter=None):
    """
    Récupère les bons de travail liés à un utilisateur.
    - role_filter: 'technicien', 'expert', 'cree_par' ou None pour tous les rôles.
    """
    if user is None:
        return WorkOrder.objects.none()
    if role_filter == 'technicien':
        qs = WorkOrder.objects.filter(techniciens=user)
    elif role_filter == 'expert':
        qs = WorkOrder.objects.filter(expert=user)
    elif role_filter == 'cree_par':
        qs = WorkOrder.objects.filter(cree_par=user)
    else:
        qs = WorkOrder.objects.filter(
            Q(techniciens=user) | Q(expert=user) | Q(cree_par=user)
        )
    return qs.select_related('machine', 'signalement').order_by('-date_creation')


def get_workorders_by_machine(machine_id):
    """
    Récupère les bons de travail d'une machine.
    """
    qs = WorkOrder.objects.filter(machine_id=machine_id)
    return qs.select_related('expert', 'cree_par').prefetch_related('techniciens').order_by('-date_creation')


def get_workorders_by_date_range(start_date, end_date, user=None, with_relations=True):
    """
    Récupère les bons de travail créés dans un intervalle de dates.
    Optionnellement restreint par utilisateur.
    """
    qs = get_workorder_queryset(with_relations).filter(
        date_creation__gte=start_date,
        date_creation__lte=end_date
    )
    if user and not user.is_superuser:
        if hasattr(user, 'role'):
            if user.role == 'technicien':
                qs = qs.filter(techniciens=user)
            elif user.role == 'expert':
                #qs = qs.filter(expert=user)
                pass
    return qs.order_by('date_creation')


def get_workorder_stats(user=None):
    """
    Retourne des statistiques globales sur les bons de travail.
    Optionnellement restreint par utilisateur.
    """
    qs = get_workorder_queryset(with_relations=False)
    if user and not user.is_superuser:
        if hasattr(user, 'role'):
            if user.role == 'technicien':
                qs = qs.filter(techniciens=user)
            elif user.role == 'expert':
                #qs = qs.filter(expert=user)
                pass

    stats = {
        'total': qs.count(),
        'by_priority': dict(qs.values('priorite').annotate(count=Count('id')).values_list('priorite', 'count')),
        'by_type': dict(qs.values('type').annotate(count=Count('id')).values_list('type', 'count')),
        # etat est une propriété Python, pas un champ DB → calcul via boucle
        'by_etat': {},
        'avg_completion_time': None,
    }

    # Calcul des états
    etat_counts = {}
    for wo in qs:
        etat_counts[wo.etat] = etat_counts.get(wo.etat, 0) + 1
    stats['by_etat'] = etat_counts

    # Calcul du délai moyen de clôture
    closed_qs = qs.filter(date_cloture__isnull=False)
    if closed_qs.exists():
        delta = ExpressionWrapper(F('date_cloture') - F('date_creation'), output_field=DurationField())
        avg_delta = closed_qs.annotate(delta=delta).aggregate(avg=Avg('delta'))['avg']
        if avg_delta:
            stats['avg_completion_time'] = avg_delta.total_seconds() / 3600  # en heures

    return stats


def get_workorder_summary_for_machine(machine_id):
    """
    Retourne un résumé des bons de travail pour une machine donnée.
    """
    qs = WorkOrder.objects.filter(machine_id=machine_id)
    etat_counts = {}
    for wo in qs:
        etat_counts[wo.etat] = etat_counts.get(wo.etat, 0) + 1

    return {
        'total': qs.count(),
        'by_etat': etat_counts,
        'last_workorder': qs.order_by('-date_creation').values('id', 'date_creation').first(),
        'open_count': sum(1 for wo in qs if wo.etat in ['en_attente', 'valide', 'en_cours']),
    }

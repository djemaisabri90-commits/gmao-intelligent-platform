from maintenance.models import Rapport


def get_rapports():
    return Rapport.objects.select_related(
        
        "workorder"
    )


def get_rapport(rapport_id):
    return Rapport.objects.select_related(
        
        "workorder"
    ).filter(id=rapport_id).first()
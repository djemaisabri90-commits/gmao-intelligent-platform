from maintenance.models import Rapport


def create_rapport(data):
    return Rapport.objects.create(**data)


def update_rapport(rapport, data):
    for attr, value in data.items():
        setattr(rapport, attr, value)
    rapport.save()
    return rapport


def delete_rapport(rapport):
    rapport.delete()
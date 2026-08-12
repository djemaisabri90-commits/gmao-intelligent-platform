from maintenance.models import Signalement


def create_signalement(user, **validated_data):
    return Signalement.objects.create(
        cree_par=user,
        **validated_data
    )


def update_signalement(signalement, **validated_data):
    for attr, value in validated_data.items():
        setattr(signalement, attr, value)

    signalement.save()
    return signalement


def close_signalement(signalement):
    signalement.statut = "traite"
    signalement.save()
    return signalement
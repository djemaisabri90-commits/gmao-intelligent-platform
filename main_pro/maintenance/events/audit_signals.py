from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.conf import settings
from rest_framework.authtoken.models import Token

from maintenance.models import Machine, WorkOrder, Intervention
from maintenance.services.audit_service import create_audit_log


User = settings.AUTH_USER_MODEL

# token auto-géré via autdit_signals :
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Machine)
def machine_saved(sender, instance, created, **kwargs):

    action = "create" if created else "update"

    create_audit_log(
        user=None,
        action=action,
        model="Machine",
        object_id=instance.id
    )


@receiver(post_delete, sender=Machine)
def machine_deleted(sender, instance, **kwargs):

    create_audit_log(
        user=None,
        action="delete",
        model="Machine",
        object_id=instance.id
    )
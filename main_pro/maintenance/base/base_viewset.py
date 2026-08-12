from rest_framework import viewsets
from maintenance.base.pagination import DefaultPagination
from maintenance.services.audit_service import audit_action, get_audit_changes


class BaseViewSet(viewsets.ModelViewSet):

    pagination_class = DefaultPagination

    read_serializer_class = None
    write_serializer_class = None

    def get_serializer_class(self):

        if self.action in ["create", "update", "partial_update"]:
            return self.write_serializer_class

        return self.read_serializer_class

# aprés la nouvelle strucutre de projet
# Viewset avec audit avancé

    def perform_create(self, serializer):

        instance = serializer.save()

        user = self.request.user

        audit_action(user, "CREATE", instance)


    def perform_update(self, serializer):

        old_instance = self.get_object()

        changes = get_audit_changes(old_instance, serializer.validated_data)

        instance = serializer.save()
        #audit_action(self.request, "update", instance, changes)
        user = self.request.user

        audit_action(user, "UPDATE", instance, changes)


    def perform_destroy(self, instance):

        user = self.request.user

        audit_action(user, "DELETE", instance)

        instance.delete()
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
import random
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from maintenance.base.permissions import IsAdmin
from maintenance.models import PasswordResetRequest
from maintenance.serializers.request_serializer import PasswordResetRequestSerializer

from maintenance.signals import generate_random_password

class PasswordResetRequestViewSet(viewsets.ModelViewSet):

    queryset = PasswordResetRequest.objects.all().order_by("-created_at")

    serializer_class = PasswordResetRequestSerializer

    permission_classes = [IsAuthenticated, IsAdmin]


    @action(detail=True, methods=["post"])
    def process(self, request, pk=None):

        reset_request = self.get_object()
        user = reset_request.user

        if reset_request.status != "pending":
            return Response(
            {"error": "Cette demande a déjà été traitée."},
            status=status.HTTP_400_BAD_REQUEST
        )



        user = reset_request.user

        temp_password = generate_random_password()

        user.set_password(temp_password)

        user.must_change_password = True

        user.activation_token = "".join(
            random.choices(
                "ABCDEFGHJKLMNPQRSTUVWXYZ23456789",
                k=6
            )
        )
        #évite de stocker en base beaucoup plus sécurisé
        user.temporary_password = temp_password

        user.save()

        reset_request.status = "resolved"

        reset_request.processed_at = timezone.now()

        reset_request.processed_by = request.user

        reset_request.save()

        return Response({
            "id": user.id,
            "username": user.username,
            "temporary_password": temp_password,
            "activation_token": user.activation_token,
            "status": "resolved"
        })
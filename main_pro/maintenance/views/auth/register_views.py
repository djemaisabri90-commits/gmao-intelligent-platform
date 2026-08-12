from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token

from maintenance.serializers.register_serializer import RegisterSerializer
from maintenance.services.utilisateur_service import create_utilisateur


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):

    serializer = RegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        utilisateur = create_utilisateur(serializer.validated_data)

        token, _ = Token.objects.get_or_create(user=utilisateur)

        return Response({
            "user": RegisterSerializer(utilisateur).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {"error": "Erreur lors de l'inscription", "details": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
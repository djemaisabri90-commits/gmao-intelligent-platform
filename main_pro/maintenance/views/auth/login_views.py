#maintenance/views/auth/login_views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from maintenance.serializers.login_serializer import LoginSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):

    serializer = LoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.validated_data["user"]

    # sécuité renforcée = génération JWT
    refresh = RefreshToken.for_user(user)
    
    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "username": user.username,
            "role": getattr(user, 'role', None),
            "must_change_password": user.must_change_password,
        }
    })





from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

# 🛡️ Sécurité : Limite à 3 tentatives par minute pour éviter le brute-force des codes
class PasswordResetThrottle(AnonRateThrottle):
    rate = '3/minute'

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 🔐 Cas connecté (via la bannière + Interceptor)
@throttle_classes([PasswordResetThrottle])
def change_password_authenticated(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # Sécurité : Vérifier que l'utilisateur connecté ne modifie que son propre compte
    if request.user != user:
        return Response({"error": "Action non autorisée."}, status=status.HTTP_403_FORBIDDEN)
        
    activation_token = request.data.get('activation_token')
    password = request.data.get('password')
    
    if not activation_token or not password:
        return Response({"error": "Données incomplètes."}, status=status.HTTP_400_BAD_REQUEST)
        
    # 🤖 VALIDATION AUTOMATIQUE : Comparaison du jeton en base de données
    if str(user.activation_token) != str(activation_token):
        return Response({"error": "Le code d'activation est incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        
    # Validation et enregistrement du nouveau mot de passe définitif
    user.set_password(password)
    user.must_change_password = False
    user.save()
    
    return Response({"message": "Mot de passe modifié avec succès."}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])  # 🔓 Cas non connecté (lien direct ou oubli)
@throttle_classes([PasswordResetThrottle])
def change_password_by_username(request):
    username = request.data.get('username')
    activation_token = request.data.get('activation_token')
    password = request.data.get('password')
    
    if not username or not activation_token or not password:
        return Response({"error": "Données incomplètes."}, status=status.HTTP_400_BAD_REQUEST)
        
    # Récupération de l'utilisateur par son identifiant unique
    user = get_object_or_404(User, username=username)
    
    # 🤖 VALIDATION AUTOMATIQUE : Vérification du jeton
    if str(user.activation_token) != str(activation_token):
        return Response({"error": "Le code d'activation ou l'identifiant est incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        
    user.set_password(password)
    user.must_change_password = False
    user.save()
    
    return Response({"message": "Mot de passe modifié avec succès."}, status=status.HTTP_200_OK)

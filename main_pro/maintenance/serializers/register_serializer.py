
"""
from rest_framework import serializers
from maintenance.models import Utilisateur

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=Utilisateur.ROLE_CHOICES)
    telephone = serializers.CharField(required=False, allow_blank=True, max_length=20)

    def validate_username(self, value):
        if Utilisateur.objects.filter(username=value).exists():
            raise serializers.ValidationError("Un utilisateur avec ce nom existe déjà.")
        return value

    def create(self, validated_data):
        # Création du User
        user = Utilisateur.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        # Création du profil Utilisateur associé
        utilisateur = Utilisateur.objects.create(
            role=validated_data['role'],
            telephone=validated_data.get('telephone', '')
        )
        return utilisateur
"""

from rest_framework import serializers
from maintenance.models import Utilisateur


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    

    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    role = serializers.ChoiceField(choices=Utilisateur.ROLE_CHOICES)

    class Meta:
        model = Utilisateur
        fields = ["username", "email", "password", "role", "telephone"]

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Mot de passe trop court")
        return value
    
    def create(self, validated_data):

        username = validated_data.pop("username")
        password = validated_data.pop("password")
        email = validated_data.pop("email", "")
        role = validated_data.pop("role")
        
        user = Utilisateur.objects.create_user(
            username=username,
            password=password,
            email=email,
            role=role
            
        )
        return user
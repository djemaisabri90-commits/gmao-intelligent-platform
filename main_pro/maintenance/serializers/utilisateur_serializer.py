# maintenance/serializers/utilisateur_serializer.py

from rest_framework import serializers
from maintenance.models import Utilisateur, Categorie 
from maintenance.serializers.categorie_serializer import CategorieSerializer

class UtilisateurReadSerializer(serializers.ModelSerializer):
    categorie_detail = CategorieSerializer(source="categorie", read_only=True)
    temporary_password = serializers.SerializerMethodField()

    class Meta:
        model = Utilisateur
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "telephone",
            "categorie",
            "categorie_detail",
            "is_active",
            "date_joined",
            "must_change_password",  # ✅ exposé côté frontend
            "activation_token",
            "temporary_password",
        ]
    
    def get_temporary_password(self, obj):
        print(
            "SERIALIZER PASSWORD =",
            getattr(obj, "_temp_password_plain", None)
        )
        # Renvoie le mot de passe en clair généré par le signal s'il existe en mémoire
        #return getattr(obj, "generated_password",
        #getattr(obj, "_temp_password_plain", None))

        return getattr(obj, "_temp_password_plain", None)
    

class UtilisateurWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    role = serializers.ChoiceField(choices=Utilisateur.ROLE_CHOICES)
    categorie = serializers.PrimaryKeyRelatedField(
    queryset=Categorie.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Utilisateur
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "role",
            "telephone",
            "categorie",
            "is_active",
            "activation_token",
                       
        ]
    

    def validate_password(self, value):
        
        #Applique votre validation de force uniquement si un mot de passe 
        #a été saisi manuellement par l'administrateur.
        if value:  # Si le champ n'est ni vide, ni nul
            from maintenance.views.utilisateur_views import validate_password_strength
            from django.core.exceptions import ValidationError
            try:
                validate_password_strength(value)
            except ValidationError as e:
                raise serializers.ValidationError(e.messages)
        return value

    # logique metier respectee
    def validate(self, data):
        role = data.get("role",
                    getattr(self.instance, "role", None))
        
        categorie = data.get("categorie",
                    getattr(self.instance, "categorie", None)
)
        if role == "technicien" and not categorie:
            raise serializers.ValidationError(
                {"categorie": "Un technicien doit avoir une catégorie."})
        
        if role != "technicien" and categorie:
            raise serializers.ValidationError(
                {"categorie": "Seuls les techniciens peuvent avoir une catégorie."})
        
        return data
    
    """
    def create(self, validated_data):
        
        #Crée un utilisateur avec mot de passe sécurisé et obligation de changement.
        
        password = validated_data.pop("password")
        user = Utilisateur.objects.create(**validated_data)
        user.set_password(password)  # ✅ hash sécurisé
        user.must_change_password = True  # ✅ obligatoire à la première connexion
        user.save()
        return user

    def update(self, instance, validated_data):
        
        #Met à jour un utilisateur avec gestion sécurisée du mot de passe.
        
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
            instance.must_change_password = True  # ✅ obligation si mot de passe changé par admin
        instance.save()
        return instance
"""
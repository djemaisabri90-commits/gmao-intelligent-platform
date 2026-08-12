from rest_framework import serializers

class BaseSerializer(serializers.ModelSerializer):
    # modèles ont :created_at + updated_at
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_user(self):

        request = self.context.get("request")

        if request and hasattr(request, "user"):
            return request.user

        return None

    def validate(self, attrs):

        # validation globale possible ici
        return super().validate(attrs)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        # formatage commun
        for key, value in data.items():
            if value is None:
                data[key] = ""

        return data
    
"""
Ajouter automatiquement l'utilisateur
Pour certains modèles (logs, rapports, vidéos)
 tu veux ajouter automatiquement l’utilisateur.
"""
"""
def create(self, validated_data):

    user = self.get_user()

    if user and "user" in self.Meta.model._meta.fields_map:
        validated_data["user"] = user

    return super().create(validated_data)
"""
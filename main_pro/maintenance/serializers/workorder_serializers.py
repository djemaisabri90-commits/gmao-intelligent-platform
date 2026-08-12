from rest_framework import serializers
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from maintenance.models import Notification, WorkOrder, Signalement, Machine, Categorie
User = get_user_model()

class MachineBasicSerializer(serializers.ModelSerializer):
    """Sérialiseur simple pour Machine (lecture seule)"""
    class Meta:
        model = Machine
        fields = ['id', 'nom', 'etat', 'description']

class WorkOrderBasicSerializer(serializers.ModelSerializer):
    """Version légère pour éviter la récursion infinie"""
    machine_detail = MachineBasicSerializer(source="machine", read_only=True)
    class Meta:
        model = WorkOrder
        fields = ["id", "description", "etat", "priorite", "type", "machine_detail"]

        
class SignalementBasicSerializer(serializers.ModelSerializer):
    """Sérialiseur simple pour Signalement (lecture seule)"""
    class Meta:
        model = Signalement
        fields = ['id', 'description', 'created_at', 'source']
class UserBasicSerializer(serializers.ModelSerializer):
    """Sérialiseur simple pour l'utilisateur (lecture seule)"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role']
        
class CategorieBasicSerializer(serializers.ModelSerializer):
    """Sérialiseur simple pour Categorie (lecture seule)"""
    class Meta:
        model = Categorie
        fields = ['id', 'nom', 'description']
def notify_user(user, workorder):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send_notification",
            "message": {
                "text": f"Nouveau bon de travail #{workorder.id}",
                "workorder_id": workorder.id,
                "categorie": workorder.categorie.nom if workorder.categorie else None,
                "url": f"/workorders/{workorder.id}"  # ✅ lien direct
            }
        }
    )
class WorkOrderSerializer(serializers.ModelSerializer):
    # Champs imbriqués en lecture seule
    machine_detail = MachineBasicSerializer(source='machine', read_only=True)
    signalement_detail = SignalementBasicSerializer(source='signalement', read_only=True)
    techniciens_detail = UserBasicSerializer(source='techniciens', many=True, read_only=True)
    cree_par_detail = UserBasicSerializer(source='cree_par', read_only=True)
    categorie_detail = CategorieBasicSerializer(source='categorie', read_only=True)
    expert_detail = UserBasicSerializer(source='expert', read_only=True)

    # Champs d'écriture (clés étrangères)
    machine = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all())
    signalement = serializers.PrimaryKeyRelatedField(
        queryset=Signalement.objects.all(),
        required=False,
        allow_null=True
    )
    categorie = serializers.PrimaryKeyRelatedField(
        queryset=Categorie.objects.all(),
        required=False,
        allow_null=True
    )
    techniciens = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='technicien'),
        many=True,
        required=False
    )
    expert = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role__in=['admin', 'expert']),
        required=False,
        allow_null=True
    )
    cree_par = serializers.PrimaryKeyRelatedField(read_only=True)

    # Champ calculé : source héritée du signalement
    source = serializers.CharField(source="signalement.source", read_only=True)

    # Champ calculé : état hérité des interventions
    etat = serializers.SerializerMethodField()

    interventions_detail = serializers.SerializerMethodField()  # ✅ champ calculé

    class Meta:
        model = WorkOrder
        fields = [
            'id',
            'signalement', 'signalement_detail',
            'source',
            'machine', 'machine_detail',
            'categorie', 'categorie_detail',
            'techniciens', 'techniciens_detail',
            'expert', 'expert_detail',
            'cree_par', 'cree_par_detail',
            'type', 'priorite',
            'description',
            'date_creation', 'date_cloture',
            'etat',  # champ calculé exposé
            "interventions_detail",
        ]
        read_only_fields = ['date_creation', 'date_cloture', 'etat', 'source']

    def create(self, validated_data):
        techniciens = validated_data.pop('techniciens', [])
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["cree_par"] = request.user

        workorder = super().create(validated_data)
        workorder.techniciens.set(techniciens)  # ✅ assignation ManyToMany

        # ✅ notifier les techniciens concernés
        # Notifications (optimisation possible avec bulk_create)
        notifications = []
        for technicien in workorder.techniciens.all():
            #Notification.objects.create(
            notifications.append(Notification(
                user=technicien,
                message=f"Nouveau bon de travail #{workorder.id}",
                workorder=workorder,
                categorie=workorder.categorie,
                url=f"/workorders/{workorder.id}"
            ))
            # Exemple: envoi d’un signal ou d’un event
            notify_user(technicien, workorder)
        Notification.objects.bulk_create(notifications)

        # notifier l’expert si défini
        if workorder.expert:
            Notification.objects.create(
                user=workorder.expert,
                message=f"Vous êtes assigné comme expert au bon #{workorder.id}",
                workorder=workorder,
                categorie=workorder.categorie,
                url=f"/workorders/{workorder.id}"
            )
            notify_user(workorder.expert, workorder)

        return workorder

    def get_etat(self, obj):
        # ✅ utilise la logique centralisée du modèle
        return obj.etat
    
        """
        interventions = obj.interventions.all()
        if not interventions.exists():
            return "en_attente"
        if all(i.date_validation for i in interventions):
            return "clos" if obj.date_cloture else "valide"
        return "en_cours"
        """

    def get_interventions_detail(self, obj):
        # ✅ import local pour éviter la récursion
        from maintenance.serializers.intervention_serializer import InterventionReadSerializer
        return InterventionReadSerializer(obj.interventions.all(), many=True).data

    def validate(self, data):
        """
        Validation conforme au modèle (reprend les règles de clean()).
        """
        # 1. Rôle de l'expert
        expert = data.get('expert')
        if expert and expert.role not in ['admin', 'expert']:
            raise serializers.ValidationError(
                "L'utilisateur doit avoir le rôle expert ou admin."
            )

        # 2. Rôle du technicien
        techniciens = data.get('techniciens', [])
        for t in techniciens:
            if t.role != 'technicien':
                raise serializers.ValidationError("Tous les utilisateurs doivent avoir le rôle technicien.")

        return data

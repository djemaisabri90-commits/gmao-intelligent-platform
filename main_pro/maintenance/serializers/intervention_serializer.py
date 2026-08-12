from rest_framework import serializers
from maintenance.models import Intervention, WorkOrder
from maintenance.serializers.workorder_serializers import WorkOrderBasicSerializer
from maintenance.serializers.utilisateur_serializer import UtilisateurReadSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class InterventionReadSerializer(serializers.ModelSerializer):
    workorder_detail = WorkOrderBasicSerializer(source="workorder", read_only=True)
    techniciens_detail = UtilisateurReadSerializer(source="techniciens", many=True, read_only=True)  # ✅ tableau
    valide_par_detail = UtilisateurReadSerializer(source="valide_par", read_only=True)
    #etat = serializers.CharField(source="etat", read_only=True)
    etat = serializers.SerializerMethodField()
    class Meta:
        model = Intervention
        fields = [
            "id", "workorder", "workorder_detail",
            "techniciens", "techniciens_detail",  # ✅ cohérent avec ManyToMany
            "date_debut", "date_fin", "actions_realisees",
            "priorite", "type_intervention",
            "valide_par", "valide_par_detail",
            "date_validation", "created_at", "updated_at", "is_locked",
            "etat"
        ]
    def get_etat(self, obj):
        # ✅ utilise la logique centralisée du modèle
        return obj.etat


class InterventionWriteSerializer(serializers.ModelSerializer):
    workorder = serializers.PrimaryKeyRelatedField(queryset=WorkOrder.objects.all())
    techniciens = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="technicien"),  # ✅ filtre direct
        many=True,
        required=False
    )
    valide_par = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role__in=["admin", "expert"]),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Intervention
        fields = [
            "id",
            "workorder",
            "techniciens",  # ✅ liste
            "date_debut",
            "date_fin",
            "actions_realisees",
            "priorite",
            "type_intervention",
            "valide_par",
            "date_validation",
            "created_at",
            "updated_at",
            "is_locked",
        ]
        read_only_fields = ["created_at", "updated_at", "date_validation", "is_locked"]

    def validate(self, data):
        # ✅ déléguer au modèle pour éviter duplication
        """
        date_debut = data.get("date_debut")
        date_fin = data.get("date_fin")
        techniciens = data.get("techniciens", [])
        valide_par = data.get("valide_par")

        # 1. Cohérence des dates
        if date_fin and date_debut and date_fin < date_debut:
            raise serializers.ValidationError("date_fin doit être après date_debut")

        # 2. Rôle des techniciens
        for t in techniciens:
            if hasattr(t, "role") and t.role != "technicien":
                raise serializers.ValidationError("Tous les utilisateurs doivent avoir le rôle technicien")

        # 3. Validation par expert/admin
        if valide_par and hasattr(valide_par, "role") and valide_par.role not in ["admin", "expert"]:
            raise serializers.ValidationError("Seul un admin ou expert peut valider une intervention")

        # 4. Une intervention validée doit être terminée
        if valide_par and not date_fin:
            raise serializers.ValidationError("Une intervention validée doit être terminée avant validation")
        """
        instance = Intervention(**data)
        instance.full_clean()  # applique la logique de clean()


        return data

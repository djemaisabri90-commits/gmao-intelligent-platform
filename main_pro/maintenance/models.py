from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from django.conf import settings
from django.utils import timezone

# Notification
class Notification(models.Model):
    class NotificationType(models.TextChoices):
        WORKORDER_CREATED = "workorder_created", "WorkOrder créé"
        INTERVENTION_STARTED = "intervention_started", "Intervention démarrée"
        INTERVENTION_FINISHED = "intervention_finished", "Intervention terminée"
        INTERVENTION_VALIDATED = "intervention_validated", "Intervention validée"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    message = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=NotificationType.choices, default=NotificationType.WORKORDER_CREATED, db_index=True)

    workorder = models.ForeignKey(
        "WorkOrder",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )
    intervention = models.ForeignKey(  # ✅ ajout optionnel
        "Intervention",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications"
    )
    categorie = models.ForeignKey(
        "Categorie",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    url = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"


# Machines
class Machine(models.Model):
    STATUS_CHOICES = [
        ('SERVICE', 'En service'),
        ('PANNE', 'En panne'),
        ('MAINTENANCE', 'En maintenance'),
        ('INCONNU', 'Inconnu'),
    ]

    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    

    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    localisation = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    date_installation = models.DateField(null=True, blank=True)
    etat = models.CharField(max_length=50, choices=STATUS_CHOICES, default='SERVICE')

    def update_etat(self):
        """
        Synchronise l'état de la machine en fonction des WorkOrders liés.
        - SERVICE : aucun WorkOrder ou tous clos
        - MAINTENANCE : au moins un WorkOrder en cours
        - PANNE : au moins un WorkOrder en attente
        - INCONNU : cas non couvert
        """
        workorders = self.workorder_set.all()

        if not workorders.exists():
            self.etat = "SERVICE"
        elif any(wo.etat == "en_cours" for wo in workorders):
            self.etat = "MAINTENANCE"
        elif any(wo.etat == "en_attente" for wo in workorders):
            self.etat = "PANNE"
        elif all(wo.etat in ["clos", "valide"] for wo in workorders):
            self.etat = "SERVICE"
        else:
            self.etat = "INCONNU"

        self.save()

    def __str__(self):
        return self.nom


# Categorie
class Categorie(models.Model):
    TYPE_CHOICES = [
        ("electrique", "Électrique"),
        ("mecanique", "Mécanique"),
        ("automation", "Automation"),
        ("utilitaire", "Utilitaire"),
    ]

    nom = models.CharField(max_length=50, choices=TYPE_CHOICES, unique=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_nom_display()
    


# Utilisateurs (Classe Abstraite)
class Utilisateur(AbstractUser):

    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("technicien", "Technicien"),
        ("expert", "Expert"),
        ("operateur", "Operateur"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="admin")
    telephone = models.CharField(max_length=20, blank=True, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name="utilisateurs")
    must_change_password = models.BooleanField(default=True)  # ✅ nouveau champ

    # 🔑 Le jeton unique pour la validation automatique (généré à la création)
    # On utilise max_length=64 pour stocker soit un UUID, soit un code alphanumérique
    activation_token = models.CharField(max_length=64, blank=True, null=True, unique=True)
    temporary_password = models.CharField(
    max_length=100,
    blank=True,
    null=True
    )

    def clean(self):
        # ⚠️ Validation métier : un technicien doit avoir une catégorie
        if self.role == "technicien" and not self.categorie:
            raise ValidationError("Un technicien doit obligatoirement être associé à une catégorie.")
        
        # tech seul = cat
        # ⚠️ Validation métier : seuls les techniciens peuvent avoir une catégorie
        if self.role != "technicien" and self.categorie:
            raise ValidationError("seul un technicien peut être associé à une catégorie.")
        
    def __str__(self):
        if self.role == "technicien" and self.categorie:
            return f"{self.username} ({self.categorie.get_nom_display()})"
        return f"{self.username} ({self.role})"
    
class PasswordResetRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("resolved", "Traitée"),
        ("rejected", "Rejetée"),
    ]
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE,
                             related_name="password_reset_requests")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,
        choices=STATUS_CHOICES,default="pending")  # pending / resolved
    processed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    processed_by = models.ForeignKey(
        Utilisateur,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="processed_password_resets"
    )

class SignalementStatus(models.TextChoices):
    NOUVEAU = "nouveau", "Nouveau"       # créé par opérateur/technicien
    EN_COURS = "en_cours", "En cours"    # expert en train d’analyser
    TRAITE = "traite", "Traité"          # expert a pris une décision (ex. création WorkOrder)
    CLOS = "clos", "Clos"                # signalement terminé/archivé



# Signalement
class Signalement(models.Model):
    class SourceChoices(models.TextChoices):
        MANUEL = "manuel", "Humain"
        PREVENTIF = "preventif", "Préventif"
        IOT = "iot", "IoT"

    statut = models.CharField(
        max_length=20,
        choices=SignalementStatus.choices,
        default=SignalementStatus.NOUVEAU,
        db_index=True
    )

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    description = models.TextField()
    source = models.CharField(
        max_length=20,
        choices=SourceChoices.choices,
        db_index=True  # ✅ index ajouté
    )

    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Vérification du rôle du créateur
        if self.cree_par and self.cree_par.role not in ["operateur", "technicien", "expert", "admin"]:
            raise ValidationError("Seul un opérateur, technicien, expert ou admin peut créer un signalement.")

        # Cohérence du statut
        if self.statut in [SignalementStatus.TRAITE, SignalementStatus.CLOS] and self.cree_par.role not in ["expert", "admin"]:
            raise ValidationError("Seul un expert ou admin peut traiter ou clôturer un signalement.")

    def __str__(self):
        return f"Signalement #{self.id} - {self.machine.nom} - {self.statut}"



# WorkOrders (Bons de travail)
class WorkOrder(models.Model):
    TYPE_CHOICES = [
        ("corrective", "Corrective"),
        ("preventive", "Préventive"),
        ("predictive", "Prédictive"),
    ]
    PRIORITY_CHOICES = [
        ("high", "Haute"),
        ("medium", "Moyenne"),
        ("low", "Basse"),
    ]

    signalement = models.ForeignKey(
        Signalement, null=True, blank=True, on_delete=models.SET_NULL
    )
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workorders"
    )

    # ✅ ManyToMany pour plusieurs techniciens
    techniciens = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="bons_techniciens",
        blank=True
    )

    expert = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bons_expert"
    )

    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default="predictive")
    priorite = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="high")
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True, db_index=True)
    date_cloture = models.DateTimeField(null=True, blank=True)
    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="bons_crees"
    )

    @property
    def etat(self):
        interventions = self.interventions.all()
        if not interventions.exists():
            return "en_attente"
        if all(i.etat == "valide" for i in interventions):
            return "clos"   # ✅ clôture automatique
        if any(i.etat == "en_cours" for i in interventions):
            return "en_cours"
        if any(i.etat == "termine" for i in interventions):
            return "termine"
        return "en_attente"

    """
    @property
    def etat(self):
        interventions = self.interventions.all()
        if not interventions.exists():
            return "en_attente"
        if all(i.date_validation for i in interventions):
            return "clos" if self.date_cloture else "valide"
        return "en_cours"
    """

    @property
    def source(self):
        return self.signalement.source if self.signalement else None

    def clean(self):
        # validation expert
        if self.expert and self.expert.role not in ["admin", "expert"]:
            raise ValidationError("L'utilisateur doit avoir le rôle expert ou admin")
        
        # validation techniciens (uniquement si l'objet est déjà en base)
        if self.pk:
            for technicien in self.techniciens.all():
                if technicien.role != "technicien":
                    raise ValidationError("Tous les utilisateurs doivent avoir le rôle technicien")

        # validation techniciens
        #for technicien in self.techniciens.all():
            #if technicien.role != "technicien":
                #raise ValidationError("Tous les utilisateurs doivent avoir le rôle technicien")
        
        # validation date cloture
        if self.date_cloture and not all(i.date_validation for i in self.interventions.all()):
            raise ValidationError("Un bon de travail clôturé doit avoir toutes ses interventions validées")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"WO#{self.id} - {self.machine.nom}"



# Interventions
class Intervention(models.Model):
    workorder = models.ForeignKey(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name="interventions"
    )
    techniciens = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="interventions_techniciens",
        blank=True
    )

    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)

    actions_realisees = models.TextField(blank=True)

    priorite = models.CharField(
        max_length=10,
        choices=[("basse", "Basse"), ("moyenne", "Moyenne"), ("haute", "Haute")],
        default="moyenne"
    )

    type_intervention = models.CharField(
        max_length=20,
        choices=[("corrective", "Corrective"), ("preventive", "Préventive"), ("inspection", "Inspection")],
        default="inspection"
    )

    valide_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="interventions_validees"
    )
    date_validation = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    is_locked = models.BooleanField(default=False)

    @property
    def etat(self):
        if not self.date_debut:
            return "en_attente"
        if self.date_debut and not self.date_fin:
            return "en_cours"
        if self.date_fin and not self.date_validation:
            return "termine"
        if self.date_validation and self.valide_par and self.is_locked:
            return "valide"
        return "en_attente"
    
    @property
    def cout_pieces(self):
        return sum(
        ligne.cout_total
        for ligne in self.pieces.all()
        )

    def clean(self):
        if self.date_fin and self.date_debut and self.date_fin < self.date_debut:
            raise ValidationError("date_fin doit être après date_debut")

        if self.date_fin and not self.date_debut:
            raise ValidationError("Une intervention terminée doit avoir une date_debut")
        
        # ✅ validation techniciens seulement si l'objet est déjà sauvegardé
        if self.pk:
            for technicien in self.techniciens.all():
                if technicien.role != "technicien":
                    raise ValidationError("Tous les utilisateurs doivent avoir le rôle technicien")
            
        if self.valide_par:
            if self.valide_par.role not in ["admin", "expert"]:
                raise ValidationError("Seul un admin ou expert peut valider une intervention")
            if not self.date_fin:
                raise ValidationError("Une intervention validée doit être terminée avant validation")
            if not self.date_validation:
                raise ValidationError("Une intervention validée doit avoir une date de validation")
            if not self.is_locked:
                raise ValidationError("Une intervention validée doit être verrouillée")

        if self.date_validation and not self.valide_par:
            raise ValidationError("valide_par requis si date_validation est définie")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Intervention #{self.id} - {self.etat} - WO {self.workorder.id}"
    
# Pièces de rechange
class Piece(models.Model):
    nom = models.CharField(max_length=100)
    reference = models.CharField(max_length=100, unique=True)
    stock_disponible = models.PositiveIntegerField(default=0)
    fournisseur = models.CharField(max_length=100)
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=0
    )
    def __str__(self):
        return f"{self.nom} ({self.reference})"

# Piece utilisée
class PieceUtilisee(models.Model):

    etat = models.CharField(
    choices=[
        ("reservee", "Réservée"),
        ("consommee", "Consommée")
    ],
    default="reservee"
    )
    intervention = models.ForeignKey(
        Intervention,
        on_delete=models.CASCADE,
        related_name="pieces"
    )
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

    @property
    def cout_total(self):
        return self.quantite * self.piece.prix_unitaire

    def clean(self):
        if self.quantite <= 0:
            raise ValidationError("La quantité doit être positive.")
        if self.piece.stock_disponible < self.quantite:
            raise ValidationError("Stock insuffisant pour cette pièce.")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        self.full_clean()
        # décrémenter le 
        if is_new:
            self.piece.stock_disponible -= self.quantite
            self.piece.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantite} x {self.piece.nom} pour Intervention {self.intervention.id}"

# Rapports
class Rapport(models.Model):
    workorder = models.OneToOneField(WorkOrder, on_delete=models.CASCADE)
    contenu = models.TextField()
    fichier_pdf = models.FileField(upload_to="rapports/", null=True, blank=True)
    date_generation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rapport WO {self.workorder.id}"


# Logs
class Log(models.Model):
    class ActionChoices(models.TextChoices):
        CREATE = "create", "Création"
        UPDATE = "update", "Mise à jour"
        DELETE = "delete", "Suppression"
        START = "start", "Démarrage"
        FINISH = "finish", "Clôture"
        VALIDATE = "validate", "Validation"

    workorder = models.ForeignKey(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name="logs"
    )
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name="logs"
    )
    intervention = models.ForeignKey(  # ✅ ajout optionnel
        "Intervention",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logs"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logs"
    )

    action = models.CharField(max_length=50, choices=ActionChoices.choices, db_index=True)
    etat_intervention = models.CharField(max_length=50, blank=True, null=True)
    date_action = models.DateTimeField(default=timezone.now, db_index=True)

    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"[{self.date_action}] {self.user} - {self.action} (WO {self.workorder.id})"

# ajout de modèle AuditLog après la séparation de projet avec des couches
# nouvelle architecture (structure) de projet
# audit avancé
class AuditLog(models.Model):
    
    ACTIONS = (
        ("create", "Créer"),
        ("update", "Modifier"),
        ("delete", "Supprimer"),
        ("validate", "Valider"),
        ("start", "Démarrer"),
        ("finish", "Términer"),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTIONS)
    # action = models.CharField(max_length=10, choices=ACTIONS)
    # héritage = services.audit_service.log_action
    # action = models.CharField(max_length=20)

    model = models.CharField(max_length=100)
    object_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    endpoint = models.CharField(max_length=255, null=True, blank=True)
    method = models.CharField(max_length=10, null=True, blank=True)
    
    changements = models.JSONField(null=True, blank=True)

    def __str__(self):
        #return f"{self.user} {self.action} {self.model_name}"
        return f"{self.user} {self.action} {self.model} {self.object_id}"
    

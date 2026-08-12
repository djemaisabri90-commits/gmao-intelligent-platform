# maintenance/views/utilisateur_views.py
# À ajouter dans vos imports en haut du fichier :
from rest_framework.throttling import AnonRateThrottle, SimpleRateThrottle
from rest_framework.decorators import throttle_classes

from rest_framework.decorators import api_view

import re
from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

import io
from django.http import FileResponse
from maintenance.base.permissions import IsAdmin # Ou votre permission d'administration
# Importations spécifiques à ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
#from django.contrib.auth.decorators import user_passes_test

from maintenance.base.permissions import IsAdmin, IsAdminOrExpert
from maintenance.models import PasswordResetRequest, Utilisateur
from maintenance.serializers.utilisateur_serializer import (
    UtilisateurReadSerializer,
    UtilisateurWriteSerializer,
)
from maintenance.selectors.utilisateur_selectors import get_utilisateurs
from maintenance.services.audit_service import audit_action
from maintenance.services.utilisateur_service import (
    create_utilisateur,
    update_utilisateur,
    delete_utilisateur,
)

def validate_password_strength(value):
        errors = []
        if len(value) < 8:
            errors.append("Le mot de passe doit contenir au moins 8 caractères.")
        if not re.search(r"[A-Z]", value):
            errors.append("Le mot de passe doit contenir au moins une majuscule.")
        if not re.search(r"[a-z]", value):
            errors.append("Le mot de passe doit contenir au moins une minuscule.")
        if not re.search(r"\d", value):
            errors.append("Le mot de passe doit contenir au moins un chiffre.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            errors.append("Le mot de passe doit contenir au moins un caractère spécial.")

        if errors:
            raise ValidationError(errors)
        
# 🛡️ Sécurité : Limite l'utilisation abusive des requêtes de mot de passe (Anti-Brute Force)
class PasswordResetThrottle(SimpleRateThrottle):
    
    #Bloque les abus (20 requêtes/rush) par IP, 
    #que l'utilisateur soit connecté ou anonyme.
    
    scope = 'password_reset'
    rate = '3/minute'  # 🎯 SOLUTION : Déclaré ici pour être lu instantanément par DRF

    def get_cache_key(self, request, view):
        # Utilise l'adresse IP du client comme clé unique dans le cache
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }

class UtilisateurViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les utilisateurs.
    - Accessible uniquement aux admins pour la gestion complète
    - Endpoint `me` pour récupérer les infos de l'utilisateur connecté
    """
    
    permission_classes = [IsAuthenticated, IsAdminOrExpert]
    queryset = Utilisateur.objects.all()

    def get_queryset(self):
        return get_utilisateurs()

    def get_serializer_class(self):
        if self.action in ["create", "update", "delete", "partial_update"]:
            return UtilisateurWriteSerializer
        return UtilisateurReadSerializer
    
    def create(self, request, *args, **kwargs):

        # Validation avec le serializer d'écriture
        write_serializer = UtilisateurWriteSerializer(
            data=request.data,
            context={"request": request}
        )

        write_serializer.is_valid(raise_exception=True)

        # Création via votre service métier
        user = create_utilisateur(
            write_serializer.validated_data
        )

        audit_action(request, "create", user)

        #print("TEMP PASSWORD =", getattr(user, "_temp_password_plain", None))

        # Réponse avec le serializer de lecture
        read_serializer = UtilisateurReadSerializer(
            user,
            context={"request": request}
        )

        return Response(
            read_serializer.data,
            status=status.HTTP_201_CREATED
        )

    """
    def perform_create(self, serializer):
        
        #Utilise le service pour créer un utilisateur.
    
        validated_data = serializer.validated_data
        user = create_utilisateur(validated_data)
        audit_action(self.request, "create", user)
        serializer.instance = user
        print("TEMP PASSWORD =", getattr(user, "_temp_password_plain", None)
    )
    """



    def perform_update(self, serializer):
        """
        Utilise le service pour mettre à jour un utilisateur.
        """
        utilisateur = self.get_object()
        validated_data = serializer.validated_data
        user = update_utilisateur(utilisateur, validated_data)
        audit_action(self.request, "update", user)
        serializer.instance = user

    def perform_destroy(self, instance):
        """
        Utilise le service pour supprimer un utilisateur.
        """
        audit_action(self.request, "delete", instance)
        delete_utilisateur(instance)
        
        

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    @throttle_classes([PasswordResetThrottle]) # ⚡ Évite le brute force du token
    def change_password(self, request, pk=None):
        """
        Endpoint pour changer le mot de passe d’un utilisateur connecté (via la bannière).
        - Exige l'activation_token de l'employé pour s'auto-valider sans l'admin.
        """
        user = self.get_object()
        activation_token = request.data.get("activation_token")
        new_password = request.data.get("password")
        
        if not new_password:
            return Response({"error": "Mot de passe requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        # ✅ Sécurité : seul l’utilisateur lui-même ou un admin peut appeler cet endpoint
        if request.user != user and request.user.role != "admin":
            return Response({"error": "Action non autorisée"}, status=status.HTTP_403_FORBIDDEN)

        # 🤖 VALIDATION AUTOMATIQUE : Si c'est l'utilisateur lui-même, il DOIT fournir son jeton unique
        if request.user == user:
            if not activation_token:
                return Response({"error": "Le code d'activation d'entreprise est requis."}, status=status.HTTP_400_BAD_REQUEST)
            if str(user.activation_token) != str(activation_token):
                return Response({"error": "Le code d'activation fourni est incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        # Validation de la force du mot de passe
        try:
            validate_password_strength(new_password)
        except ValidationError as e:
            return Response({"error": str(e.messages)}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)

        # ✅ Gestion des règles métiers d'origine
        if request.user == user:
            user.must_change_password = False  # Libéré définitivement, l'admin n'a rien à faire
        else:
            user.must_change_password = True   # Si un admin change le pass d'un autre, il doit le rechanger

        # 🔒 INVALIDATION SÉCURISÉE (IMPORTANT)
        user.activation_token = None
        user.temporary_password = None  # si tu l’utilises en DB

        user.save()
        return Response({"status": "Mot de passe changé avec succès"})
    
    @action(detail=False, methods=["post"], permission_classes=[AllowAny]) # 🔓 Changé à AllowAny pour permettre l'accès déconnecté
    @throttle_classes([PasswordResetThrottle])
    def change_password_by_username(self, request):
        """
        Endpoint global pour changer le mot de passe via l'username (Cas non connecté).
        L'utilisateur doit obligatoirement fournir son activation_token.
        L'admin peut aussi l'utiliser librement.
        """
        username = request.data.get("username")
        activation_token = request.data.get("activation_token")
        new_password = request.data.get("password")

        if not username or not new_password:
            return Response({"error": "Nom d'utilisateur et mot de passe requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Utilisateur.objects.get(username=username)
        except Utilisateur.DoesNotExist:
            # 🛡️ Sécurité : On renvoie la même erreur pour ne pas divulguer si un username existe ou pas
            return Response({"error": "Identifiants ou code d'activation invalides"}, status=status.HTTP_400_BAD_REQUEST)

        # 🤖 VALIDATION AUTOMATIQUE : Si ce n'est pas un admin connecté qui fait l'action, le token est OBLIGATOIRE
        is_admin = request.user.is_authenticated and request.user.role == "admin"
        if not is_admin:
            if not activation_token or str(user.activation_token) != str(activation_token):
                return Response({"error": "Identifiants ou code d'activation invalides"}, status=status.HTTP_400_BAD_REQUEST)

        # Validation de la complexité
        try:
            validate_password_strength(new_password)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)

        # ✅ Application de vos règles d'origine adaptées
        if is_admin:
            user.must_change_password = False  # L'admin force la réinitialisation propre
        else:
            user.must_change_password = False  # L'employé s'est auto-validé avec son token secret !

        # 🔒 nettoyage sécurité
        user.activation_token = None
        user.temporary_password = None

        user.save()
        return Response({"status": "Mot de passe changé avec succès"})


    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Endpoint pour récupérer les infos de l'utilisateur connecté.
        Inclut must_change_password pour que le frontend sache s’il doit
        forcer le changement de mot de passe.
        """
        serializer = UtilisateurReadSerializer(request.user)
        return Response(serializer.data)
    



    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated, IsAdmin])
    def export_activation_pdf(self, request):
        """
        Génère un flux PDF contenant les fiches individuelles d'activation 
        pour tous les utilisateurs n'ayant pas encore réinitialisé leur mot de passe.
        """
        # 1. Extraction des utilisateurs non activés via l'ORM
        utilisateurs_inactifs = self.get_queryset().filter(must_change_password=True, is_active=True)
        
        if not utilisateurs_inactifs.exists():
            return Response(
                {"error": "Aucun compte en attente d'activation initiale trouvé."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. Création d'un buffer en mémoire pour stocker le PDF sans surcharger le disque
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter,
            rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # 🎨 Styles typographiques corporatifs pour le mémoire PFE
        title_style = ParagraphStyle(
            'FicheTitle', parent=styles['Heading1'], fontSize=16, leading=20, 
            textColor='#1e3a8a', alignment=TA_CENTER, spaceAfter=10
        )
        label_style = ParagraphStyle(
            'FicheLabel', parent=styles['Normal'], fontSize=11, leading=15, textColor='#374151'
        )
        token_style = ParagraphStyle(
            'FicheToken', parent=styles['Code'], fontSize=14, leading=18, 
            textColor='#b91c1c', alignment=TA_CENTER, fontName='Helvetica-Bold',
            spaceBefore=8, spaceAfter=8
        )
        instruction_style = ParagraphStyle(
            'FicheInstruction', parent=styles['Italic'], fontSize=9, leading=13, 
            textColor='#4b5563', alignment=TA_LEFT
        )

        # 3. Construction des fiches individuelles détachables
        for index, user in enumerate(utilisateurs_inactifs):
            role_label = user.get_role_display() if hasattr(user, 'get_role_display') else user.role
            cat_label = user.categorie.get_nom_display() if (user.role == "technicien" and user.categorie) else "N/A"
            
            # Bloc d'en-tête de la fiche
            story.append(Paragraph(f"<b>GROUPE DELICE BOUSALEM</b>", title_style))
            story.append(Paragraph(f"<b>FICHE D'ACTIVATION INITIALE — GMAO INTELLIGENTE</b>", title_style))
            story.append(Spacer(1, 10))
            
            # Informations de l'employé
            story.append(Paragraph(f"<b>Nom & Prénom :</b> {user.last_name.upper()} {user.first_name}", label_style))
            story.append(Paragraph(f"<b>Profil / Rôle :</b> {role_label} (Catégorie : {cat_label})", label_style))
            story.append(Paragraph(f"<b>Identifiant de connexion (Username) :</b> <font color='#1e40af'><b>{user.username}</b></font>", label_style))
            
            story.append(Spacer(1, 5))
            story.append(Paragraph(f"VOTRE CODE DE VALIDATION UNIQUE À SAISIR SUR LA BANNIÈRE :", label_style))
            
            # Affichage du jeton cryptographique généré automatiquement par le signal
            story.append(Paragraph(f"{user.activation_token}", token_style))
            story.append(Spacer(1, 3))
            story.append(Paragraph(f"VOTRE MOT DE PASSE TEMPORAIRE QUE VOUS DEVEZ LE CHANGER :", label_style))
            story.append(Paragraph(f"{user.temporary_password}", token_style))
            
            # Consignes de sécurité d'usine
            story.append(Paragraph(
                "<i>Consigne de sécurité : Connectez-vous à la plateforme avec vos identifiants temporaires, "
                "cliquez sur l'alerte de sécurité, puis saisissez ce code d'activation pour configurer votre "
                "mot de passe définitif. Cette fiche est strictement personnelle.</i>", 
                instruction_style
            ))
            story.append(Spacer(1, 15))
            
            # ✂️ Ligne pointillée de découpe (sauf pour le tout dernier élément)
            if index < len(utilisateurs_inactifs) - 1:
                story.append(HRFlowable(
                    width="100%", thickness=1, color="#9ca3af", 
                    spaceBefore=15, spaceAfter=20, hAlign='CENTER', dash=[4, 4]
                    #vgap obsolète supprimé/ dash(4,4) 4points 4espace
                ))

        # 4. Compilation et envoi du fichier
        doc.build(story)
        buffer.seek(0)
        
        return FileResponse(
            buffer, 
            as_attachment=True, 
            filename="fiches_activation_ouvriers.pdf", 
            content_type='application/pdf'
        )
    
    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated, IsAdmin])
    def export_reset_pdf(self, request, pk=None):
        """
        Génère un flux PDF contenant les fiches individuelles d'activation 
        pour tous les utilisateurs n'ayant pas encore réinitialisé leur mot de passe.
        """
        # 1. Extraction des utilisateurs non activés via l'ORM
        user = self.get_object()
        
        

        # 2. Création d'un buffer en mémoire pour stocker le PDF sans surcharger le disque
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter,
            rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # 🎨 Styles typographiques corporatifs pour le mémoire PFE
        title_style = ParagraphStyle(
            'FicheTitle', parent=styles['Heading1'], fontSize=16, leading=20, 
            textColor='#1e3a8a', alignment=TA_CENTER, spaceAfter=10
        )
        label_style = ParagraphStyle(
            'FicheLabel', parent=styles['Normal'], fontSize=11, leading=15, textColor='#374151'
        )
        token_style = ParagraphStyle(
            'FicheToken', parent=styles['Code'], fontSize=14, leading=18, 
            textColor='#b91c1c', alignment=TA_CENTER, fontName='Helvetica-Bold',
            spaceBefore=8, spaceAfter=8
        )
        instruction_style = ParagraphStyle(
            'FicheInstruction', parent=styles['Italic'], fontSize=9, leading=13, 
            textColor='#4b5563', alignment=TA_LEFT
        )

        # 3. Construction des fiches individuelles détachables
        role_label = user.get_role_display() if hasattr(user, 'get_role_display') else user.role
        cat_label = user.categorie.get_nom_display() if (user.role == "technicien" and user.categorie) else "N/A"
            
            # Bloc d'en-tête de la fiche
        story.append(Paragraph(f"<b>GROUPE DELICE BOUSALEM</b>", title_style))
        story.append(Paragraph(f"<b>FICHE D'ACTIVATION — GMAO INTELLIGENTE</b>", title_style))
        story.append(Spacer(1, 10))
            
            # Informations de l'employé
        story.append(Paragraph(f"<b>Nom & Prénom :</b> {user.last_name.upper()} {user.first_name}", label_style))
        story.append(Paragraph(f"<b>Profil / Rôle :</b> {role_label} (Catégorie : {cat_label})", label_style))
        story.append(Paragraph(f"<b>Identifiant de connexion (Username) :</b> <font color='#1e40af'><b>{user.username}</b></font>", label_style))
            
        story.append(Spacer(1, 5))
        story.append(Paragraph(f"VOTRE CODE DE VALIDATION UNIQUE À SAISIR SUR LA BANNIÈRE :", label_style))
            
            # Affichage du jeton cryptographique généré automatiquement par le signal
        story.append(Paragraph(f"{user.activation_token}", token_style))
        story.append(Spacer(1, 3))
        story.append(Paragraph(f"VOTRE MOT DE PASSE TEMPORAIRE QUE VOUS DEVEZ LE CHANGER :", label_style))
        story.append(Paragraph(f"{user.temporary_password}", token_style))
            
            # Consignes de sécurité d'usine
        story.append(Paragraph(
                "<i>Consigne de sécurité : Connectez-vous à la plateforme avec vos identifiants temporaires, "
                "cliquez sur l'alerte de sécurité, puis saisissez ce code d'activation pour configurer votre "
                "mot de passe définitif. Cette fiche est strictement personnelle.</i>", 
                instruction_style
            ))
        story.append(Spacer(1, 15))
            
            # ✂️ Ligne pointillée de découpe (sauf pour le tout dernier élément)
    
        story.append(HRFlowable(
            width="100%", thickness=1, color="#9ca3af", 
            spaceBefore=15, spaceAfter=20, hAlign='CENTER', dash=[4, 4]
            #lingne pointilée : vgap obsolète supprimé/ dash(4,4) 4points 4espace
        ))

        # 4. Compilation et envoi du fichier
        doc.build(story)
        buffer.seek(0)
        
        return FileResponse(
            buffer, 
            as_attachment=True, 
            filename=f"fiche_activation_{user.username}.pdf", 
            content_type='application/pdf'
        )
    
    
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def request_password_reset(self, request):
        username = request.data.get("username")

        if not username:
            return Response(
                {"error": "Nom d'utilisateur requis"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = Utilisateur.objects.get(username=username)
        except Utilisateur.DoesNotExist:
            # Évite de révéler si le compte existe ou non(max security)
            return Response(
                {"message": "Si le compte existe, la demande a été enregistrée."},
                status=status.HTTP_200_OK
            )
        # affhicher au soutenance inshallah
        """
        try:
            user = Utilisateur.objects.get(username=username)
            except Utilisateur.DoesNotExist:
            return Response(
                {"error": "Nom d'utilisateur introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )

            PasswordResetRequest.objects.create(user=user)

        return Response(
            {"message": "Votre demande a été transmise à l'administrateur."},
            status=status.HTTP_201_CREATED
        )
        """

        existing = PasswordResetRequest.objects.filter(
            user=user,
            status="pending"
        ).exists()

        if existing:
            return Response(
            {"error": "Une demande est déjà en attente de traitement."},
            status=status.HTTP_400_BAD_REQUEST
            )

        PasswordResetRequest.objects.create(user=user)

        return Response(
            {"message": "Votre demande a été transmise à l'administrateur."},
            status=status.HTTP_201_CREATED
        )




"""
    @user_passes_test(lambda u: u.is_staff)
    def export_activation_tokens_pdf(request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="fiches_activation.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
    
        # Style personnalisé pour le code
        code_style = ParagraphStyle(
            'CodeStyle',
            parent=styles['Heading2'],
            fontSize=14,
            leading=18,
            textColor='#d32f2f' # Rouge alerte
        )

        inactive_users = Utilisateur.objects.filter(is_active=False, must_change_password=True)

        for user in inactive_users:
            story.append(Paragraph(f"<b>Fiche d'activation GMAO - {user.role}</b>", styles['Title']))
            story.append(Spacer(1, 15))
            story.append(Paragraph(f"Employé : {user.first_name} {user.last_name}", styles['Normal']))
            story.append(Paragraph(f"Identifiant de connexion : <b>{user.username}</b>", styles['Normal']))
            story.append(Spacer(1, 10))
            story.append(Paragraph(f"VOTRE CODE DE VALIDATION UNIQUE : {user.activation_token}", code_style))
            story.append(Spacer(1, 15))
            story.append(Paragraph("<i>Consigne : Connectez-vous sur la plateforme, saisissez ce code pour définir votre mot de passe définitif.</i>", styles['Italic']))
            story.append(Paragraph("-" * 80, styles['Normal'])) # Ligne de découpe
            story.append(Spacer(1, 30))

        doc.build(story)
        return response


    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def change_password(self, request, pk=None):
        
        #Endpoint pour changer le mot de passe d’un utilisateur.
        #- Si l’utilisateur change lui-même son mot de passe, must_change_password passe à False.
        #- Si c’est un admin qui change le mot de passe, must_change_password reste True.
        
        user = self.get_object()
        new_password = request.data.get("password")
        if not new_password:
            return Response({"error": "Mot de passe requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_password_strength(new_password)
        except ValidationError as e:
            return Response({"error": str(e.messages)}, status=status.HTTP_400_BAD_REQUEST)
        
        # ✅ sécurité : seul l’utilisateur ou un admin peut changer
        if request.user != user and request.user.role != "admin":
            return Response({"error": "Action non autorisée"}, status=status.HTTP_403_FORBIDDEN)

        user.set_password(new_password)

        # ✅ Si l’utilisateur connecté change son propre mot de passe
        if request.user == user:
            user.must_change_password = False
        else:
            # ✅ Si un admin change le mot de passe d’un autre utilisateur
            user.must_change_password = True

        user.save()
        return Response({"status": "Mot de passe changé avec succès"})

    @action(detail=False, methods=["post"], permission_classes=[IsAdmin])
    def change_password_by_username(self, request):
        username = request.data.get("username")
        new_password = request.data.get("password")

        if not username or not new_password:
            return Response({"error": "Nom d'utilisateur et mot de passe requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Utilisateur.objects.get(username=username)
        except Utilisateur.DoesNotExist:
            return Response({"error": "Utilisateur introuvable"}, status=status.HTTP_404_NOT_FOUND)

        try:
            validate_password_strength(new_password)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)


        # ✅ Cas 1 : non connecté → must_change_password reste True
        user.must_change_password = True
        if (request.user.role != "admin"):
            return Response({
            "error": "Action non autorisée" },
            status=403)
        
        # ✅ Exception : admin réinitialise → must_change_password = False
        if request.user.is_authenticated and request.user.role == "admin":
            user.must_change_password = False

        user.save()

        return Response({"status": "Mot de passe changé avec succès"})
"""
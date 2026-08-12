# maintenance/services/utilisateur_service.py
from maintenance.models import Utilisateur, Categorie
def create_utilisateur(validated_data):
    
    # 🎯 1. Extraction propre du mot de passe (fourni ou non par le Serializer)
    raw_password = validated_data.pop("password", None)
    
    # Récupération sécurisée des autres données métiers
    # DRF fournit déjà une instance de Categorie via le serializer

    categorie = validated_data.get("categorie")

    # 🎯 2. Création initiale via l'ORM sans passer le mot de passe s'il est vide/nul
    # Si raw_password est absent, le signal prendra le relais automatiquement à la sauvegarde

    user = Utilisateur.objects.create_user(
        username=validated_data["username"],
        first_name=validated_data["first_name"],
        last_name=validated_data["last_name"],
        email=validated_data.get("email", ""),
        password= None, # Configuré temporairement à None
        role=validated_data.get("role", "technicien"),
        telephone=validated_data.get("telephone", ""),
        categorie=categorie,
        activation_token=validated_data.get("activation_token")
    )


    # récupération du mot de passe créé par le signal
    user.generated_password = getattr(
        user,
        "_temp_password_plain",
        None
    )

    if raw_password and raw_password.strip():
        user.set_password(raw_password)

    user.must_change_password = True
    user.save()

    return user
"""
    # 🎯 3. Si l'administrateur a spécifié un mot de passe manuel dans le UserForm, on l'applique
    if raw_password and raw_password.strip():
        user.set_password(raw_password)
    
    # ✅ Obligation de changer le mot de passe à la première connexion
    user.must_change_password = True
    #user.is_active= True et False desactive
    user.save()
    return user
"""
def update_utilisateur(utilisateur, data):
    for attr, value in data.items():

        if attr == "categorie" and utilisateur.role == "technicien":

            # Cas 1 : ID (recommandé)
            if isinstance(value, int):
                utilisateur.categorie = Categorie.objects.get(id=value)

            # Cas 2 : instance déjà fournie par serializer
            elif isinstance(value, Categorie):
                utilisateur.categorie = value

            # Cas 3 : nom (fallback sécurisé)
            else:
                categorie = Categorie.objects.filter(nom=value.strip()).first()
                if not categorie:
                    raise ValueError(f"Categorie '{value}' introuvable")
                utilisateur.categorie = categorie

        elif attr == "password":
            utilisateur.set_password(value)
            utilisateur.must_change_password = True

        else:
            setattr(utilisateur, attr, value)

    utilisateur.save()
    return utilisateur

def delete_utilisateur(utilisateur):
    """
    Supprime un utilisateur.
    """
    utilisateur.delete()



    """
def create_utilisateur(validated_data):
    
    Crée un utilisateur avec gestion sécurisée du mot de passe,
    attribution de catégorie et obligation de changer le mot de passe.
    
    categorie = None
    if validated_data.get("role") == "technicien" and validated_data.get("categorie"):
        categorie_value = validated_data["categorie"]
        if isinstance(categorie_value, int):
            categorie = Categorie.objects.get(id=categorie_value)
        else:
            categorie = Categorie.objects.get(nom=categorie_value)

    user = Utilisateur.objects.create_user(
        username=validated_data["username"],
        email=validated_data.get("email", ""),
        password=validated_data["password"],
        role=validated_data.get("role", "technicien"),
        telephone=validated_data.get("telephone", ""),
        categorie=categorie,
    )


    categorie = validated_data.get("categorie")

    # 🎯 2. Création initiale via l'ORM sans passer le mot de passe s'il est vide/nul
    # Si raw_password est absent, le signal prendra le relais automatiquement à la sauvegarde


    user = Utilisateur.objects.create_user(
        username=validated_data["username"],
        email=validated_data.get("email", ""),
        password= None, # Configuré temporairement à None
        role=validated_data.get("role", "technicien"),
        telephone=validated_data.get("telephone", ""),
        categorie=categorie,
        activation_token=validated_data.get("activation_token")
    )

    user.must_change_password = True
    #user.is_active= True et False desactive
    user.save()
    return user
    """

    """
def update_utilisateur(utilisateur, data):
    #Met à jour un utilisateur avec gestion sécurisée du mot de passe et de la catégorie.
    
    for attr, value in data.items():
        if attr == "categorie" and utilisateur.role == "technicien":
            if isinstance(value, int):
                utilisateur.categorie = Categorie.objects.get(id=value)
            else:
                utilisateur.categorie = Categorie.objects.get(nom=value)
        elif attr == "password":
            utilisateur.set_password(value)  # ✅ hash sécurisé
            # ✅ Obligation de changer le mot de passe si modifié par admin
            utilisateur.must_change_password = True
        else:
            setattr(utilisateur, attr, value)
    
    for attr, value in data.items():
        if attr == "categorie" and utilisateur.role == "technicien":
            # Ici aussi, DRF fournit déjà une instance de Categorie
            utilisateur.categorie = value
        elif attr == "password":
            utilisateur.set_password(value)  # ✅ hash sécurisé
            utilisateur.must_change_password = True
        else:
            setattr(utilisateur, attr, value)

    utilisateur.save()
    return utilisateur
"""

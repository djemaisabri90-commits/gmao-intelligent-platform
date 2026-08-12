FR-Lang.
Installation avec Docker
Prérequis

Installer :

Docker Desktop
Git

Cloner le projet :

git clone https://github.com/djemaisabri90-commits/gmao-intelligent-platform.git
cd gmao-intelligent-platform

Créer le fichier d'environnement à partir du modèle :

copy .env.example .env

Sous Linux/macOS :

cp .env.example .env

Adapter ensuite les variables d'environnement.

Démarrer la plateforme

Construire les images :

docker compose build

Démarrer les services :

docker compose up -d

Vérifier l'état des conteneurs :

docker compose ps

Afficher les logs :

docker compose logs -f
🌐 Accès

Frontend :

http://localhost:3000

Backend API :

http://localhost:8000

API maintenance :

http://localhost:3000/api/maintenance/

API prédictive :

http://localhost:3000/predictive/
🗄️ PostgreSQL

La base de données PostgreSQL est persistée à l'aide d'un volume Docker :

postgres_data

Cela permet de conserver les données lorsque les conteneurs sont arrêtés ou recréés.

🔴 Redis

Redis est utilisé comme service d'infrastructure pour les fonctionnalités nécessitant une communication rapide et/ou temps réel.

Il est intégré au réseau Docker de la plateforme.

### Building and running your application

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://localhost:8000.

### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)

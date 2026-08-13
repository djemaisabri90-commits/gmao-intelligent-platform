# gmao-intelligent-platform
Intelligent CMMS (GMAO) platform with predictive maintenance, Django REST API, React, PostgreSQL, Redis and Docker.
# 🏭 GMAO Intelligent Platform

> Plateforme intelligente de Gestion de Maintenance Assistée par Ordinateur (GMAO) intégrant la maintenance prédictive, la gestion des interventions, le suivi des équipements, la gestion des pièces, l'audit et un module de maintenance prédictive basé sur le Machine Learning.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)
![React](https://img.shields.io/badge/React-TypeScript-blue?logo=react)
![Vite](https://img.shields.io/badge/Vite-7-purple?logo=vite)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7-red?logo=redis)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)
![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-green?logo=nginx)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-orange?logo=scikit-learn)

---

## 📌 Présentation

Cette plateforme GMAO a été conçue pour centraliser et digitaliser les processus de maintenance industrielle.

Elle permet notamment de gérer :

- 👤 utilisateurs et rôles
- 🔐 authentification et contrôle d'accès
- 🏭 équipements et machines
- ⚠️ signalements d'incidents
- 📋 ordres de travail (Work Orders)
- 🔧 interventions de maintenance
- 📦 pièces de rechange et stock
- 📊 tableaux de bord opérationnels
- 📝 journaux d'audit
- 🔔 notifications
- 🤖 maintenance prédictive
- 📈 historique et évaluation des modèles Machine Learning

L'objectif est de proposer une architecture modulaire capable d'intégrer les processus opérationnels de maintenance avec des fonctionnalités d'analyse et de prédiction.

---

## 🔄 Méthodologie de développement

Le projet a été développé selon une approche **Agile Scrum**, avec une organisation en sprints successifs, un backlog fonctionnel, une priorisation des fonctionnalités, un développement incrémental ainsi que des phases régulières de tests et de validation.

# 🏗️ Architecture

La plateforme repose sur une architecture web modulaire conteneurisée avec Docker.

```text
                         ┌─────────────────────────┐
                         │       Utilisateur       │
                         │     Web Browser         │
                         └────────────┬────────────┘
                                      │
                                      │ HTTP
                                      ▼
                         ┌─────────────────────────┐
                         │      React + Vite       │
                         │       TypeScript        │
                         │        Frontend         │
                         └────────────┬────────────┘
                                      │
                                      │ /api
                                      ▼
                         ┌─────────────────────────┐
                         │         Nginx           │
                         │     Web Server / Proxy  │
                         └────────────┬────────────┘
                                      │
                                      │ HTTP / ASGI
                                      ▼
                    ┌─────────────────────────────────┐
                    │          Django REST API        │
                    │                                 │
                    │  Authentication / RBAC          │
                    │  Maintenance                    │
                    │  Work Orders                    │
                    │  Interventions                  │
                    │  Inventory                      │
                    │  Audit                          │
                    │  Notifications                  │
                    │  Predictive Maintenance         │
                    └──────────────┬──────────────────┘
                                   │
                 ┌─────────────────┼──────────────────┐
                 │                 │                  │
                 ▼                 ▼                  ▼
        ┌────────────────┐ ┌───────────────┐ ┌─────────────────┐
        │  PostgreSQL 16 │ │ Redis 7       │ │ Machine         │
        │                │ │               │ │ Learning        │
        │ Main database  │ │ Cache /       │ │ scikit-learn    │
        │                │ │ messaging     │ │ Random Forest   │
        └────────────────┘ └───────────────┘ └─────────────────┘
Architecture Docker

L'application est entièrement conteneurisée.

                    Docker Compose
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
 ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
 │  Frontend   │   │   Backend   │   │ PostgreSQL  │
 │ React/Nginx │──▶│   Django    │──▶│     16      │
 └─────────────┘   └──────┬──────┘   └─────────────┘
                          │
                          ▼
                    ┌───────────┐
                    │   Redis   │
                    │     7     │
                    └───────────┘
Le réseau Docker permet aux différents services de communiquer entre eux par leurs noms de service.
Frontend

Le frontend est développé avec :

React
TypeScript
Vite
React Query
Tailwind CSS
Recharts
Axios
React Router

L'interface est organisée par fonctionnalités afin de favoriser la modularité et la maintenabilité.
Backend

Le backend repose sur :

Python 3.12
Django 4.2
Django REST Framework
Django Channels
Daphne
SimpleJWT
PostgreSQL
Redis

L'architecture backend est organisée autour de plusieurs responsabilités.
Cette séparation permet de distinguer notamment :

logique métier
accès aux données
API REST
sérialisation
événements
prédiction
tests
Authentification et sécurité

La plateforme utilise une authentification basée sur JWT.
Les principaux mécanismes comprennent :

JWT Access / Refresh Tokens
authentification des endpoints
contrôle d'accès basé sur les rôles (RBAC)
routes protégées côté frontend
permissions Django REST Framework
changement obligatoire du mot de passe lors de la première connexion
gestion de réinitialisation des identifiants
journalisation des événements d'audit

Les secrets et variables d'environnement ne sont pas versionnés dans Git.
Maintenance prédictive

La plateforme intègre un module de maintenance prédictive basé sur le Machine Learning.

Le modèle actuel utilise :

Random Forest Classifier

avec notamment :

scikit-learn
GridSearchCV
SMOTE
Random Over-Sampling
joblib
Pipeline
Données de maintenance
        │
        ▼
Préparation des données
        │
        ▼
Feature Engineering
        │
        ▼
Gestion du déséquilibre
(SMOTE / ROS)
        │
        ▼
GridSearchCV
        │
        ▼
Random Forest
        │
        ▼
Évaluation
        │
        ▼
Modèle validé
        │
        ▼
Prédiction du risque

Le système permet notamment de :

prédire le risque de défaillance
identifier les équipements à risque
visualiser les risques sur une carte
afficher les prochaines défaillances prédites
suivre l'historique des entraînements
comparer les métriques des modèles
effectuer un réentraînement
conserver les versions des modèles
Métriques

Le module exploite notamment :

Accuracy
F1-score
Balanced Accuracy
ROC-AUC
matrice de confusion
distribution des classes
📊 Tableaux de bord

La plateforme fournit plusieurs vues permettant de suivre l'activité de maintenance.

Dashboard opérationnel
nombre de machines
signalements
ordres de travail
interventions
coûts de maintenance
état du stock
indicateurs de performance
Dashboard prédictif
historique des entraînements
métriques des modèles
comparaison des performances
distribution des classes
matrice de confusion
cartographie des risques
dates de défaillance prédites
version du modèle
🔄 Workflow de maintenance

Le processus principal suit une chaîne structurée :

Signalement
     │
     ▼
Validation
     │
     ▼
Work Order
     │
     ▼
Affectation
     │
     ▼
Intervention
     │
     ▼
Démarrage
     │
     ▼
Fin d'intervention
     │
     ▼
Validation
     │
     ▼
Verrouillage
     │
     ▼
Clôture

Cette approche permet de contrôler le cycle de vie d'une opération de maintenance et d'assurer la traçabilité des actions.

🧪 Tests

Le projet comprend une suite de tests couvrant notamment :

authentification
JWT
utilisateurs
machines
signalements
Work Orders
interventions
pièces
notifications
audit
maintenance prédictive
entraînement des modèles
sécurité
workflows métier

Les tests ont été exécutés avec succès dans l'environnement du projet.

📁 Structure générale du projet
gmao/
│
├── .dockerignore
├── .env.example
├── .gitignore
│
├── Dockerfile
├── Dockerfile.frontend
├── compose.yaml
├── requirements.txt
├── README.Docker.md
│
├── main_interface/
│   └── React / TypeScript / Vite
│
└── main_pro/
    ├── main_pro/
    ├── maintenance/
    ├── predictive/
    └── templates

🎓 Contexte académique

Projet réalisé dans le cadre d'un projet de fin d'études de Master professionnel.

Domaine :

Gestion de maintenance industrielle — Transformation numérique — Intelligence artificielle — Maintenance prédictive

Le projet combine des compétences en :

développement web
architecture logicielle
bases de données
cybersécurité
Cloud / conteneurisation
Machine Learning
conception d'API
tests logiciels


👨‍💻 Auteur

Sabri Djemai

Développement logiciel · Architecture applicative · Cloud & Docker · Machine Learning · Cybersécurité

📄 Licence

Ce projet est actuellement destiné à un usage académique et de démonstration.

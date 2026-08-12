# gmao-intelligent-platform
Intelligent CMMS (GMAO) platform with predictive maintenance, Django REST API, React, PostgreSQL, Redis and Docker.
# 🏭 GMAO Intelligent Platform

> Plateforme intelligente de Gestion de Maintenance Assistée par Ordinateur (GMAO) intégrant la maintenance corrective, la gestion des interventions, le suivi des équipements, la gestion des pièces, l'audit et un module de maintenance prédictive basé sur le Machine Learning.

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

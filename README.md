# 🌦️ Script de récupération de données météo – Sentinelle

Ce script Python permet de récupérer les données météorologiques quotidiennes depuis une API backend, elle-même alimentée par les données de la plateforme Windy.

📦 Fonctionnalité principale :
 - Envoie une requête à l’API `https://api.windy.com/api/point-forecast/v2`
 avec les paramètres suivants :

    `lat : latitude`

    `lon : longitude`

    `model : iconEu`

    `parameters : wind, windGust, ptype, lclouds, rh, temp, snowPrecip, pressure`

    `levels : surface`

    `key : clé API Windy (chargée depuis le .env)`

- Récupère et extrait les données météo au timestamp le plus proche de l’instant présent

- Renvoie les données sous forme de dictionnaire Python


## 📄 Données extraites
Les données récupérées sont automatiquement filtrées pour obtenir les valeurs météo au plus proche de l’instant présent, notamment :

- Température

- Vent (composantes u et v)

- Rafales

- Précipitations neigeuses (snowPrecip)

- Humidité relative

- Pression

- Types de précipitations (ptype)



## 🧱 Prérequis
Installez les dépendances avec :
```bash
pip install -r requirements.txt
```
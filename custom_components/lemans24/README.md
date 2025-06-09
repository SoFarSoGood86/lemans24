# 🏁 24 Heures du Mans - Intégration Home Assistant

Cette intégration Home Assistant vous permet de suivre en temps réel la course automobile des **24 Heures du Mans**, en utilisant les données fournies par l'API temps réel du WEC (Al Kamel Systems).

## ⚙️ Installation

1. Téléchargez le fichier ZIP ou clonez ce dépôt dans votre répertoire `custom_components` :
   ```bash
   custom_components/lemans24/
   ```

2. Ajoutez à votre fichier `configuration.yaml` :
   ```yaml
   sensor:
     - platform: lemans24
       api_key: VOTRE_CLE_API
       name: "24h du Mans"
       scan_interval: 00:00:30
   ```

3. Redémarrez Home Assistant.

## 📡 Capteurs disponibles

### 🏎️ Voitures
- `LeMans24 - Car #X`
  - `position` : Position actuelle en course
  - `team` : Écurie
  - `laps` : Nombre de tours complétés
  - `last_lap_time` : Temps du dernier tour
  - `best_lap_time` : Meilleur tour réalisé
  - `status` : En piste / Pit Stop / DNF

### 🥇 Leader
- `LeMans24 - Leader` : Nom et numéro de la voiture en tête

### 🚗 Total voitures
- `LeMans24 - Total Cars` : Nombre total de voitures encore en course

### 🕐 Temps restant
- `LeMans24 - Remaining Time` : Temps restant dans la course

### 🏁 Drapeaux
- `LeMans24 - Race Status` : État global de la course (green, yellow, red, FCY, SC)

### 🛠 Voitures au stand
- `LeMans24 - Cars in Pit` : Liste ou nombre de voitures aux stands

### 🌦 Météo (si disponible)
- `LeMans24 - Weather` : Température, humidité, pluie

## 🧪 Exemples d’automatisations

- Notifications si une voiture entre au stand
- Affichage sur écran e-ink d’un classement en temps réel
- Alerte si un drapeau rouge est levé

## 🧑‍💻 Développement

Cette intégration utilise les appels API de :
```
https://fiawec.alkamelsystems.com/api/live?apikey=VOTRE_CLE_API
```

Merci de respecter les conditions d'utilisation de l'API Al Kamel / WEC.

## 📬 Contact

Auteur : [Votre nom / GitHub]  
Licence : MIT  
Compatible : Home Assistant ≥ 2023.12  
Langage : Python 3.11+
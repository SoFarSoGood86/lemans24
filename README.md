# 🏁 Intégration Home Assistant – 24 Heures du Mans

[![HACS Support](https://img.shields.io/badge/HACS-Default-orange.svg)](https://hacs.xyz)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 🇫🇷 Description

Cette intégration personnalisée Home Assistant vous permet de suivre en temps réel toutes les informations officielles de la mythique course automobile des **24 Heures du Mans** :

- 🏎️ Position et classement des voitures
- ⏱️ Chronos, temps au tour, écarts
- 🟩🟨 Drapeaux de course (vert, jaune, safety car…)
- 👨‍👩‍👧‍👦 Équipes, pilotes, voitures et catégories
- ⏳ Temps restant dans la course

### 🧪 Fonctionnalités

- Intégration native dans Home Assistant via des entités de type `sensor`
- Rafraîchissement automatique des données depuis une API externe
- Prise en charge de [HACS](https://hacs.xyz) pour une installation facile

### 🛠️ Installation via HACS

1. Ajouter ce dépôt dans HACS :
   - **URL** : `https://github.com/SoFarSoGood86/home-assistant-lemans24`
   - **Type** : Intégration
2. Redémarrer Home Assistant
3. Configurer via `configuration.yaml` ou l’interface

### 🧾 Configuration YAML (exemple)

```yaml
sensor:
  - platform: lemans24
    api_key: VOTRE_CLÉ_API

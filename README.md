# 🔌 éCO2mix pour Home Assistant

Cette intégration Home Assistant vous permet d'accéder aux données RTE (Réseau de Transport d'Électricité) via l'API éCO2mix, offrant une vue détaillée du réseau électrique français.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![maintained](https://img.shields.io/maintenance/yes/2024.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![Dashboard Preview](https://raw.githubusercontent.com/lfpoulain/ha-eco2mix/refs/heads/main/images/dashboard.png)

## ✨ Fonctionnalités

- 📈 Suivi en temps réel de la consommation électrique
- 🔋 Détail de la production par source d'énergie
- 🔄 Monitoring des échanges internationaux (Import/Export)
- 📊 Visualisations dynamiques du mix énergétique
- 📱 Dashboard intégré et responsive
- ⚡ Conversion automatique en GigaWatts

## 📋 Prérequis

1. 🏠 Une installation Home Assistant fonctionnelle
2. 🛠️ HACS (Home Assistant Community Store)
3. 📊 Cartes personnalisées (via HACS) :
   - 📈 apexcharts-card
   - 🥧 pie-chart-card

## 🚀 Installation

### Via HACS (Recommandé) 

1. Dans HACS > Intégrations
2. Menu ⋮ > Dépôts personnalisés
3. Ajouter `https://github.com/lfpoulain/ha-eco2mix`
4. Sélectionner "Intégration"
5. Rechercher "éCO2mix"
6. Installer et redémarrer Home Assistant

![Installation Steps](https://raw.githubusercontent.com/lfpoulain/ha-eco2mix/refs/heads/main/images/installation.png)

### Installation Manuelle 🛠️

1. 📥 Télécharger le dépôt
2. 📁 Copier `custom_components/eco2mix` dans votre dossier `custom_components`
3. 🔄 Redémarrer Home Assistant

## ⚙️ Configuration

1. Aller dans Configuration > Intégrations
2. Cliquer sur le bouton "+" 
3. Rechercher "éCO2mix"
4. Sélectionner les capteurs souhaités

![Configuration Interface](https://raw.githubusercontent.com/lfpoulain/ha-eco2mix/refs/heads/main/images/config.png)


## 📊 Dashboard

Le dashboard est créé automatiquement avec :

### Vue Principale
![Main View](https://raw.githubusercontent.com/lfpoulain/ha-eco2mix/refs/heads/main/images/main_view.png)

- 📊 Valeurs principales en GW
- 📈 Graphique d'évolution 24h
- 🥧 Répartition de la production

### Sources d'Énergie Suivies

| Source | Icône |
|--------|-------|
| Nucléaire | ⚛️ |
| Éolien | 🌪️ |
| Solaire | ☀️ |
| Hydraulique | 💧 |
| Bioénergies | 🌱 |
| Gaz | 🔥 |
| Charbon | 🏭 |
| Fioul | 🛢️ |

## ❓ Dépannage

Si les données ne s'affichent pas :
1. 🔍 Vérifier votre connexion Internet
2. 📝 Consulter les logs Home Assistant
3. 🔄 Redémarrer Home Assistant

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- 🐛 Signaler des bugs
- 💡 Proposer des améliorations
- 🔧 Soumettre des pull requests

## 📫 Support

Besoin d'aide ? 
- 📝 Ouvrir une [Issue](https://github.com/lfpoulain/ha-eco2mix/issues)
- 💬 Rejoindre la discussion

## 👏 Crédits

- ⚡ Données : [RTE éCO2mix](https://www.rte-france.com/eco2mix)
- 🌐 API : [ODRE](https://odre.opendatasoft.com/)

## 📄 Licence

Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus de détails.

---
Made with ❤️ by [@lfpoulain](https://github.com/lfpoulain)
And with the generous help of [@piitaya](https://github.com/piitaya)

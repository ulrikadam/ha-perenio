# Perenio Smart Cameras for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/release/ulrik-adam/ha-perenio.svg)](https://github.com/ulrik-adam/ha-perenio/releases)
[![License](https://img.shields.io/github/license/ulrik-adam/ha-perenio.svg)](LICENSE)

Intégration Home Assistant pour les caméras Perenio Smart (PEIFC01 et autres modèles).

<p align="center">
  <img src="https://perenio.com/images/logo.png" alt="Perenio Logo" width="200"/>
</p>

## 📸 À propos

Cette intégration custom permet de connecter vos caméras Perenio Smart à Home Assistant via l'API cloud officielle Perenio. Elle supporte l'authentification OAuth2, la découverte automatique des caméras, les snapshots en temps réel et bien plus encore.

## ✨ Fonctionnalités

- ✅ **Authentification OAuth2** sécurisée avec l'API Perenio Cloud
- ✅ **Découverte automatique** de toutes vos caméras
- ✅ **Snapshots en temps réel** de vos caméras
- ✅ **Rafraîchissement automatique** des tokens (10 jours)
- ✅ **Interface de configuration** graphique intuitive
- ✅ **Support multi-caméras** - ajoutez autant de caméras que vous voulez
- ✅ **Attributs détaillés** - status, online, ID, modèle, firmware
- 🚧 **Streaming vidéo** (WebRTC - en développement)

## 📋 Caméras supportées

- ✅ **PEIFC01** - Indoor Fixed Camera 1080p
- ✅ **PEIRC01** - Indoor Motor Camera
- ✅ Autres modèles Perenio (non testés mais probablement compatibles)

## 🚀 Installation

### Via HACS (Recommandé)

1. Ouvrez **HACS** dans Home Assistant
2. Cliquez sur **"Integrations"**
3. Cliquez sur le menu **⋮** en haut à droite
4. Sélectionnez **"Custom repositories"**
5. Ajoutez l'URL : `https://github.com/ulrik-adam/ha-perenio`
6. Catégorie : **"Integration"**
7. Cliquez sur **"Add"**
8. Recherchez **"Perenio"** et installez
9. **Redémarrez** Home Assistant

### Installation Manuelle

1. Téléchargez la dernière version depuis [Releases](https://github.com/ulrik-adam/ha-perenio/releases)
2. Décompressez l'archive
3. Copiez le dossier `custom_components/perenio` dans votre dossier `config/custom_components/`
4. Redémarrez Home Assistant

## ⚙️ Configuration

1. Dans Home Assistant, allez dans **Paramètres** → **Appareils et services**
2. Cliquez sur **+ Ajouter une intégration**
3. Recherchez **"Perenio"**
4. Entrez votre **email** et **mot de passe** Perenio Smart
5. Cliquez sur **Soumettre**

🎉 Vos caméras apparaissent automatiquement !

## 📖 Documentation

- [Guide d'installation détaillé](custom_components/perenio/INSTALLATION.md)
- [Documentation complète](custom_components/perenio/README.md)
- [Exemples d'utilisation](#utilisation)

## 🎯 Utilisation

### Carte caméra simple

```yaml
type: picture-entity
entity: camera.perenio_camera_salon
camera_view: live
show_state: false
```

### Automatisation snapshot sur détection

```yaml
automation:
  - alias: "Photo quand mouvement détecté"
    trigger:
      platform: state
      entity_id: binary_sensor.mouvement_salon
      to: "on"
    action:
      service: camera.snapshot
      target:
        entity_id: camera.perenio_camera_salon
      data:
        filename: "/config/www/snapshots/{{ now().strftime('%Y%m%d_%H%M%S') }}.jpg"
```

### Notification avec snapshot

```yaml
automation:
  - alias: "Alerte mouvement avec photo"
    trigger:
      platform: state
      entity_id: binary_sensor.mouvement_salon
      to: "on"
    action:
      - service: camera.snapshot
        target:
          entity_id: camera.perenio_camera_salon
        data:
          filename: "/tmp/snapshot.jpg"
      - service: notify.mobile_app
        data:
          title: "🚨 Mouvement détecté"
          message: "Mouvement dans le salon"
          data:
            image: "/tmp/snapshot.jpg"
```

## 🔧 Configuration Avancée

### Modifier l'intervalle de mise à jour

```yaml
# configuration.yaml
perenio:
  scan_interval: 60  # En secondes (défaut: 30)
```

## 🐛 Dépannage

### Les caméras n'apparaissent pas

1. Vérifiez que vos identifiants sont corrects
2. Assurez-vous que les caméras sont bien connectées dans l'app Perenio
3. Regardez les logs : **Paramètres** → **Système** → **Logs**
4. Recherchez les erreurs contenant `perenio`

### Erreur "Invalid Auth"

- Vérifiez votre email et mot de passe
- Essayez de vous déconnecter/reconnecter dans l'app Perenio mobile
- Assurez-vous que votre compte n'est pas bloqué

### Pas de snapshot disponible

- Les snapshots nécessitent que la caméra soit en ligne
- Vérifiez l'état de la caméra dans l'app Perenio
- Certains modèles peuvent ne pas supporter les snapshots à la demande

### Logs utiles

```bash
# Voir les logs en temps réel
ha core logs -f | grep perenio
```

## 📡 Architecture Technique

```
┌─────────────────────┐
│  Home Assistant     │
│                     │
│  ┌───────────────┐  │
│  │ Perenio       │  │
│  │ Integration   │  │
│  └───────┬───────┘  │
└──────────┼──────────┘
           │
           │ OAuth2 + REST API
           │
           ▼
┌─────────────────────┐
│  Perenio Cloud      │
│                     │
│  • oauth.perenio.com│
│  • iot.perenio.com  │
└──────────┬──────────┘
           │
           │ WebSocket / WebRTC
           │
           ▼
┌─────────────────────┐
│  Caméra PEIFC01     │
│  (192.168.0.20)     │
└─────────────────────┘
```

### Endpoints API utilisés

- **OAuth** : `https://oauth.perenio.com/auth/realms/aaa.kaa`
- **API** : `https://iot.perenio.com/apif/api/v1`

## 🤝 Contribution

Les contributions sont les bienvenues ! 

1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 🧪 Développement

### Prérequis

- Python 3.11+
- Home Assistant 2023.1+

### Tests

```bash
# Installer les dépendances
pip install -r requirements_dev.txt

# Lancer les tests
pytest

# Vérifier le style
black custom_components/perenio
flake8 custom_components/perenio
```

## 📝 Changelog

### Version 0.1.0 (2025-01-06)

- 🎉 Version initiale
- ✅ Authentification OAuth2 avec client_secret
- ✅ Support des snapshots
- ✅ Découverte automatique des caméras
- ✅ Interface de configuration graphique

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- Merci à la communauté Home Assistant
- Merci à Perenio pour leurs caméras de qualité
- Développé avec ❤️ par [Ulrik Adam](https://github.com/ulrik-adam)

## ⚠️ Disclaimer

Ce projet n'est pas affilié à, approuvé par, ou en partenariat avec Perenio IoT. C'est un projet open-source développé par la communauté.

## 📞 Support

- 🐛 [Signaler un bug](https://github.com/ulrik-adam/ha-perenio/issues)
- 💬 [Discussions](https://github.com/ulrik-adam/ha-perenio/discussions)
- 📧 Email : ulrik.adam@gmail.com

## ⭐ Vous aimez cette intégration ?

N'hésitez pas à mettre une étoile sur GitHub ! ⭐

---

**Made with ❤️ for the Home Assistant community**

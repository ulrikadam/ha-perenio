# Perenio Smart Camera Integration for Home Assistant

Intégration custom pour connecter vos caméras Perenio Smart à Home Assistant via l'API cloud Perenio.

## ✨ Fonctionnalités

- ✅ Authentification OAuth2 avec l'API Perenio Cloud
- ✅ Découverte automatique des caméras
- ✅ Snapshots des caméras en temps réel
- ✅ Rafraîchissement automatique des tokens
- ✅ Support des modèles PEIFC01 et autres
- 🚧 Streaming vidéo (WebRTC - en développement)

## 📋 Prérequis

- Home Assistant 2023.1 ou plus récent
- Un compte Perenio Smart avec des caméras configurées
- L'application mobile Perenio Smart doit fonctionner correctement

## 📦 Installation

### Via HACS (Recommandé)

1. Ouvrez HACS dans Home Assistant
2. Cliquez sur "Integrations"
3. Cliquez sur le menu ⋮ en haut à droite
4. Sélectionnez "Custom repositories"
5. Ajoutez l'URL : `https://github.com/[votre-username]/ha-perenio`
6. Catégorie : `Integration`
7. Cliquez sur "Add"
8. Recherchez "Perenio" et installez
9. Redémarrez Home Assistant

### Installation Manuelle

1. Téléchargez ce repository
2. Copiez le dossier `custom_components/perenio` dans votre dossier `config/custom_components/`
3. Redémarrez Home Assistant

## ⚙️ Configuration

1. Dans Home Assistant, allez dans **Paramètres** → **Appareils et services**
2. Cliquez sur **+ Ajouter une intégration**
3. Recherchez **"Perenio"**
4. Entrez votre **email** et **mot de passe** Perenio Smart
5. Cliquez sur **Soumettre**

Vos caméras apparaîtront automatiquement ! 🎉

## 🎥 Utilisation

### Afficher une caméra sur le dashboard

```yaml
type: picture-entity
entity: camera.perenio_camera_salon
show_state: false
show_name: true
camera_view: live
```

### Prendre un snapshot automatiquement

```yaml
automation:
  - alias: "Snapshot à la détection de mouvement"
    trigger:
      - platform: state
        entity_id: binary_sensor.mouvement_salon
        to: "on"
    action:
      - service: camera.snapshot
        target:
          entity_id: camera.perenio_camera_salon
        data:
          filename: "/config/www/snapshots/salon_{{ now().strftime('%Y%m%d_%H%M%S') }}.jpg"
```

### Voir les enregistrements

Les vidéos enregistrées sur la carte SD de la caméra sont accessibles via les attributs de l'entité.

## 🔧 Configuration Avancée

### Modifier l'intervalle de mise à jour

Par défaut, l'intégration rafraîchit les données toutes les 30 secondes. Vous pouvez modifier cela dans `configuration.yaml` :

```yaml
perenio:
  scan_interval: 60  # En secondes
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

## 📡 API Endpoints

Cette intégration utilise les endpoints suivants :

- **OAuth** : `https://oauth.perenio.com/auth/realms/aaa.kaa`
- **API** : `https://iot.perenio.com/apif/api/v1`

## 🔐 Sécurité

- Vos identifiants sont stockés de manière sécurisée dans Home Assistant
- Les tokens OAuth sont automatiquement rafraîchis
- Aucune donnée n'est partagée avec des tiers

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Changelog

### Version 0.1.0 (2025-01-06)

- 🎉 Version initiale
- ✅ Authentification OAuth2
- ✅ Support des snapshots
- ✅ Découverte automatique des caméras

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- Merci à la communauté Home Assistant
- Merci à Perenio pour leurs caméras de qualité
- Développé avec ❤️ par Ulrik

## ⚠️ Disclaimer

Ce projet n'est pas affilié à, approuvé par, ou en partenariat avec Perenio IoT.

## 📞 Support

Pour toute question ou problème :

- Ouvrez une [issue sur GitHub](https://github.com/[votre-username]/ha-perenio/issues)
- Consultez les [discussions](https://github.com/[votre-username]/ha-perenio/discussions)

---

**Vous aimez cette intégration ?** ⭐ N'hésitez pas à mettre une étoile sur GitHub !

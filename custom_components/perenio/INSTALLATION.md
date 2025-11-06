# 🚀 Installation Rapide - Perenio pour Home Assistant

## Méthode 1 : Installation Manuelle (Recommandée pour les tests)

### 1. Copier les fichiers

```bash
# Sur votre serveur Home Assistant
cd /config
mkdir -p custom_components/perenio
```

Copiez tous les fichiers du dossier `perenio` dans `/config/custom_components/perenio/`

### 2. Redémarrer Home Assistant

```bash
# Via l'interface Web
Paramètres → Système → Redémarrer

# Ou en ligne de commande
ha core restart
```

### 3. Ajouter l'intégration

1. Paramètres → Appareils et services
2. + Ajouter une intégration
3. Rechercher "Perenio"
4. Entrer email et mot de passe Perenio Smart
5. Valider

## Méthode 2 : Via SSH/Terminal

```bash
# Télécharger directement sur le serveur
cd /config/custom_components
wget https://github.com/[votre-repo]/archive/main.zip
unzip main.zip
mv ha-perenio-main/perenio ./
rm -rf ha-perenio-main main.zip

# Redémarrer
ha core restart
```

## Vérification

Après redémarrage, vérifiez les logs :

```bash
ha core logs | grep perenio
```

Vous devriez voir :
```
INFO (MainThread) [custom_components.perenio] Successfully authenticated with Perenio
```

## Dépannage Rapide

### Erreur "Invalid Auth"
→ Vérifiez email/mot de passe dans l'app Perenio mobile

### Erreur "Cannot Connect"
→ Vérifiez votre connexion Internet
→ Testez : `ping oauth.perenio.com`

### Les caméras n'apparaissent pas
→ Ouvrez l'app Perenio et vérifiez que les caméras sont en ligne
→ Regardez les logs détaillés

## Prochaines étapes

1. Ajoutez une caméra sur votre dashboard
2. Créez des automatisations
3. Configurez des alertes
4. Profitez ! 🎉

## Besoin d'aide ?

- 📖 Lisez le [README complet](README.md)
- 🐛 [Ouvrez une issue](https://github.com/[votre-repo]/issues)
- 💬 [Discussions GitHub](https://github.com/[votre-repo]/discussions)

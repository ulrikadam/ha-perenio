# Contributing to Perenio Home Assistant Integration

Merci de votre intérêt pour contribuer à ce projet ! 🎉

## 🚀 Comment contribuer

### Signaler un bug

1. Vérifiez que le bug n'a pas déjà été signalé dans les [Issues](https://github.com/ulrik-adam/ha-perenio/issues)
2. Créez une nouvelle issue avec le template "Bug Report"
3. Incluez :
   - Version de Home Assistant
   - Version de l'intégration
   - Logs pertinents
   - Étapes pour reproduire le bug

### Proposer une fonctionnalité

1. Vérifiez que la fonctionnalité n'a pas déjà été proposée
2. Créez une nouvelle issue avec le template "Feature Request"
3. Décrivez clairement :
   - Le besoin
   - La solution proposée
   - Les alternatives envisagées

### Soumettre du code

1. **Fork** le repository
2. **Créez une branche** pour votre fonctionnalité
   ```bash
   git checkout -b feature/ma-super-fonctionnalite
   ```
3. **Codez** en suivant les conventions du projet
4. **Testez** vos modifications
5. **Committez** avec un message clair
   ```bash
   git commit -m "feat: ajoute support du streaming vidéo"
   ```
6. **Push** vers votre fork
   ```bash
   git push origin feature/ma-super-fonctionnalite
   ```
7. **Créez une Pull Request**

## 📋 Standards de code

### Style Python

- Suivez [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Utilisez `black` pour le formatage
- Utilisez `flake8` pour la vérification

```bash
black custom_components/perenio
flake8 custom_components/perenio
```

### Documentation

- Documentez toutes les fonctions publiques
- Utilisez des docstrings au format Google
- Mettez à jour le README si nécessaire

### Tests

- Ajoutez des tests pour les nouvelles fonctionnalités
- Assurez-vous que tous les tests passent

```bash
pytest tests/
```

## 🔍 Structure du projet

```
ha-perenio/
├── custom_components/
│   └── perenio/
│       ├── __init__.py       # Point d'entrée
│       ├── camera.py         # Entités caméra
│       ├── config_flow.py    # Configuration
│       ├── const.py          # Constantes
│       ├── manifest.json     # Métadonnées
│       ├── perenio_api.py    # Client API
│       └── strings.json      # Traductions
├── tests/                    # Tests unitaires
├── .gitignore
├── hacs.json                 # Config HACS
├── LICENSE
└── README.md
```

## 📝 Convention des commits

Utilisez [Conventional Commits](https://www.conventionalcommits.org/) :

- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage
- `refactor:` Refactoring
- `test:` Tests
- `chore:` Maintenance

Exemples :
```
feat: ajoute support du streaming WebRTC
fix: corrige l'authentification OAuth2
docs: met à jour le README avec exemples
```

## 🧪 Tests

### Exécuter les tests

```bash
# Tous les tests
pytest

# Tests spécifiques
pytest tests/test_camera.py

# Avec couverture
pytest --cov=custom_components/perenio
```

### Écrire des tests

```python
import pytest
from custom_components.perenio.perenio_api import PerenioAPI

@pytest.mark.asyncio
async def test_authentication():
    """Test OAuth2 authentication."""
    api = PerenioAPI("test@example.com", "password")
    result = await api.async_authenticate()
    assert result is True
```

## 🌍 Traductions

Pour ajouter une nouvelle langue :

1. Copiez `custom_components/perenio/strings.json`
2. Créez `translations/LANGUE_CODE.json`
3. Traduisez les textes
4. Soumettez une PR

## ⚡ Développement local

### Configuration

```bash
# Cloner le repo
git clone https://github.com/ulrik-adam/ha-perenio.git
cd ha-perenio

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # ou `venv\Scripts\activate` sur Windows

# Installer les dépendances
pip install -r requirements_dev.txt

# Lier vers votre installation HA
ln -s $(pwd)/custom_components/perenio ~/.homeassistant/custom_components/
```

### Debugging

Ajoutez dans `configuration.yaml` :

```yaml
logger:
  default: info
  logs:
    custom_components.perenio: debug
```

## 🎯 Roadmap

### Priorités

- [ ] Support complet du streaming vidéo (WebRTC)
- [ ] Détection de mouvement
- [ ] Accès aux enregistrements carte SD
- [ ] Support PTZ (si disponible)
- [ ] Tests unitaires complets
- [ ] Documentation API complète

### Idées futures

- [ ] Support des notifications push
- [ ] Intégration avec Google Home / Alexa
- [ ] Mode offline avec cache
- [ ] Support multi-utilisateurs

## 📞 Questions ?

N'hésitez pas à :
- Ouvrir une [Discussion](https://github.com/ulrik-adam/ha-perenio/discussions)
- Me contacter : ulrik.adam@gmail.com

## 🙏 Remerciements

Merci à tous les contributeurs qui aident à améliorer ce projet !

---

**Happy coding! 🚀**

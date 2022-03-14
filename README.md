# accelerate-dojo-playground
Ce repo comporte :
- un script pour générer automatiquement des tags sur le repo actif
- les tags générés grâce à ce script

## Installation

### Créer son environnement virtuel

```sh
virtualenv -p python3 venv
```


### Installer les dépendances

```sh
pip3 install -r requirements
```

## Créer et utiliser un token github

Pour créer un nouveau token, aller sur son compte [github](https://github.com/settings/tokens/new). Seul la section *dépôt* peut être cochée.

Renseigner la variable `GITHUB_TOKEN` dans le fichier `.env`.

## Run

```sh
python main.py
```

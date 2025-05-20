# RamlPostman_Convertor

# Documentation : Analyse d'un fichier RAML et génération d'une collection Postman

## Introduction
Ce script permet de parser un fichier RAML, d'extraire ses informations principales et de générer une collection Postman pour faciliter l'interaction avec l'API documentée.

## Prérequis
Avant d'exécuter ce script, assurez-vous d'avoir installé les modules suivants :
- `argparse` (inclus dans la bibliothèque standard Python)
- `requests`
- `json`
- `yaml`

Vous pouvez les installer en exécutant :

```bash
pip install requests PyYAML
```
## Exécution du script

```bash
python script.py chemin_du_fichier.raml -key CLE_API [-n Nom_de_la_collection]
```

## Arguments
`-raml_file` : Chemin du fichier RAML à analyser.

`-key` : Clé API Postman pour l'authentification.

`-n` (optionnel) : Nom personnalisé de la collection dans Postman. Par défaut, il prend le titre défini dans le RAML.
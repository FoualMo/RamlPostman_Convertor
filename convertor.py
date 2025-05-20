import argparse
from Parser import Parser
import Postman

def parse_raml(file_path, api_key):
    """Analyse le fichier RAML et affiche les informations principales."""
    try:
        with open(file_path, 'r') as f:
            raml_data = Parser.parse_raml(f)
        
        print(f"Title: {raml_data.get('title', 'Non défini')}")
        print(f"Version: {raml_data.get('version', 'Non défini')}")
        print(f"API Key: {api_key}")
        
        print("\nRessources:")
        for resource in raml_data.get('resources', []):
            print(f"- {resource.get('uri', 'Inconnu')} ({', '.join(resource.get('methods', []))})")

        return raml_data

    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        return None
    except Exception as e:
        print(f"Erreur lors de l'analyse du fichier RAML : {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser un fichier RAML avec une clé API")
    parser.add_argument("raml_file", type=str, help="Chemin du fichier RAML à convertir")
    parser.add_argument("-key", type=str, required=True, help="Clé API Postman pour l'authentification")
    parser.add_argument("-n", type=str, required=False, help="Nom de la collection à avoir dans Postman - sinon title dans le RAML")

    args = parser.parse_args()

    try:
        raml_data = Parser.parse_raml(args.raml_file)
        if raml_data is None:
            raise RuntimeError("Impossible de parser le fichier RAML.")

        pm = Postman.Postman(args.key)
        items = Parser.build_postman_collection(raml_data)
        API_name = args.n if args.n else raml_data.get('title', 'Nom non défini')


        pm.create_collection(API_name, items)
        print("Collection Postman créée avec succès !")

    except Exception as e:
        print(f"Erreur inattendue : {e}")

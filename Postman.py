import requests
import json
from Utils import Utils


class Postman:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'X-Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        self.base_url = 'https://api.getpostman.com'
    

    def get_collections(self):
        """Retrieve all collections."""
        url = f"{self.base_url}/collections"
        response = requests.get(url, headers=self.headers,verify=False)
        if response.status_code == 200:
            return response.json()['collections']
        else:
            response.raise_for_status()

    def get_collection(self, collection_uid):
        """Retrieve a single collection by its UID."""
        url = f"{self.base_url}/collections/{collection_uid}"
        response = requests.get(url, headers=self.headers,verify=False)
        if response.status_code == 200:
            return response.json()['collection']
        else:
            response.raise_for_status()

    def run_collection(self, collection_uid, environment_uid=None):
        """Run a collection and return the results."""
        url = f"{self.base_url}/collections/{collection_uid}/run"
        payload = {
            "collection": collection_uid,
        }
        if environment_uid:
            payload['environment'] = environment_uid

        response = requests.post(url, headers=self.headers, data=json.dumps(payload),verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_environments(self):
        """Retrieve all environments."""
        url = f"{self.base_url}/environments"
        response = requests.get(url, headers=self.headers,verify=False)
        if response.status_code == 200:
            return response.json()['environments']
        else:
            response.raise_for_status()

    def find_collection_by_name(self, project_name):
        """Find a collection by project name."""
        collections = self.get_collections()
        for collection in collections:
            if project_name.lower() in collection['name'].lower():
                return collection['uid']
        raise ValueError(f"No collection found for project name: {project_name}")
    
    def download_collection(self, collection_uid):
        """Download a collection by its UID."""
        url = f"{self.base_url}/collections/{collection_uid}"
        response = requests.get(url, headers=self.headers,verify=False)
        response.raise_for_status()
        collection = response.json()
        name = self.get_collection(collection_uid)['info']['name']

        collection_path = f"{name}.json"
        with open(collection_path, 'w') as f:
            json.dump(collection, f, indent=4)
        Utils.h1(f"Collection {name} téléchargé avec succés")

    def get_environment(self, environment_uid):
        """Retrieve a single environment by its UID."""
        url = f"{self.base_url}/environments/{environment_uid}"
        response = requests.get(url, headers=self.headers,verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    

    def update_collection(self, collection_uid, jsonfile):
        url = f"{self.base_url}/collections/{collection_uid}"
        
        with open(jsonfile, "r") as file:
            data = json.load(file)

        response = requests.put(url, headers=self.headers, json=data, verify=False)

        if response.status_code == 200:
            print("La collection a été modifiée avec succès.")
            return response.json()
        else:
            print(f"Erreur lors de la mise à jour : {response.status_code} - {response.text}")
            return None



    
    def create_collection(self, name, items):
        """
        Crée une collection Postman avec un nom donné et une liste de requêtes (items).
        
        :param name: Nom de la collection
        :param items: Liste d'items (requêtes) à inclure dans la collection
        :return: UID de la collection créée
        """
        collection = {
            "collection": {
                "info": {
                    "name": name,
                    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
                },
                "item": items,
                "events" : self.Event(name),
                "variable": [
                            {
                        "key": "baseUrl",
                        "value": ""
                        }
                ]
            }
        }
        url = f"{self.base_url}/collections"
        response = requests.post(url, headers=self.headers, json=collection, verify=False)

        if response.status_code == 200: 
            Utils.h1(f"Collection '{name}' créée avec succès.")
            return response.json()['collection']['uid']
        else:
            print(f"Erreur lors de la création de la collection : {response.status_code} - {response.text}")
            response.raise_for_status()

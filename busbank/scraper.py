import requests

API_URL = "https://api.entur.org/anshar/1.0/rest/vm"

def get_geoposes() -> str:
    response = requests.get(API_URL, headers={
        "ET-ClientName": "busbank-miljohackknowit",
    })

    if response.status_code != 200:
        print("Whelp! Did not get 200 OK from entur API")
        return
    
    return response.text

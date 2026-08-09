from api.database.supabase_rest import supabase_get
import os
import requests


def headers():
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    return {
        "apikey": key,
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json"
    }


def save_memory(content):
    url = os.environ["SUPABASE_URL"] + "/rest/v1/memory"

    r = requests.post(
        url,
        headers=headers(),
        json={
            "content": content
        }
    )

    return r.status_code == 201 or r.status_code == 200


def load_memory():
    url = os.environ["SUPABASE_URL"] + "/rest/v1/memory?select=*"

    r = requests.get(
        url,
        headers=headers()
    )

    if r.status_code == 200:
        return r.json()

    return []

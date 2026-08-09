import os
import requests

def supabase_get(table):
    url = os.environ["SUPABASE_URL"] + f"/rest/v1/{table}"

    r = requests.get(
        url,
        headers={
            "apikey": os.environ["SUPABASE_SERVICE_KEY"],
            "Authorization": "Bearer " + os.environ["SUPABASE_SERVICE_KEY"]
        }
    )

    return {
        "status": r.status_code,
        "data": r.json()
    }

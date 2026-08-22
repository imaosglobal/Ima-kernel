from dotenv import load_dotenv
import os
import requests

load_dotenv(".env")

url=os.getenv("SUPABASE_URL")
key=os.getenv("SUPABASE_KEY")

headers={
    "apikey": key,
    "Authorization": f"Bearer {key}"
}

r=requests.get(
    url+"/rest/v1/",
    headers=headers
)


import os
import requests


def _headers():
    key = os.environ["SUPABASE_SERVICE_KEY"]

    return {
        "apikey": key,
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
    }


def _url(table):
    return os.environ["SUPABASE_URL"] + f"/rest/v1/{table}"


def supabase_get(table, params=None):
    r = requests.get(
        _url(table),
        headers=_headers(),
        params=params or {},
    )

    return {
        "status": r.status_code,
        "data": r.json(),
    }


def supabase_insert(table, data):
    r = requests.post(
        _url(table),
        headers={
            **_headers(),
            "Prefer": "return=representation",
        },
        json=data,
    )

    return {
        "status": r.status_code,
        "data": r.json(),
    }


def supabase_update(table, data, params=None):
    r = requests.patch(
        _url(table),
        headers={
            **_headers(),
            "Prefer": "return=representation",
        },
        params=params or {},
        json=data,
    )

    return {
        "status": r.status_code,
        "data": r.json(),
    }

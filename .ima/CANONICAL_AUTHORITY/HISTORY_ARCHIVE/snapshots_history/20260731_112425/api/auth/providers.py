import os

AUTH_STATE={
    "email_password":True,
    "google_oauth":bool(os.getenv("GOOGLE_CLIENT_ID")),
    "apple_signin":bool(os.getenv("APPLE_KEY")),
    "enterprise_sso":False
}

def get_auth_state():
    return AUTH_STATE

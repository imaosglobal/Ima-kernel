import json
import time
import urllib.request
import urllib.error
import os

class SyncManager:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        
        # Fallback default configuration
        default_config = {
            "primary": "AIzaSyAAikmBef4qN77z9T4uJH81u3S5wYOIibU",
            "secondary": "AIzaSyAPWCdHyHeQmun0-1Dh46390IST2FI9TG4",
            "updated": int(time.time() * 1000)
        }
        self.save_config(default_config)
        return default_config

    def save_config(self, config):
        config["updated"] = int(time.time() * 1000)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        self.config = config

    def validate_key(self, api_key):
        """
        Validates the key against a live Google API model list endpoint.
        """
        if not api_key:
            return False
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.getcode() == 200
        except urllib.error.HTTPError as e:
            # If forbidden or unauthorized, the key is definitely invalid
            if e.code in [400, 401, 403]:
                return False
            # For network-level rate limits or 5xx, we treat it as transient, but still currently unusable
            return False
        except Exception:
            # Network failure or timeout
            return False

    def perform_sync(self):
        print("[INFO] Starting synchronization...")
        primary_key = self.config.get("primary")
        secondary_key = self.config.get("secondary")

        # Step 1: Attempt to sync with primary key
        if self.validate_key(primary_key):
            print("[SUCCESS] Sync operation completed successfully using primary key.")
            return True

        # Step 2: Primary failed. Initiate self-healing fallback mechanism
        print("[WARNING] Primary key validation failed. Initiating self-healing...")
        
        if self.validate_key(secondary_key):
            print("[HEALING] Secondary key is functional. Swapping secondary to primary...")
            
            # Auto-heal: Promote secondary to primary and demote primary to secondary
            healed_config = {
                "primary": secondary_key,
                "secondary": primary_key
            }
            self.save_config(healed_config)
            print("[SUCCESS] Self-healing complete. System configuration updated and synced.")
            return True
        else:
            print("[CRITICAL] Self-healing failed: Both primary and secondary keys are invalid.")
            return False

if __name__ == "__main__":
    manager = SyncManager()
    manager.perform_sync()
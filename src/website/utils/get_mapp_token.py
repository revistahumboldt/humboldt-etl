import requests
import os

def get_mapp_token():
    try:
        client_id = os.getenv("MAPP_CLIENT_ID", "")
        client_secret = os.getenv("MAPP_CLIENT_SECRET", "")
        token_url = os.getenv("MAPP_TOKEN_URL", "")

        if not all([client_id, client_secret, token_url]):
            raise ValueError("Environment variables MAPP_CLIENT_ID, MAPP_CLIENT_SECRET e MAPP_TOKEN_URL must be configured.")

        response = requests.post(
            token_url,
            auth=(client_id, client_secret),
            headers={"Content-Type": "application/json"}
        )

        response.raise_for_status()
        return response.json()["access_token"]
    
    except requests.exceptions.HTTPError as err:
        print(f"Error HTTP: {err.response.status_code}")
        print(f"Message: {err.response.text}")
        raise
    except requests.exceptions.RequestException as err:
        print(f"Request error: {err}")
        raise
    except ValueError as err:
        print(f"Configuration error: {err}")
        raise
    except KeyError:
        print("Error: 'access_token' not found in API response.")
        raise


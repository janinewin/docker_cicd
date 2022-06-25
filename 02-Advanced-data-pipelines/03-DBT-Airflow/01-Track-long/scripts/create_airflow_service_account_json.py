import json
import os

PROJECT_ID = os.getenv("PROJECT_ID")
PRIVATE_KEY_ID = os.getenv("PRIVATE_KEY_ID")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CLIENT_EMAIL = os.getenv("CLIENT_EMAIL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_X509_CERT_URL = os.getenv("CLIENT_X509_CERT_URL")


def create_airflow_service_account_json():
    with open("/opt/airflow/.bigquery_keys/airflow-service-account.json", "w") as file:
        json.dump(
            {
                "type": "service_account",
                "project_id": PROJECT_ID,
                "private_key_id": PRIVATE_KEY_ID,
                "private_key": PRIVATE_KEY,
                "client_email": CLIENT_EMAIL,
                "client_id": CLIENT_ID,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": CLIENT_X509_CERT_URL,
            },
            file,
        )


if __name__ == "__main__":
    create_airflow_service_account_json()

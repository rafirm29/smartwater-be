import requests
import json

from config.config import settings
from schemas.notification import Notification

from google.oauth2 import service_account
import google.auth.transport.requests as google_request


def get_google_access_token(json_keyfile_path):
    credentials = service_account.Credentials.from_service_account_file(
        json_keyfile_path,
        scopes=["https://www.googleapis.com/auth/firebase.messaging"],
    )
    request = google_request.Request()

    credentials.refresh(request)

    access_token = credentials.token
    return access_token


def send_notification(device_token: str, payload: Notification):
    token = get_google_access_token(settings.PATH_TO_PRIVATE_KEY)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
    }

    body = {
        "message": {
            "token": device_token,
            "notification": {
                "title": payload.title,
                "body": payload.body
            },
            # "android": {
            #     "priority": "5"
            # },
        }
    }
    response = requests.post(
        "https://fcm.googleapis.com/v1/projects/ikanku-d709b/messages:send", headers=headers, data=json.dumps(body))

    return response

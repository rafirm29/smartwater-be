import requests
import json

from config.config import settings
from schemas.notification import Notification


def send_notification(device_token: str, payload: Notification):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + settings.FCM_SERVER_TOKEN,
    }

    body = {
        "message": {
            "token": device_token,
            "notification": {
                "title": payload.title,
                "body": payload.body
            },
            "android": {
                "priority": "5"
            },
        }
    }
    response = requests.post(
        "https://fcm.googleapis.com/v1/projects/ikanku-d709b/messages:send", headers=headers, data=json.dumps(body))

    return response

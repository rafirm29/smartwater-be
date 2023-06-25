import requests
import json

from config.config import settings
from schemas.notification import Notification


def send_notification(device_token: str, payload: Notification):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + settings.FCM_SERVER_TOKEN,
    }

    body = {
        'notification': payload.dict(),
        'to':
        device_token,
        'priority': 'high'
    }
    response = requests.post(
        "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))

    return response

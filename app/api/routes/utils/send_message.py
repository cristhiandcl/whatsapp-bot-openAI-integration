import requests
from json import dumps

from app.core.config import settings


def send_jarvis_response(recipient: str, jarvis_response: str):
    headers = {
        "Content-type" : "application/json",
        "Authorization": f"Bearer {settings.access_token}",
    }

    url = f"https://graph.facebook.com/{settings.version}/{settings.phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type"   : "individual",
        "preview_url"      : False,
        "to"               : recipient,
        "type"             : "text",
        "text"             : {"body": jarvis_response},
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Status:", response.status_code)
        print("Body:", response.text)
        return response
    else:
        print(response.status_code)
        print(response.text)
        return response

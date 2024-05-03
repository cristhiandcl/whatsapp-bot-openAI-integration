"""Merli answer Module"""
from fastapi import APIRouter
import requests
from app.core.config import settings

router = APIRouter()


@router.get("/")
async def test_whatsapp_connection():
    """Test whatsapp connection Endpoint"""

    url = f"https://graph.facebook.com/{settings.version}/{settings.phone_number_id}/messages"
    headers = {
        "Authorization": "Bearer " + settings.access_token,
        "Content-Type" : "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to"               : settings.recipient_waid,
        "type"             : "template",
        "template"         : {"name": "hello_world", "language": {"code": "en_US"}},
    }
    response = requests.post(url, headers=headers, json=data)

    return response.json()

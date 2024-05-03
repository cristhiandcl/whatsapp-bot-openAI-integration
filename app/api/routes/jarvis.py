"""Jarvis answer Module"""

from fastapi import APIRouter, Request, HTTPException, status
import logging

from openai_tools_gpt import ToolsGPT
from app.core.config import settings
from .utils.send_message import send_jarvis_response

context = [{"role"   : "system",
            "content": """You are Jarvis, my personal assistant expert on coding stuff, 
            I work on a mac with python most of the time, so unless the language is specified, 
            assume you are always asked about an implementation in python, you also answer question about general topics"""}]

router = APIRouter()
jarvis = ToolsGPT(with_memory=True, memory=context)


# FastAPI Routes
@router.get("/")
async def get_webhook(request: Request):
    """Whatsapp Webhook Connection validation"""

    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    # Check if a token and mode were sent
    if mode and token:
        # Check the mode and token sent are correct
        if mode == "subscribe" and token == settings.verify_token:
            # Respond with 200 OK and challenge token from the request
            logging.info("WEBHOOK_VERIFIED")
            return int(challenge)
        else:
            # Responds with '403 Forbidden' if verify tokens do not match
            logging.info("VERIFICATION_FAILED")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Verification failed")
    else:
        # Responds with '400 Bad Request' if verify tokens do not match
        logging.info("MISSING_PARAMETER")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing parameters")


@router.post("/")
async def post_webhook(request: Request):
    # Logic for handling POST requests
    body = await request.json()
    container = body["entry"][0]["changes"][0]["value"]

    if container.get("messages"):
        contact: str = container["messages"][0]["from"]
        message: str = container["messages"][0]["text"]["body"]
        response: str = jarvis.invoke(message)

        send_jarvis_response(contact, response)

    return {"status": "ok"}

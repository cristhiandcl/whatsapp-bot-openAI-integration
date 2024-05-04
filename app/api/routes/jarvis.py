"""Jarvis answer Module"""

from fastapi import APIRouter, Request, HTTPException, status
import logging

from app.core.config import settings
from .utils.send_message import send_jarvis_response
from app.api.deps import GPT
from app.database.mongo_config import mongo_collection

router = APIRouter()


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
async def post_webhook(gpt_data: GPT):
    # Logic for handling POST requests

    if gpt_data:
        jarvis = gpt_data["gpt"]
        response: str = jarvis.invoke(gpt_data["message"])
        send_jarvis_response(gpt_data["contact"], response)
        await mongo_collection.insert_one({"contact": gpt_data["contact"],
                                           "query"  : gpt_data["message"],
                                           "answer" : response})

    return {"status": "ok"}

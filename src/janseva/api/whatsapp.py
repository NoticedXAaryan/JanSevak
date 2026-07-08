"""FastAPI router for handling WhatsApp webhooks via Twilio."""

import logging

from fastapi import APIRouter, BackgroundTasks, Form, Request
from fastapi.responses import Response

from janseva.agents.service import process_message
from janseva.api.twilio_client import send_whatsapp_message

logger = logging.getLogger(__name__)

router = APIRouter()


async def handle_whatsapp_message(from_number: str, body: str):
    """Background task to process the message and send the reply."""
    try:
        # Twilio sends 'whatsapp:+14155238886'. We need an integer ID for our DB.
        # Strip non-numeric characters to create a pseudo-telegram-id.
        numeric_id = "".join(filter(str.isdigit, from_number))

        if not numeric_id:
            logger.error(f"Could not parse valid ID from WhatsApp number: {from_number}")
            return

        pseudo_telegram_id = int(numeric_id)

        # 1. Pass through the same exact AI agent pipeline as Telegram!
        response_text = await process_message(telegram_id=pseudo_telegram_id, user_text=body)

        # 2. Send the response back via Twilio API
        if len(response_text) > 1600:
            # Twilio WhatsApp character limit is 1600. Split if needed.
            for i in range(0, len(response_text), 1600):
                await send_whatsapp_message(from_number, response_text[i : i + 1600])
        else:
            await send_whatsapp_message(from_number, response_text)

    except Exception as e:
        logger.error(f"Error handling WhatsApp message: {e}")


@router.post("/webhook/twilio")
async def twilio_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    From: str = Form(...),
    Body: str = Form(...),
):
    """
    Webhook endpoint for Twilio incoming WhatsApp messages.
    Must return a 200 OK immediately, so we process the message in the background.
    """
    logger.info(f"Received WhatsApp message from {From}: {Body[:50]}...")

    # Process message in background to avoid Twilio timeout
    background_tasks.add_task(handle_whatsapp_message, From, Body)

    # Return empty TwiML response
    return Response(content="<Response></Response>", media_type="application/xml")

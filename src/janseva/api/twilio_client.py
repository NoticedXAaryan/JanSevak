"""Twilio REST API client for sending WhatsApp messages."""
import httpx
import logging
from typing import Optional

from janseva.config import settings

logger = logging.getLogger(__name__)

async def send_whatsapp_message(to_number: str, body: str, media_url: Optional[str] = None) -> bool:
    """
    Sends a WhatsApp message via the Twilio REST API.
    
    Args:
        to_number (str): The destination number (e.g. 'whatsapp:+1234567890' or just '+1234567890')
        body (str): The text message to send.
        media_url (str): Optional URL to a media file (image, audio, etc.)
    """
    if not settings.twilio_account_sid or not settings.twilio_auth_token:
        logger.warning("Twilio credentials not set. Cannot send WhatsApp message.")
        return False
        
    if not to_number.startswith("whatsapp:"):
        # Format if not already formatted
        to_number = f"whatsapp:{to_number}"
        
    url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.twilio_account_sid}/Messages.json"
    
    payload = {
        "To": to_number,
        "From": settings.twilio_whatsapp_number,
        "Body": body
    }
    
    if media_url:
        payload["MediaUrl"] = media_url

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                data=payload,
                auth=(settings.twilio_account_sid, settings.twilio_auth_token)
            )
            
            if response.status_code in (200, 201):
                logger.info(f"WhatsApp message sent successfully to {to_number}")
                return True
            else:
                logger.error(f"Failed to send WhatsApp message. Status: {response.status_code}, Body: {response.text}")
                return False
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        return False

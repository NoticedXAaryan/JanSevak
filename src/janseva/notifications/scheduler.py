"""Background task scheduler for notifications."""
import asyncio
import logging
from aiogram import Bot

from janseva.notifications.engine import broadcast_scheme_alert

logger = logging.getLogger(__name__)

async def check_for_new_schemes(bot: Bot):
    """
    Simulates checking a database or external API for new schemes, 
    and sends out alerts to users interested in those schemes.
    """
    logger.info("Running scheduled check for new schemes...")
    
    # In a real app, you would query the DB for schemes created since the last run.
    # For this hackathon, we simulate a new agriculture scheme if it's the first run or 
    # we just demonstrate the capability. We'll skip sending an actual mock message 
    # every cycle to avoid spamming real users, but the function is here.
    
    # Example logic:
    # new_schemes = await get_new_schemes_from_db()
    # for scheme in new_schemes:
    #     await broadcast_scheme_alert({
    #         "title": scheme.title,
    #         "description": scheme.summary,
    #         "interest_tag": scheme.category
    #     }, bot)
    
    pass

async def notification_scheduler_loop(bot: Bot, interval_seconds: int = 3600):
    """
    Run the notification checks periodically.
    """
    logger.info(f"Starting background notification scheduler (interval: {interval_seconds}s)")
    while True:
        try:
            await check_for_new_schemes(bot)
        except Exception as e:
            logger.error(f"Error in notification scheduler: {e}")
        
        await asyncio.sleep(interval_seconds)

def start_scheduler(bot: Bot):
    """Start the scheduler in the background."""
    asyncio.create_task(notification_scheduler_loop(bot, interval_seconds=3600))  # Run every hour

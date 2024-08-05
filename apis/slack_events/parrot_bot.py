import logging
from routers.slack import slack_app

logger = logging.getLogger(__name__)


# オウム返しBOT
@slack_app.event("message")
def handle_message_events(body, say, logger):
    logger.debug(f"Received event: {body}")
    event = body["event"]
    channel_type = event.get("channel_type")
    logger.info(f"Message received in channel type: {channel_type}")
    
    if channel_type == "im":
        logger.info("Responding to DM")
        say(event["text"] + " だがや")
    else:
        logger.info("Responding to channel message")
        say(event["text"] + " ですぞえ")
import logging
import sys
from src.config import get_settings
from src.youtube_client import YouTubeClient
from src.whatsapp_client import WhatsAppClient
from src.formatter import format_trailer_digest

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Initializing Hindi Movie Trailer Automation Pipeline...")
    settings = get_settings()

    if not all([settings.youtube_api_key, settings.evolution_api_url, settings.evolution_api_token, settings.evolution_instance, settings.whatsapp_recipient]):
        logger.error("Missing critical environment variables. Check your configuration parameters.")
        sys.exit(1)

    try:
        # Step 1: Fetch items from YouTube
        yt_client = YouTubeClient(api_key=settings.youtube_api_key)
        trailers = yt_client.fetch_hindi_movie_trailers()

        # Step 2: Format the content payload
        message_body = format_trailer_digest(trailers)

        # Step 3: Dispatch over WhatsApp via Evolution API
        wa_client = WhatsAppClient(
            api_url=settings.evolution_api_url,
            api_token=settings.evolution_api_token,
            instance=settings.evolution_instance
        )
        wa_client.send_message(recipient=settings.whatsapp_recipient, message=message_body)
        
        logger.info("Pipeline execution completed successfully.")
    except Exception as e:
        logger.exception(f"Pipeline failed with unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
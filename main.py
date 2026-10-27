import os
import logging
import sys
from dotenv import load_dotenv
from src.config import get_settings
from src.youtube_client import YouTubeClient
from src.whatsapp_client import WhatsAppClient
from src.formatter import format_trailer_digest

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

PROCESSED_LOG_FILE = "last_processed_trailers.txt"

def load_processed_ids() -> set:
    if not os.path.exists(PROCESSED_LOG_FILE):
        return set()
    with open(PROCESSED_LOG_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def save_processed_id(video_id: str):
    with open(PROCESSED_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{video_id}\n")

def main():
    logger.info("Initializing Hindi Movie Trailer Automation Pipeline...")
    settings = get_settings()

    if not all([settings.youtube_api_key, settings.evolution_api_url, settings.evolution_api_key, settings.whatsapp_number]):
        logger.error("Missing critical environment variables. Check your configuration parameters.")
        sys.exit(1)

    try:
        # Step 1: Fetch items from YouTube
        yt_client = YouTubeClient(api_key=settings.youtube_api_key)
        all_trailers = yt_client.fetch_hindi_movie_trailers()

        # Step 2: Filter out already processed trailers to avoid duplicates
        processed_ids = load_processed_ids()
        new_trailers = [t for t in all_trailers if t["video_id"] not in processed_ids]

        if not new_trailers:
            logger.info("No new unseen movie trailers found in the last 48 hours.")
            return

        # Step 3: Format the content payload for new trailers only
        message_body = format_trailer_digest(new_trailers)

        # Step 4: Dispatch over WhatsApp via Evolution API
        wa_client = WhatsAppClient(
            api_url=settings.evolution_api_url,
            api_token=settings.evolution_api_key
        )
        wa_client.send_message(recipient=settings.whatsapp_number, message=message_body)
        
        # Step 5: Mark these video IDs as processed
        for trailer in new_trailers:
            save_processed_id(trailer["video_id"])

        logger.info(f"Pipeline executed successfully. Dispatched {len(new_trailers)} new trailers.")
    except Exception as e:
        logger.exception(f"Pipeline failed with unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
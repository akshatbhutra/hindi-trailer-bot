import logging
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class WhatsAppClient:
    def __init__(self, api_url: str, api_token: str):
        self.api_url = api_url.rstrip("/")
        self.api_token = api_token

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=2, max=10))
    def send_message(self, recipient: str, message: str) -> bool:
        """
        Sends a text message using the simplified Evolution API endpoint.
        """
        headers = {
            "apikey": self.api_token,
            "Content-Type": "application/json"
        }
        payload = {
            "number": recipient,
            "text": message
        }

        logger.info(f"Sending WhatsApp message via Evolution API to {recipient}")
        response = requests.post(self.api_url, json=payload, headers=headers, timeout=15)
        
        if response.status_code in [200, 201]:
            logger.info("WhatsApp message successfully dispatched.")
            return True
        else:
            logger.error(f"Failed to send WhatsApp message. Status: {response.status_code}, Response: {response.text}")
            response.raise_for_status()
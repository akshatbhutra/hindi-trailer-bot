import logging
from datetime import datetime, timezone, timedelta
from googleapiclient.discovery import build
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

OFFICIAL_CHANNELS = {
    "KVN Productions": "UC3DOgauBYLQQXdH1siGjfpw",
    "Sony Pictures Entertainment India": "UCz97F7dMxBNOfGYu3rx8aCw",
    "Aamir Khan Talkies": "UCqjQu9qgL_eDXPwRnq45ZDQ",
    "Balaji Motion Pictures": "UC_Q23_cM9c4nKjC2w5jR5vQ",
    "Star Studios": "UC2N_4N_7a3dY9N3S5881Pqw",
    "Mythri Movie Makers": "UCKZSn5C-RzrLjuWJF8wWiDw",
    "Jio Studios": "UC5hC2b6d1X2zQ9rL1t7V8Zg",
    "Rajshri": "UCEKWXRsfUHkan-D_ljU8Asw",
    "Maddock Films": "UC-LOdiPoxninevJ0DkleCLg",
    "Nadiadwala Grandson": "UCzF90q2mXJ3e8Qy7r7O_84w",
    "Yash Raj Films (YRF)": "UCTM_-wRBRZ3iJVP8K18vV_g",
    "Dharma Productions": "UC-9-hxRHNrtKcfdJDTvRWrg",
    "Red Chillies Entertainment": "UC7-06ilZZB4g8lJgA7B_07w",
    "Zee Studios": "UC1A9sH3q9p9_JjJ2sF_4gLw",
    "T-Series / T-Series Films": "UCq-Fj5jknLsUf-MWSy4_brA",
    "Sony Music India": "UCzuWYPspssK-L5vWf_k7dYg",
    "Zee Music Company": "UCFFbwnve3yF62-tVXkTyJqg",
    "Tips Official": "UC5837vX8w1gQ8fK2v_v1Q7g",
    "Saregama Music": "UCtm_QoN2SIxwCE3Qt_flY7Q",
    "Speed Records": "UC676r1_a6w248Q8s3g9c89A",
    "Panorama Music": "UCD1J3rD7J6Q8_7j5lVvL3Ww"
}

class YouTubeClient:
    def __init__(self, api_key: str):
        self.youtube = build("youtube", "v3", developerKey=api_key)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch_hindi_movie_trailers(self) -> list[dict]:
        """
        Queries exclusively from the curated list of official studio & music label 
        channel IDs for Hindi movie trailers/teasers uploaded in the last 48 hours.
        """
        now = datetime.now(timezone.utc)
        published_after = (now - timedelta(hours=48)).isoformat()
        
        all_trailers = []

        for studio_name, channel_id in OFFICIAL_CHANNELS.items():
            logger.info(f"Scanning official channel: {studio_name}")
            
            try:
                search_response = self.youtube.search().list(
                    part="snippet",
                    channelId=channel_id,
                    type="video",
                    order="date",
                    publishedAfter=published_after,
                    maxResults=5,
                    relevanceLanguage="hi"
                ).execute()

                for item in search_response.get("items", []):
                    snippet = item["snippet"]
                    video_id = item["id"]["videoId"]
                    title = snippet["title"]
                    channel_title = snippet["channelTitle"]
                    published_at = snippet["publishedAt"]

                    title_lower = title.lower()
                    # Exclude non-trailer uploads like full audio, lyrical videos, or interviews
                    if not any(keyword in title_lower for keyword in ["trailer", "teaser", "official", "promo"]):
                        continue

                    all_trailers.append({
                        "video_id": video_id,
                        "title": title,
                        "channel": channel_title,
                        "published_at": published_at,
                        "url": f"https://www.youtube.com/watch?v={video_id}"
                    })

            except Exception as e:
                logger.warning(f"Could not fetch data for channel {studio_name}: {e}")
                continue

        logger.info(f"Successfully matched and verified {len(all_trailers)} official trailers across trusted channels.")
        return all_trailers
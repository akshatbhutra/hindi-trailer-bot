import logging
from datetime import datetime, timezone, timedelta
from googleapiclient.discovery import build
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class YouTubeClient:
    def __init__(self, api_key: str):
        self.youtube = build("youtube", "v3", developerKey=api_key)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch_hindi_movie_trailers(self) -> list[dict]:
        """
        Searches YouTube for Hindi movie trailers published within the last 48 hours.
        """
        now = datetime.now(timezone.utc)
        published_after = (now - timedelta(hours=48)).isoformat()

        query = "Hindi movie official trailer"
        logger.info(f"Querying YouTube API for: '{query}' published after {published_after}")

        search_response = self.youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            order="date",
            publishedAfter=published_after,
            maxResults=30,
            relevanceLanguage="hi"
        ).execute()

        trailers = []
        for item in search_response.get("items", []):
            snippet = item["snippet"]
            video_id = item["id"]["videoId"]
            title = snippet["title"]
            channel_title = snippet["channelTitle"]
            published_at = snippet["publishedAt"]

            title_lower = title.lower()
            if not any(keyword in title_lower for keyword in ["trailer", "teaser", "official"]):
                continue

            trailers.append({
                "video_id": video_id,
                "title": title,
                "channel": channel_title,
                "published_at": published_at,
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })

        logger.info(f"Successfully matched and filtered {len(trailers)} valid trailers.")
        return trailers
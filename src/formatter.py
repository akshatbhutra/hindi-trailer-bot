from datetime import datetime

def format_trailer_digest(trailers: list[dict]) -> str:
    """
    Formats the list of trailers into a clean, markdown-supported WhatsApp text message.
    """
    current_date = datetime.now().strftime("%d %b %Y")
    
    if not trailers:
        return f"🎬 *Bollywood / Hindi Movie Trailer Digest* 🎬\n📅 *Date:* {current_date}\n\nNo new official trailers or teasers were found uploaded in the last 48 hours."

    digest = f"🎬 *Bollywood / Hindi Movie Trailer Digest* 🎬\n📅 *Date:* {current_date}\nFound *{len(trailers)}* new official trailer(s):\n\n"
    
    for idx, trailer in enumerate(trailers, 1):
        digest += f"*{idx}. {trailer['title']}*\n"
        digest += f"📺 *Channel:* {trailer['channel']}\n"
        digest += f"🔗 {trailer['url']}\n\n"
        
    digest += "_Powered by Python & Evolution API_"
    return digest
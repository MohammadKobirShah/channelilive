import subprocess
import json

# ✅ Replace with YouTube Channel URLs
YOUTUBE_CHANNELS = [
    "https://www.youtube.com/@ChanneliNews",       # Example: NASA Live
    "https://www.youtube.com/@JamunaTVbd"        # Example: ESPN Live
]

# 🔥 Generate M3U Header
m3u_content = "#EXTM3U\n"

def get_youtube_live_info(channel_url):
    """Fetch YouTube Live Video Details using yt-dlp"""
    command = ["yt-dlp", "--dump-json", "-f", "best", channel_url]
    print(f"🔍 Running: {' '.join(command)}")  

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        video_info = json.loads(result.stdout)
        return {
            "channel_name": video_info.get("uploader", "Unknown Channel"),
            "channel_logo": video_info.get("thumbnail", ""),
            "video_id": video_info.get("id", ""),
            "formats": video_info.get("formats", [])  # Get all available formats
        }
    except Exception as e:
        print(f"❌ Error fetching info: {e}")
        return None

# 🔄 Process Each YouTube Channel
for channel_url in YOUTUBE_CHANNELS:
    live_info = get_youtube_live_info(channel_url)

    if live_info and live_info["video_id"]:
        channel_name = live_info["channel_name"]
        channel_logo = live_info["channel_logo"]
        video_id = live_info["video_id"]
        formats = live_info["formats"]

        # 🔀 Extract M3U8 URLs for Different Qualities
        quality_map = {}
        for fmt in formats:
            if fmt.get("ext") == "m3u8":
                quality_map[fmt["height"]] = fmt["url"]  # Store by resolution

        # 🎥 Add Streams to M3U
        m3u_content += f"\n#EXTINF:-1 tvg-logo=\"{channel_logo}\",{channel_name}\n"
        for q in sorted(quality_map.keys()):  # Sort by resolution (low to high)
            m3u_content += f"{quality_map[q]}\n"

# 📁 Save M3U File
with open("youtube_live.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_content)

print("✅ M3U File Updated Successfully!")

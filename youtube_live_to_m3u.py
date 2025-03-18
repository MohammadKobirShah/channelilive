import subprocess
import json

# Replace with your YouTube channel URL
YOUTUBE_CHANNEL_URL = "https://www.youtube.com/@ChanneliNews"  # Example: NASA Live

# Video quality formats
QUALITY_MAP = {
    "144p": "160",
    "240p": "133",
    "360p": "134",
    "480p": "135",
    "720p": "136",
    "1080p": "137",
}

# Function to fetch channel name, logo, and live video ID
def get_youtube_live_info(channel_url):
    command = ["yt-dlp", "--dump-json", "-f", "best", channel_url]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        video_info = json.loads(result.stdout)
        return {
            "channel_name": video_info.get("uploader", "Unknown Channel"),
            "channel_logo": video_info.get("thumbnail", ""),
            "video_id": video_info.get("id", ""),
        }
    except Exception as e:
        print(f"Error fetching channel info: {e}")
        return None

# Function to fetch live stream URLs for different qualities
def get_live_stream_urls(video_id):
    urls = {}
    for quality, format_code in QUALITY_MAP.items():
        command = ["yt-dlp", "--dump-json", "-f", format_code, f"https://www.youtube.com/watch?v={video_id}"]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            video_info = json.loads(result.stdout)
            urls[quality] = video_info["url"]
        except Exception as e:
            print(f"Error fetching {quality} stream: {e}")
            urls[quality] = None
    return urls

# Generate an M3U file
def generate_m3u(live_urls, channel_name, channel_logo, output_file="youtube_live.m3u"):
    m3u_content = "#EXTM3U\n"
    for quality, url in live_urls.items():
        if url:
            m3u_content += f'#EXTINF:-1 tvg-name="{channel_name}" tvg-logo="{channel_logo}", {channel_name} {quality}\n{url}\n'

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(m3u_content)

    print(f"M3U file generated: {output_file}")

# Main Execution
if __name__ == "__main__":
    live_info = get_youtube_live_info(YOUTUBE_CHANNEL_URL)
    if live_info:
        live_stream_urls = get_live_stream_urls(live_info["video_id"])
        generate_m3u(live_stream_urls, live_info["channel_name"], live_info["channel_logo"])

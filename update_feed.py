import json
import subprocess
import os

# Your Church YouTube Stream URL
CHANNEL_URL = "https://www.youtube.com/@elizabethleemethodist/streams"
FEED_FILE = "content.json"

def get_youtube_videos():
   # We use the /live URL and a browser User-Agent to ensure we see the videos
    cmd = [
        "yt-dlp",
        "--get-title", "--get-id", "--get-thumbnail", "--get-description",
        "--playlist-items", "1-5",
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "--print", '{"title": "%(title)s", "description": "%(description).100s...", "hdPosterUrl": "%(thumbnail)s", "url": "https://www.youtube.com/watch?v=%(id)s", "id": "%(id)s"}',
        "https://www.youtube.com/@elizabethleemethodist/live"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        videos = [json.loads(line) for line in result.stdout.strip().split('\n') if line]
        return videos
    except Exception as e:
        print(f"Error fetching videos: {e}")
        return []

def update_roku_json():
    videos = get_youtube_videos()
    
    # Adding Roku-specific fields
    for v in videos:
        v["streamFormat"] = "hls"
        v["isLive"] = False # Defaulting to false as we discussed

    new_feed = {
        "categories": [
            {
                "title": "Recent Church Services",
                "items": videos
            }
        ]
    }
    
    with open(FEED_FILE, "w") as f:
        json.dump(new_feed, f, indent=4)
    print(f"Successfully updated {FEED_FILE}")

if __name__ == "__main__":
    update_roku_json()
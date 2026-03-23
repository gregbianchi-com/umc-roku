import json
import subprocess
import os

# Your Church YouTube Stream URL
CHANNEL_URL = "https://www.youtube.com/@elizabethleemethodist/streams"
FEED_FILE = "content.json"

def get_youtube_videos():
    # Using the direct Channel ID is the most stable way for automation
    # Elizabeth Lee Methodist Church ID: UC8D_H8v7M-UfG_N5C596p9A
    CHANNEL_ID_URL = "https://www.youtube.com/channel/UC8D_H8v7M-UfG_N5C596p9A/videos"
    
    cmd = [
        "yt-dlp",
        "--get-title", "--get-id", "--get-thumbnail", "--get-description",
        "--playlist-items", "1-5",
        "--flat-playlist",
        "--ignore-no-formats-error",
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "--print", '{"title": "%(title)s", "description": "%(description).100s...", "hdPosterUrl": "%(thumbnail)s", "url": "https://www.youtube.com/watch?v=%(id)s", "id": "%(id)s"}',
        CHANNEL_ID_URL
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        if not output:
            print("No output from yt-dlp. Check the channel URL.")
            return []
            
        videos = [json.loads(line) for line in output.split('\n') if line.strip()]
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
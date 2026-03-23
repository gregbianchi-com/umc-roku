import json
import scrapetube

CHANNEL_ID = "UC8D_H8v7M-UfG_N5C596p9A"
FEED_FILE = "content.json"

def get_videos():
    # This pulls the latest 5 videos from the 'Live' tab directly
    videos = scrapetube.get_channel(CHANNEL_ID, content_type="streams", limit=5)
    items = []
    
    for video in videos:
        items.append({
            "id": video['videoId'],
            "title": video['title']['runs'][0]['text'],
            "description": "Church Service",
            "hdPosterUrl": f"https://i.ytimg.com/vi/{video['videoId']}/maxresdefault.jpg",
            "url": f"https://www.youtube.com/watch?v={video['videoId']}",
            "streamFormat": "hls",
            "isLive": False
        })
    return items

def update_json():
    video_list = get_videos()
    new_feed = {
        "categories": [
            {
                "title": "Recent Church Services",
                "items": video_list
            }
        ]
    }
    
    with open(FEED_FILE, "w") as f:
        json.dump(new_feed, f, indent=4)
    print(f"Successfully updated with {len(video_list)} videos.")

if __name__ == "__main__":
    update_json()
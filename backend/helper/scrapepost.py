import httpx
import os
from urllib.parse import quote
import json
from dotenv import load_dotenv

load_dotenv()

def scrape_post(post_id):
    variables = {
        "shortcode": post_id,
        "child_comment_count": 10,
        "fetch_comment_count": 10,
    }
    url = "https://www.instagram.com/graphql/query/?query_hash=b3055c01b4b222b8a47dc12b090e4e64&variables="
    
    headers = {
        "x-ig-app-id": os.environ.get("INSTAGRAM_APP_ID"),
        # Additional headers might be needed, such as:
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json",
        "Cookie": "your_cookies_here"  # You might need to include cookies from a logged-in session
    }
    
    response = httpx.get(
        url=url + quote(json.dumps(variables)),
        headers=headers,
    )
    
    if response.status_code == 401:
        raise Exception("Unauthorized request. Check your headers and cookies.")
    
    data = response.json()
    
    if "data" not in data or "shortcode_media" not in data["data"]:
        raise Exception("Failed to retrieve post data.")
    
    post_data = data["data"]["shortcode_media"]
    
    post_info = {
        "id": post_data["id"],
        "shortcode": post_data["shortcode"],
        "caption": post_data["edge_media_to_caption"]["edges"][0]["node"]["text"] if post_data["edge_media_to_caption"]["edges"] else "",
        "images": [],
        "comments": []
    }
    
    if "edge_sidecar_to_children" in post_data:
        for edge in post_data["edge_sidecar_to_children"]["edges"]:
            post_info["images"].append(edge["node"]["display_url"])
    else:
        post_info["images"].append(post_data["display_url"])
    
    # Extract comments
    comments = post_data["edge_media_to_parent_comment"]["edges"]
    for comment in comments:
        comment_node = comment["node"]
        post_info["comments"].append({
            "id": comment_node["id"],
            "text": comment_node["text"],
            "username": comment_node["owner"]["username"]
        })
    
    return post_info


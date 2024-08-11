import json
import httpx
from urllib.parse import quote

def scrape_user_followers(user_id: str, session: httpx.Client, page_size=50, max_pages: int = None):
    followers_base_url = "https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables="
    
    followers_variables = {
        "id": user_id,
        "first": page_size,
        "after": None,
    }
    
    followers = []
    page_count = 0
    
    while True:
        if max_pages and page_count >= max_pages:
            break
        
        resp = session.get(followers_base_url + quote(json.dumps(followers_variables)))
        data = resp.json()
        
        if not data["data"]["user"]["edge_followed_by"]["edges"]:
            break
        
        followers.extend(data["data"]["user"]["edge_followed_by"]["edges"])
        
        page_info = data["data"]["user"]["edge_followed_by"]["page_info"]
        if not page_info["has_next_page"]:
            break
        
        followers_variables["after"] = page_info["end_cursor"]
        page_count += 1
    
    return followers

session = httpx.Client()
followers_data = scrape_user_followers("7144226283", session, page_size=50, max_pages=5)

print("Total followers fetched:", len(followers_data))
print("Followers Data:", json.dumps(followers_data, indent=2))

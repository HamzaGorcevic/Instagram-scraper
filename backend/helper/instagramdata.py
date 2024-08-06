import json
import httpx
from urllib.parse import quote
from helper.parsepost import parse_post
from models.media import Media
def scrape_user_posts(user_id: str, session: httpx.Client, page_size=1, max_pages: int = None):
    base_url = "https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables="
    variables = {
        "id": user_id,
        "first": page_size,
        "after": None,
    }
    _page_number = 1
    while True:
        resp = session.get(base_url + quote(json.dumps(variables)))
        data = resp.json()
        posts = data["data"]["user"]["edge_owner_to_timeline_media"]
        for post in posts["edges"]:
            yield parse_post(post["node"])  # note: we're using parse_post function from previous chapter
        page_info = posts["page_info"]
        if _page_number == 1:
            print(f"scraping total {posts['count']} posts of {user_id}")
        else:
            print(f"scraping page {_page_number}")
        if not page_info["has_next_page"]:
            break
        if variables["after"] == page_info["end_cursor"]:
            break
        variables["after"] = page_info["end_cursor"]
        _page_number += 1     
        if max_pages and _page_number > max_pages:
            break

def scraper(profile_id,pages):
     with httpx.Client(timeout=httpx.Timeout(20.0)) as session:
        posts = list(scrape_user_posts(profile_id, session, max_pages=pages))
        print("before parsnig",posts)
        parsedPosts = [Media(**post) for post in posts]
        print("after parsnig",parsedPosts)
        return parsedPosts
        

import json
import httpx
from urllib.parse import quote
from helper.parsepost import parse_post
from models.media import Media
def scrape_user_posts(profile_name: str, session: httpx.Client, page_size=1, max_pages: int = None):
    
    result = session.get(
        f"https://i.instagram.com/api/v1/users/web_profile_info/?username={profile_name}",
    )
    profile_data = json.loads(result.content)
    user_id = profile_data["data"]["user"]["id"]
    

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
     with httpx.Client(  headers={
        # this is internal ID of an instegram backend app. It doesn't change often.
        "x-ig-app-id": "936619743392459",
        # use browser-like features
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
    },timeout=httpx.Timeout(20.0)) as session:
        posts = list(scrape_user_posts(profile_id, session, max_pages=pages))
        parsedPosts = [Media(**post) for post in posts]
        return parsedPosts
        



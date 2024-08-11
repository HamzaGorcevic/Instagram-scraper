import jmespath
from typing import Dict

def parse_post(data: Dict) -> Dict:
    result = jmespath.search("""{
        post_id: id,
        thumbnail: display_url,
        media: (edge_sidecar_to_children.edges[].node.display_url) || [display_url],
        video_url: video_url,
        description: edge_media_to_caption.edges[0].node.text || ""
    }""", data)
    return result
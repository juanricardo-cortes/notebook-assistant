from abstractions.base_scraper import SocialScraper
from facebook import GraphAPI # type: ignore

class FacebookService(SocialScraper):
    def __init__(self, access_token, output_folder='output/facebook'):
        super().__init__(output_folder)
        self.graph = GraphAPI(access_token)

    def scrape_profile(self, group_url: str) -> list:
        """Scrapes new posts from a Facebook group URL."""
        # Extract group ID from the URL
        group_id = group_url.split('/')[-1] if '/' in group_url else group_url
        posts = self.graph.get_connections(group_id, 'feed')
        return posts.get('data', [])

    def get_user_profile(self):
        return self.graph.get_object('me')

    def get_user_posts(self):
        return self.graph.get_connections('me', 'posts')

    def post_status(self, message):
        return self.graph.put_object(parent_object='me', connection_name='feed', message=message)

    def get_page_posts(self, page_id):
        return self.graph.get_connections(page_id, 'posts')

    def post_to_page(self, page_id, message):
        return self.graph.put_object(parent_object=page_id, connection_name='feed', message=message)

    def scrape_facebook_profile(self, profile_url: str) -> list:
        """Scrapes new posts from a Facebook profile URL."""
        # Extract profile ID from the URL (simplified example)
        profile_id = profile_url.split('/')[-1] if '/' in profile_url else profile_url
        posts = self.graph.get_connections(profile_id, 'posts')
        return posts.get('data', [])
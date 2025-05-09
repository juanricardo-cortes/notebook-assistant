from googleapiclient.discovery import build # type: ignore
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound # type: ignore
import os
import datetime
import re
import urllib.parse
from abstractions.base_scraper import SocialScraper

class YouTubeService(SocialScraper):
    def __init__(self, api_key, output_folder='output/youtube'):
        super().__init__(output_folder)
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)


    def scrape_profile(self, profile_url: str) -> list:
        try:
            transcripts = []
            channel_id = self.extract_channel_id_from_url(profile_url)
            channel_name = profile_url.split('@')[1].split('/')[0]
            print(f"Checking new videos for {channel_name}...")
            new_videos = self.get_recent_videos(channel_id)
            if new_videos:
                for video in new_videos:
                    transcript = self.fetch_transcript(video['video_id'])
                    if transcript:
                        transcripts.append(self.save_transcript(
                            channel_name, 
                            video['video_id'], 
                            video['title'], 
                            video['description'], 
                            video['views'], 
                            video['comments'],
                            video['likes'],
                            transcript))
            else:
                print(f"No new videos for {channel_name} yesterday.")
            return transcripts
        except Exception as e:
            print(f"Failed to process {profile_url}: {e}")
        

    def get_uploads_playlist_id(self, channel_id):
        response = self.youtube.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()
        uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        return uploads_playlist_id

    def get_recent_videos(self, channel_id):
        uploads_playlist_id = self.get_uploads_playlist_id(channel_id)
        today = datetime.datetime.utcnow().date()
        yesterday = today - datetime.timedelta(days=1)

        response = self.youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads_playlist_id,
            maxResults=50
        ).execute()

        new_videos = []
        for item in response['items']:
            published_at = item['snippet']['publishedAt']
            published_date = datetime.datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").date()
            if published_date == yesterday:
                video_id = item['snippet']['resourceId']['videoId']
                title = item['snippet']['title']
                description = item['snippet'].get('description', '')

                # Fetch additional details like views, comments, and likes
                video_details = self.youtube.videos().list(
                    part='statistics',
                    id=video_id
                ).execute()

                statistics = video_details['items'][0]['statistics']
                views = statistics.get('viewCount', 0)
                comments = statistics.get('commentCount', 0)
                likes = statistics.get('likeCount', 0)

                new_videos.append({
                    'video_id': video_id,
                    'title': title,
                    'description': description,
                    'views': views,
                    'comments': comments,
                    'likes': likes
                })
        return new_videos

    def fetch_transcript(self, video_id):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            print(f"Transcript not available for video {video_id}: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def save_transcript(self, channel_name, video_id, video_title, description, views, comments, likes, transcript):
        transcript_data = {
            "youtube_link": f"https://www.youtube.com/watch?v={video_id}",
            "channel_name": channel_name,
            "title": video_title,
            "description": description,
            "views": views,
            "comments": comments,
            "likes": likes,
            "transcript": [
                {"start": entry['start'], "text": entry['text']} for entry in transcript
            ]
        }
        return transcript_data

    def extract_channel_id_from_url(self, url):
        # Extract handle from URL
        parsed_url = urllib.parse.urlparse(url)
        path_parts = parsed_url.path.split('/')
        if '@' in path_parts[1]:
            handle = path_parts[1][1:]  # Remove '@'
        else:
            raise ValueError(f"Invalid YouTube handle URL: {url}")

        # Search for channel by handle using YouTube API
        response = self.youtube.search().list(
            part='snippet',
            q=handle,
            type='channel',
            maxResults=1
        ).execute()

        if response['items']:
            channel_id = response['items'][0]['snippet']['channelId']
            return channel_id
        else:
            raise ValueError(f"No channel found for handle: {handle}")

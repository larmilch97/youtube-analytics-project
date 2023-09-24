import os
from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=self.video_id).execute()
        self.title: str = video_response['items'][0]['snippet']['title']
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']
        self.comment_count: int = video_response['items'][0]['statistics']['commentCount']

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id: str = playlist_id

import os
from datetime import timedelta
import isodate
from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id: str = playlist_id
        self.title: str = self.title_video(playlist_id)
        self.url: str = f"https://www.youtube.com/playlist?list={playlist_id}"

    def title_video(self, playlist_id: str) -> str:
        title = self.youtube.playlists().list(id=playlist_id, part='snippet').execute()
        playlist_title: str = title['items'][0]['snippet']['title']
        return playlist_title

    @property
    def total_duration(self) -> timedelta:
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        total_duration = timedelta()
        for video in video_response['items']:
            iso_8601_duration: str = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_statistics = self.youtube.videos().list(id=','.join(video_ids), part='statistics').execute()

        video_likes = [(video['id'], int(video['statistics']['likeCount'])) for video in video_statistics['items']]
        best_video_id, _ = max(video_likes, key=lambda x: x[1])
        return f"https://youtu.be/{best_video_id}"

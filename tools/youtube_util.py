import subprocess

import google.auth
from googleapiclient.discovery import build

def get_title(video_url: str):
    title_cmd = f"yt-dlp --get-title {video_url}"
    process = subprocess.run(title_cmd.split(), capture_output=True, text=True)
    return process.stdout.strip()

def video_as_audio(video_url: str, audio_type: str, starting_time: str = None, end_time: str = None):
    outfile = f"tmp.{audio_type}"
    download_cmd = f"yt-dlp -x --audio-format {audio_type} -o {outfile}".split()
    post_args = ""
    if starting_time:
        post_args += f" -ss {starting_time}"
    if end_time:
        post_args += f" -to {end_time}"
    if post_args:
        download_cmd += ["--postprocessor-args", post_args]
    download_cmd += [video_url]
    # print(download_cmd)
    subprocess.run(download_cmd, capture_output=True, text=True)
    return outfile

def get_playlist(playlist_id: str):
    # Set up the API client
    credentials, project = google.auth.default(
        scopes=['https://www.googleapis.com/auth/youtube.readonly'])
    youtube = build('youtube', 'v3', credentials=credentials)

    # Set the maximum number of results to retrieve
    max_results = 250
    # Get the playlist items
    playlist_items = []
    next_page_token = None
    while True:
        playlist_request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=max_results,
            pageToken=next_page_token
        )
        playlist_response = playlist_request.execute()
        playlist_items += playlist_response['items']
        next_page_token = playlist_response.get('nextPageToken')
        if next_page_token is None:
            break

    # Extract the titles from the playlist items
    return [(item['snippet']['title'], item['snippet']['resourceId']['videoId']) for item in playlist_items]

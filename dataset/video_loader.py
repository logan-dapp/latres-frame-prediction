from pytube import YouTube
from urllib.request import urlopen
import json
import os
import random
import shutil
import time

HATMAN_VIDEOS = eval(open('hatman_videos.txt').read())

def random_name():
    return ''.join([random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_') for _ in range(50)])

class HatmanDownloader:
    def __init__(self, data_folder='training_videos'):
        self.videos = HATMAN_VIDEOS
        self.data_folder = data_folder
        if not os.path.exists(self.data_folder):
            os.mkdir(self.data_folder)

    def __next__(self):
        try:
            video = self.videos.pop(0)
            print(f'Fetching {video}...')
            yt = YouTube(video)
            files = set(os.listdir('.'))
            yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
            while set(os.listdir('.')) == files:
                time.sleep(1.0)
            new_files = set(os.listdir('.')).difference(files)
            new_file = [x for x in new_files if '.mp4' in x][0]
            new_name = random_name() + '.mp4'
            os.rename(new_file, new_name)
            shutil.move(new_name, self.data_folder)
            return f'{self.data_folder}/{new_name}'
        except IndexError:
            raise StopIteration

def get_all_videos_in_channel(channel_id):
    """Code from Stian on StackOverflow"""

    api_key = open(PUT+API+KEY+HERE).read()

    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    first_url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(api_key, channel_id)

    video_links = []
    url = first_url
    while True:
        inp = urlopen(url)
        resp = json.load(inp)

        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links.append(base_video_url + i['id']['videoId'])

        try:
            next_page_token = resp['nextPageToken']
            url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break
    return video_links

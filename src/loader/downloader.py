# %%
from youtube_dl import YoutubeDL
import sys
from pathlib import *
import json


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from settings import *


class downloader:
    def __init__(self, settings):
        self.settings = settings
        self.audioDownloader = YoutubeDL({
            'format': settings["youtubeDLFormat"],
            'outtmpl': str(SRC_DIR)+'/'+str(settings['downloadPath'])+'/%(title)s.%(ext)s',
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }]
            })


    '''
        download the song from youtube with the given URL.
        returns the dict of soung deatils

        songName : name of song
        songUrl  : URL of the song 
    '''
    def download(self, songName, songUrl):
        try:
            print("Downloading {}...".format(songName))
            audioDownloaded = self.audioDownloader.extract_info(songUrl)

            return audioDownloaded
        except Exception as e:
            print(e)
            print("Failed..")
            return None

# %%
import json
import os
import sys
from pathlib import *

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scrapper.urlExtractor import *
from loader.downloader import *


class songsLayout:
    def __init__(self, settings):
        self.settings = settings
        
        with open(self.settings['layoutPath']) as l:
            sLayout = json.load(l)

        if self.settings["allSongs"] not in sLayout:
            raise Exception("No default all Song list in songs layout \n>>>Add allSong in the layout json file<<<")


    '''
        creates a new playlist in the layout

        playlistName : name of the new playlist
        flag : N - creates new playlist if playlist dont exists else raise exception
               C - creates new playlist if playlist dont exists
               O - creates new playlist and overwrite if already exists
    '''
    def createPlaylist(self, playlistName, flag='N'):
        with open(self.settings['layoutPath']) as l:
            sLayout = json.load(l)

        if flag != 'N' and flag != 'O' and flag != 'C':
            raise Exception(f'flag error : {flag}')

        if playlistName == self.settings["allSongs"] and ( flag == 'N' or flag == 'O'):
            raise Exception(f'can\'t make changes in {self.settings["allSongs"]}')

        if playlistName in sLayout and flag == 'N':
            raise Exception(f'playlist : {playlistName} already exists')

        if flag == 'N' or flag == 'O':
            sLayout[playlistName] = {}
            sLayout[playlistName]['songs'] = {}

        with open(self.settings['layoutPath'], 'w') as l:
            json.dump(sLayout, l, indent=4)

    '''
        delete the specific playlist from the layout

        playlistName : name of the playlist to be deleted
        flag : D - delete playlist if playlist exists
               E - delete playlist if playlist exists else raise exception and raise exception if try to delete default playlist
    '''
    def deletePlaylist(self, playlistName, flag='D'):
        with open(self.settings['layoutPath']) as l:
            sLayout = json.load(l)

        if flag != 'D' and flag != 'E':
            raise Exception(f'flag error : {flag}')
        
        if playlistName == self.settings["allSongs"] and flag == 'E':
            raise Exception(f'can\'t make changes in {self.settings["allSongs"]}')
        elif playlistName == self.settings["allSongs"]:
            print(f'can\'t make changes in {self.settings["allSongs"]}')
            return

        if playlistName not in sLayout and flag == 'E':
            raise Exception(f'No playlist : {playlistName}')
        
        if playlistName in sLayout:
            del sLayout[playlistName]

        with open(self.settings['layoutPath'], 'w') as l:
            json.dump(sLayout, l, indent=4)

    '''
        add song to the specific playlist and dowload the song

        playlistName : name of the playlist
        songName : name of the song to be downloaded and added
        flag : C - create new playlist if it doesn't exists
               E - raise exception if playlist dont exists
    '''
    def addSong(self, playlistName, songName, flag='E'):
        with open(self.settings['layoutPath']) as l:
            sLayout = json.load(l)

        if flag != 'C' and flag != 'E':
            raise Exception(f'flag error : {flag}')

        if playlistName not in sLayout and flag == 'E':
            raise Exception(f'No playlist : {playlistName}')
        if playlistName not in sLayout and flag == 'C':
            self.createPlaylist(playlistName, 'N')
            with open(self.settings['layoutPath']) as l:
                sLayout = json.load(l)

        if songName in sLayout[playlistName]['songs']:
            print('song already in the playlist')
        else:
            songFileName, songUrl = getUrl(songName)
            if songName in sLayout[self.settings["allSongs"]]['songs']:
                sLayout[playlistName]['songs'][songName] = sLayout[self.settings["allSongs"]]['songs'][songName]
            else:
                oldSong = ""
                for songName in sLayout[self.settings["allSongs"]]['songs']:
                    if sLayout[self.settings["allSongs"]]['songs'][songName]['file'] == songFileName:
                        oldSong = songName
                if oldSong != "":
                    print(f'{songName} already exists as different name : {oldSong}')
                    print(f'song added as {oldSong}')
                    sLayout[playlistName]['songs'][oldSong] = sLayout[self.settings["allSongs"]]['songs'][oldSong] 
                else:
                    songDownloader = downloader(self.settings)
                    songData = songDownloader.download(songName, songUrl)

                    sLayout[playlistName]['songs'][songName] = {'file': songFileName, 'url': songUrl}
                    sLayout[self.settings["allSongs"]]['songs'][songName] = {'file': songFileName, 'url': songUrl}

        with open(self.settings['layoutPath'], 'w') as l:
            json.dump(sLayout, l, indent=4)

    '''
        sync all playlists with allSongs
    '''
    def sync(self):
        with open(self.settings['layoutPath']) as l:
            sLayout = json.load(l)


        for playlistName in sLayout:
            if playlistName == self.settings["allSongs"]: 
                continue

            for songName in list(sLayout[playlistName]['songs']):
                if songName not in sLayout[self.settings["allSongs"]]['songs']:
                    del sLayout[playlistName]['songs'][songName]


        with open(self.settings['layoutPath'], 'w') as l:
            json.dump(sLayout, l, indent=4)


    '''
        remove song from the playlist
        playlistName : name of the playlist
        songName : name of the song to be removed
    '''
    def removeSong(self, playlistName, songName):
        with open(self.settings['layoutPath']) as l:
            sLayout = json.load(l)

        if playlistName not in sLayout :
            print(f'No playlist : {playlistName}')
            return

        if songName in sLayout[playlistName]['songs']:
            del sLayout[playlistName]['songs'][songName]
        else:
            print(f'no {songName} in {playlistName}')

        with open(self.settings['layoutPath'], 'w') as l:
            json.dump(sLayout, l, indent=4)


    '''
        remove song from allSongs/allPlaylist and delete it from the directory
        songName : name of the song to be deleted
    '''
    def deleteSong(self, songName):
        with open(self.settings['layoutPath']) as l:
           sLayout = json.load(l)

        if songName in sLayout[self.settings["allSongs"] ]['songs']:
            songFileName = sLayout[self.settings["allSongs"]]['songs'][songName]
            del sLayout[self.settings["allSongs"]]['songs'][songName]

            if os.path.exists(os.path.join(self.settings['downloadPath'], songFileName)):
                os.remove(os.path.join(self.settings['downloadPath'], songFileName))
            else:
                print(f'The song does not exist : {os.path.join(self.settings["downloadPath"], songFileName)}')
        else:
            print(f'no {songName} in {self.settings["allSongs"]}')

        with open(self.settings['layoutPath'], 'w') as l:
            json.dump(sLayout, l, indent=4)
       
        self.sync()


    '''
        returns list of all playlist
    '''
    def getPlaylist(self):
        with open(self.settings['layoutPath']) as l:
            sLayout = json.load(l)

        allPlaylists = []

        for playlistName in sLayout:
            if playlistName == self.settings["allSongs"]: 
                allPlaylists.append(playlistName + ' - default')
            else:
                allPlaylists.append(playlistName)

        return allPlaylists

    '''
        returns list of all songs in a playlist
        playlistName : name of the playlist
    '''
    def getSongs(self, playlistName):
        with open(self.settings['layoutPath']) as l:
            sLayout = json.load(l)

        if playlistName not in sLayout :
            print(f'No playlist : {playlistName}')
            return

        allSongs = []

        for songName in sLayout[playlistName]['songs']:
            allSongs.append(songName)

        return allSongs


    '''
        returns list of all songs
    '''
    def getAllSongs(self):
        with open(self.settings['layoutPath']) as l:
            sLayout = json.load(l)

        allSongs = []

        for songName in sLayout[self.settings["allSongs"]]['songs']:
            allSongs.append(songName)

        return allSongs
    
    def clearLayout(self):
        with open(self.settings['layoutPath']) as l:
           sLayout = json.load(l)

        sLayout = {
            self.settings["allSongs"] : {
                "songs": {}
            }
        }

        with open(self.settings['layoutPath'], 'w') as l:
            json.dump(sLayout, l, indent=4)


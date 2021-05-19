import pygame 

class musicPlayer():
    def __init__(self):
        pygame.mixer.init()
        self.currSong = ''


    '''
        check is song in playing
    '''
    def playCheck(self):
        return pygame.mixer.music.get_busy()

    '''
        Play the specific Song
    '''
    def play(self, songName, songPath):
        self.currSong = songName
        print(f'playing song {self.currSong}')
        pygame.mixer.music.load(songPath)
        pygame.mixer.music.play()

    '''
        stop the song playing
    '''
    def stop(self):
        if not self.playCheck :
            self.currSong ==''

        if self.currSong == '':
            print('No song playing')
        else:
            print(f'song stopped {self.currSong}')
            self.currSong = ''
            pygame.mixer.music.stop()

    '''
        pause the song
    '''
    def pause(self):   
        if not self.playCheck :
            self.currSong = ''

        if self.currSong == '':
            print('No song playing')
        else:
            print(f'song paused {self.currSong}')
            pygame.mixer.music.pause()

    '''
        unpause the song
    '''
    def unpause(self):
        if not self.playCheck :
            self.currSong = ''

        if self.currSong == '':
            print('No song playing')
        else:
            print(f'song unpaused {self.currSong}')
            pygame.mixer.music.unpause()
import pygame 

class musicPlayer():
    def __init__(self):
        pygame.mixer.init()

    '''
        Play the specific Song
    '''
    def play(self, songPath):
        print("playing song...")
        pygame.mixer.music.load(songPath)
        pygame.mixer.music.play()

    '''
        stop the song playing
    '''
    def stop(self):
        print("song stopped...")
        pygame.mixer.music.stop()

    '''
        pause the song
    '''
    def pause(self):   
        print("song paused...")
        pygame.mixer.music.pause()

    '''
        unpause the song
    '''
    def unpause(self):
        print("song unpaused...")
        pygame.mixer.music.unpause()

    '''
        check is song in playing
    '''
    def playCheck(self):
        return pygame.mixer.music.get_busy()
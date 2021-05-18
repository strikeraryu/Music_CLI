import pygame 

class musicPlayer():
    def __init__(self):
        pygame.mixer.init()

    '''
        Play the specific Song
    '''
    def play(slef, songPath):
        pygame.mixer.music.load(songPath)
        pygame.mixer.music.play()

    '''
        stop the song playing
    '''
    def stop(self):
        pygame.mixer.music.stop()

    '''
        pause the song
    '''
    def pause(self):   
        pygame.mixer.music.pause()

    '''
        unpause the song
    '''
    def unpause(self):
        pygame.mixer.music.unpause()
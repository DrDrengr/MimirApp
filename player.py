import os
import pygame

class Player():
    def __init__(self):
        rootPath = os.path.abspath(os.path.dirname(__file__))
        self.soundPath = os.path.join(rootPath, "sounds/actionButton.wav")
    
    def playMenuSound(self):
        pygame.mixer.init()
        my_sound = pygame.mixer.Sound(self.soundPath)
        my_sound.set_volume(0.07)
        my_sound.play()
        pygame.time.wait(int(my_sound.get_length()))
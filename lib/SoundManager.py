import pygame
import lib.Color as Color

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.background_music = None
        self.music_volume = 0.3
        self.sound_volume = 0.7
        self.load_sounds()
    
    def load_sounds(self):
        try:
            self.sounds['correct'] = pygame.mixer.Sound("sounds/acierto.mp3")
            self.sounds['wrong'] = pygame.mixer.Sound("sounds/error.mp3")
            
            for sound in self.sounds.values():
                sound.set_volume(self.sound_volume)
            
            pygame.mixer.music.load("sounds/fondo.mp3")
            pygame.mixer.music.set_volume(self.music_volume)
        except pygame.error as e:
            print(f"Error loading sounds: {e}")
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_background_music(self):
        try:
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass
    
    def stop_background_music(self):
        pygame.mixer.music.stop()
    
    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sound_volume(self, volume):
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
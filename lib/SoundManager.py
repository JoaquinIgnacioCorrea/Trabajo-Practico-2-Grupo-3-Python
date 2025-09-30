import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self._sounds = {}
        self._background_music = None
        self._music_volume = 0.3
        self._sound_volume = 0.5
        self._load_sounds()
    
    def _load_sounds(self):
        self._sounds['correct'] = pygame.mixer.Sound("sounds/acierto.mp3")
        self._sounds['wrong'] = pygame.mixer.Sound("sounds/error.mp3")
        
        for sound in self._sounds.values():
            sound.set_volume(self._sound_volume)
        
        pygame.mixer.music.load("sounds/fondo.mp3")
        pygame.mixer.music.set_volume(self._music_volume)
    
    def play_sound(self, sound_name):
        if sound_name in self._sounds:
            self._sounds[sound_name].play()
    
    def play_background_music(self):
        pygame.mixer.music.play(-1)
    
    def stop_background_music(self):
        pygame.mixer.music.stop()
    
    def set_music_volume(self, volume):
        self._music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self._music_volume)
    
    def set_sound_volume(self, volume):
        self._sound_volume = max(0.0, min(1.0, volume))
        for sound in self._sounds.values():
            sound.set_volume(self._sound_volume)

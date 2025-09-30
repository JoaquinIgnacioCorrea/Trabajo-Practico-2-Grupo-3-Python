import pygame
import lib.Var as Var
import lib.Color as Color

class Player:
    def __init__(self):
        self._lane = Var.INITIAL_LANE
        self._x = Var.LANE_LEFT_X if self._lane == "L" else Var.LANE_RIGHT_X
        self._y = Var.PLAYER_Y
        self._width = 80
        self._height = 196
        self._moving = False
        self._animation_frame = 0
        self._animation_speed = 0.15
        self._rect = pygame.Rect(self._x - self._width//2, self._y - self._height//2, self._width, self._height)
        
        self._sprites_idle = []
        self._sprites_walk = []
        self._load_sprites()
    
    def get_lane(self):
        return self._lane
    
    def set_lane(self, lane):
        self._lane = lane
    
    def get_x(self):
        return self._x
    
    def set_x(self, x):
        self._x = x
    
    def get_rect(self):
        return self._rect
        
    def _load_sprites(self):
        idle_sprite = pygame.image.load("Sprites/Personajes/idle.png").convert_alpha()
        self._sprites_idle.append(pygame.transform.scale(idle_sprite, (self._width, self._height)))
        
        for i in range(1, 5):
            walk_sprite = pygame.image.load(f"Sprites/Personajes/walk_{i}.png").convert_alpha()
            self._sprites_walk.append(pygame.transform.scale(walk_sprite, (self._width, self._height)))
    
    def move_to_lane(self, target_lane):
        if target_lane != self._lane and target_lane in ["L", "R"]:
            self._lane = target_lane
            self._x = Var.LANE_LEFT_X if target_lane == "L" else Var.LANE_RIGHT_X
            self._moving = True
            self._update_rect()
    
    def _update_rect(self):
        self._rect = pygame.Rect(self._x - self._width//2, self._y - self._height//2, self._width, self._height)
    
    def update(self, dt):
        self._animation_frame += self._animation_speed * dt * 60
        if self._animation_frame >= len(self._sprites_walk):
            self._animation_frame = 0
        
        if self._moving:
            if self._animation_frame >= 1:
                self._moving = False
    
    def draw(self, screen):
        sprite_list = self._sprites_walk if len(self._sprites_walk) > 0 else self._sprites_idle
        frame_index = int(self._animation_frame) % len(sprite_list)
        current_sprite = sprite_list[frame_index]
        screen.blit(current_sprite, (self._x - self._width//2, self._y - self._height//2))

import pygame
import lib.Var as Var
import lib.Color as Color

class Player:
    def __init__(self):
        self.lane = Var.INITIAL_LANE
        self.x = Var.LANE_LEFT_X if self.lane == "L" else Var.LANE_RIGHT_X
        self.y = Var.PLAYER_Y
        self.width = 80
        self.height = 80
        self.moving = False
        self.animation_frame = 0
        self.animation_speed = 0.15
        self.rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
        
        self.sprites_idle = []
        self.sprites_walk = []
        self.load_sprites()
        
    def load_sprites(self):
        try:
            idle_sprite = pygame.image.load("sprites/personaje/idle.png").convert_alpha()
            self.sprites_idle.append(pygame.transform.scale(idle_sprite, (self.width, self.height)))
            
            for i in range(1, 5):
                try:
                    walk_sprite = pygame.image.load(f"sprites/personaje/walk_{i}.png").convert_alpha()
                    self.sprites_walk.append(pygame.transform.scale(walk_sprite, (self.width, self.height)))
                except pygame.error:
                    continue
                    
            if not self.sprites_walk:
                self.sprites_walk = self.sprites_idle.copy()
                
        except pygame.error:
            pass
    
    def move_to_lane(self, target_lane):
        if target_lane != self.lane and target_lane in ["L", "R"]:
            self.lane = target_lane
            self.x = Var.LANE_LEFT_X if target_lane == "L" else Var.LANE_RIGHT_X
            self.moving = True
            self.update_rect()
    
    def update_rect(self):
        self.rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
    
    def update(self, dt):
        self.animation_frame += self.animation_speed * dt * 60
        if len(self.sprites_walk) > 0 and self.animation_frame >= len(self.sprites_walk):
            self.animation_frame = 0
        elif len(self.sprites_walk) == 0 and self.animation_frame >= 1:
            self.animation_frame = 0
        
        if self.moving:
            if self.animation_frame >= 1:
                self.moving = False
    
    def draw(self, screen):
        sprite_list = self.sprites_walk if len(self.sprites_walk) > 0 else self.sprites_idle
        
        if len(sprite_list) > 0:
            frame_index = int(self.animation_frame) % len(sprite_list)
            current_sprite = sprite_list[frame_index]
            screen.blit(current_sprite, (self.x - self.width//2, self.y - self.height//2))
        else:
            pygame.draw.rect(screen, Color.GREEN, self.rect)
            pygame.draw.circle(screen, Color.DARK, (self.x, self.y - 20), 8)
import pygame
import lib.Var as Var
import lib.Color as Color

class Background:
    def __init__(self):
        self.road_stripes = []
        self.stripe_speed = Var.INITIAL_SPEED
        self.init_stripes()
    
    def init_stripes(self):
        for i in range(0, Var.HEIGHT + 100, 50):
            self.road_stripes.append(i)
    
    def update(self, dt, speed):
        self.stripe_speed = speed
        for i in range(len(self.road_stripes)):
            self.road_stripes[i] += self.stripe_speed * dt * 60
            if self.road_stripes[i] > Var.HEIGHT + 50:
                self.road_stripes[i] = -50
    
    def draw(self, screen):
        screen.fill(Color.BG)
        
        road_rect = pygame.Rect(0, 0, Var.WIDTH, Var.HEIGHT)
        pygame.draw.rect(screen, Color.ROAD, road_rect)
        
        for y in self.road_stripes:
            pygame.draw.line(screen, Color.GRAY, (Var.WIDTH//2, y), (Var.WIDTH//2, y + 25), 5)

class InputHandler:
    def __init__(self):
        self.keys_pressed = set()
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.keys_pressed.add(event.key)
        elif event.type == pygame.KEYUP:
            self.keys_pressed.discard(event.key)
    
    def is_key_pressed(self, key):
        return key in self.keys_pressed
    
    def clear(self):
        self.keys_pressed.clear()
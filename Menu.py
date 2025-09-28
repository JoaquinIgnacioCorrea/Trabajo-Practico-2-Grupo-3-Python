import pygame
import sys
import lib.Color as Color
import lib.Var as Var
from lib.Game import Game

class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Var.WIDTH, Var.HEIGHT))
        pygame.display.set_caption("Math Runner - Menu")
        self.clock = pygame.time.Clock()
        
        self.font_big = pygame.font.SysFont("arial", Var.FONT_SIZE_BIG, bold=True)
        self.font_med = pygame.font.SysFont("arial", Var.FONT_SIZE_MED, bold=True)
        self.font_small = pygame.font.SysFont("arial", Var.FONT_SIZE_SMALL)
        
        self.running = True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.start_game()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def start_game(self):
        pygame.quit()
        game = Game()
        game.run()
        self.running = False
    
    def draw(self):
        self.screen.fill(Color.BG)
        
        center_x = Var.WIDTH // 2
        center_y = Var.HEIGHT // 2
        
        title_text = self.font_big.render("MATH RUNNER", True, Color.TEXT)
        title_rect = title_text.get_rect(center=(center_x, center_y - 100))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.font_med.render("Aprende matemáticas jugando", True, Color.GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(center_x, center_y - 50))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        start_text = self.font_med.render("Presiona ESPACIO para jugar", True, Color.GREEN)
        start_rect = start_text.get_rect(center=(center_x, center_y + 50))
        self.screen.blit(start_text, start_rect)
        
        exit_text = self.font_small.render("Presiona ESC para salir", True, Color.GRAY)
        exit_rect = exit_text.get_rect(center=(center_x, center_y + 100))
        self.screen.blit(exit_text, exit_rect)
        
        pygame.display.flip()
    
    def run(self):
        menu_active = True
        while menu_active and self.running:
            self.clock.tick(Var.FPS)
            self.handle_events()
            self.draw()
            
            if not self.running:
                menu_active = False
        
        pygame.quit()

if __name__ == "__main__":
    menu = Menu()
    menu.run()
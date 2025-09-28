import pygame
import sys
import lib.Color as Color
import lib.Var as Var

class GameConfig:
    def __init__(self):
        self.music_volume = 0.5
        self.sound_volume = 0.7
        self.difficulty = 1
        self.show_tutorial = True
    
    def save_config(self):
        pass
    
    def load_config(self):
        pass

class Tutorial:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Var.WIDTH, Var.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont("arial", Var.FONT_SIZE_BIG, bold=True)
        self.font_med = pygame.font.SysFont("arial", Var.FONT_SIZE_MED, bold=True)
        self.font_small = pygame.font.SysFont("arial", Var.FONT_SIZE_SMALL)
        self.running = True
    
    def show_tutorial(self):
        tutorial_active = True
        while tutorial_active and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    tutorial_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        tutorial_active = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        tutorial_active = False
            
            self.draw_tutorial()
            self.clock.tick(Var.FPS)
    
    def draw_tutorial(self):
        self.screen.fill(Color.BG)
        
        center_x = Var.WIDTH // 2
        y_offset = 50
        
        title = self.font_big.render("¿Cómo Jugar?", True, Color.TEXT)
        title_rect = title.get_rect(center=(center_x, y_offset))
        self.screen.blit(title, title_rect)
        
        instructions = [
            "• Usa A/← para moverte al carril izquierdo",
            "• Usa D/→ para moverte al carril derecho", 
            "• Resuelve los problemas matemáticos eligiendo el carril correcto",
            "• ¡Respuestas consecutivas correctas dan más puntos!",
            "• Tienes 3 vidas - ¡no las desperdicies!",
            "",
            "¡Diviértete aprendiendo matemáticas!"
        ]
        
        for i, instruction in enumerate(instructions):
            if instruction:
                text = self.font_small.render(instruction, True, Color.DARK)
                text_rect = text.get_rect(center=(center_x, y_offset + 100 + i * 35))
                self.screen.blit(text, text_rect)
        
        continue_text = self.font_med.render("Presiona ESPACIO para continuar", True, Color.GREEN)
        continue_rect = continue_text.get_rect(center=(center_x, Var.HEIGHT - 80))
        self.screen.blit(continue_text, continue_rect)
        
        pygame.display.flip()

def show_game_tutorial():
    tutorial = Tutorial()
    tutorial.show_tutorial()
    pygame.quit()
    return tutorial.running
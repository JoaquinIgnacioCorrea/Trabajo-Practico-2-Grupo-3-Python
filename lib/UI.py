import pygame
import lib.Color as Color

class GameUI:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.lives = 3
        self.combo = 0
        self.max_combo = 0
        
    def update_score(self, points):
        self.score += points
    
    def update_level(self, new_level):
        self.level = new_level
    
    def update_lives(self, new_lives):
        self.lives = new_lives
    
    def update_combo(self, new_combo):
        self.combo = new_combo
        if self.combo > self.max_combo:
            self.max_combo = self.combo
    
    def draw(self, screen, font_big, font_med, font_small):
        margin = 20
        
        score_text = font_med.render(f"Score: {self.score}", True, Color.TEXT)
        screen.blit(score_text, (margin, margin))
        
        level_text = font_med.render(f"Nivel: {self.level}", True, Color.TEXT)
        screen.blit(level_text, (margin, margin + 40))
        
        lives_text = font_med.render(f"Vidas: {self.lives}", True, Color.TEXT)
        screen.blit(lives_text, (margin, margin + 80))
        
        if self.combo > 0:
            combo_text = font_small.render(f"Combo: {self.combo}x", True, Color.ORANGE)
            screen.blit(combo_text, (margin, margin + 120))
        
        if self.max_combo > 0:
            max_combo_text = font_small.render(f"Mejor Combo: {self.max_combo}x", True, Color.GRAY)
            screen.blit(max_combo_text, (margin, margin + 145))

class GameOverScreen:
    def __init__(self):
        self.show = False
        self.final_score = 0
        self.max_combo = 0
        self.level_reached = 1
    
    def set_game_over_data(self, score, max_combo, level):
        self.show = True
        self.final_score = score
        self.max_combo = max_combo
        self.level_reached = level
    
    def draw(self, screen, font_big, font_med, font_small):
        if not self.show:
            return
        
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(180)
        overlay.fill(Color.DARK)
        screen.blit(overlay, (0, 0))
        
        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2
        
        game_over_text = font_big.render("GAME OVER", True, Color.RED)
        game_over_rect = game_over_text.get_rect(center=(center_x, center_y - 100))
        screen.blit(game_over_text, game_over_rect)
        
        score_text = font_med.render(f"Puntuación Final: {self.final_score}", True, Color.WHITE)
        score_rect = score_text.get_rect(center=(center_x, center_y - 40))
        screen.blit(score_text, score_rect)
        
        level_text = font_med.render(f"Nivel Alcanzado: {self.level_reached}", True, Color.WHITE)
        level_rect = level_text.get_rect(center=(center_x, center_y))
        screen.blit(level_text, level_rect)
        
        combo_text = font_med.render(f"Mejor Combo: {self.max_combo}x", True, Color.ORANGE)
        combo_rect = combo_text.get_rect(center=(center_x, center_y + 40))
        screen.blit(combo_text, combo_rect)
        
        restart_text = font_small.render("Presiona R para reiniciar o ESC para salir", True, Color.GRAY)
        restart_rect = restart_text.get_rect(center=(center_x, center_y + 100))
        screen.blit(restart_text, restart_rect)
import pygame
import os
import lib.Color as Color

class GameUI:
    def __init__(self):
        self._score = 0
        self._level = 1
        self._lives = 3
        self._combo = 0
        self._max_combo = 0
        self._current_operation = None
    
    def set_score(self, score):
        self._score = score
    
    def set_level(self, level):
        self._level = level
    
    def set_lives(self, lives):
        self._lives = lives
    
    def set_combo(self, combo):
        self._combo = combo
    
    def set_max_combo(self, max_combo):
        self._max_combo = max_combo
    
    def set_current_operation(self, operation):
        self._current_operation = operation
    
    def draw(self, screen, font_big, font_med, font_small):
        margin = 20
        border_radius = 15
        
        stats_box_width = 150
        stats_box_height = 190
        stats_bg = pygame.Surface((stats_box_width, stats_box_height), pygame.SRCALPHA)
        pygame.draw.rect(stats_bg, (*Color.WHITE, 120), stats_bg.get_rect(), border_radius=border_radius)
        screen.blit(stats_bg, (margin, margin))
        
        text_margin_x = margin + 10
        text_margin_y = margin + 15
        
        score_text = font_med.render(f"Score: {self._score}", True, Color.DARK)
        screen.blit(score_text, (text_margin_x, text_margin_y))
        
        level_text = font_med.render(f"Nivel: {self._level}", True, Color.DARK)
        screen.blit(level_text, (text_margin_x, text_margin_y + 40))
        
        lives_text = font_med.render(f"Vidas: {self._lives}", True, Color.DARK)
        screen.blit(lives_text, (text_margin_x, text_margin_y + 80))
        
        if self._combo > 0:
            combo_text = font_small.render(f"Combo: {self._combo}x", True, Color.ORANGE)
            screen.blit(combo_text, (text_margin_x, text_margin_y + 120))
        
        if self._max_combo > 0:
            max_combo_text = font_small.render(f"Mejor Combo: {self._max_combo}x", True, Color.GRAY)
            screen.blit(max_combo_text, (text_margin_x, text_margin_y + 145))
        
        if self._current_operation:
            operation_width = 250
            operation_height = 60
            operation_bg = pygame.Surface((operation_width, operation_height), pygame.SRCALPHA)
            pygame.draw.rect(operation_bg, (*Color.WHITE, 120), operation_bg.get_rect(), border_radius=border_radius)
            
            operation_x = screen.get_width() - operation_width - margin
            screen.blit(operation_bg, (operation_x, margin))
            
            operation_text = font_big.render(self._current_operation, True, Color.DARK)
            operation_rect = operation_text.get_rect(center=(operation_x + operation_width // 2, margin + operation_height // 2))
            screen.blit(operation_text, operation_rect)

class GameOverScreen:
    def __init__(self):
        self._show = False
        self._final_score = 0
        self._max_combo = 0
        self._level_reached = 1
        
        game_over_path = os.path.join(os.path.dirname(__file__), "..", "Sprites", "UI", "game_over.png")
        self._game_over_img = pygame.image.load(game_over_path).convert_alpha()
    
    def set_show(self, show):
        self._show = show
    
    def set_game_over_data(self, score, max_combo, level):
        self._show = True
        self._final_score = score
        self._max_combo = max_combo
        self._level_reached = level
    
    def draw(self, screen, font_big, font_med, font_small):
        if not self._show:
            return
        
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(180)
        overlay.fill(Color.DARK)
        screen.blit(overlay, (0, 0))
        
        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2
        
        game_over_rect = self._game_over_img.get_rect(center=(center_x, center_y - 100))
        screen.blit(self._game_over_img, game_over_rect)
        
        score_text = font_med.render(f"Puntuación Final: {self._final_score}", True, Color.WHITE)
        score_rect = score_text.get_rect(center=(center_x, center_y - 40))
        screen.blit(score_text, score_rect)
        
        level_text = font_med.render(f"Nivel Alcanzado: {self._level_reached}", True, Color.WHITE)
        level_rect = level_text.get_rect(center=(center_x, center_y))
        screen.blit(level_text, level_rect)
        
        combo_text = font_med.render(f"Mejor Combo: {self._max_combo}x", True, Color.ORANGE)
        combo_rect = combo_text.get_rect(center=(center_x, center_y + 40))
        screen.blit(combo_text, combo_rect)
        
        restart_text = font_small.render("Presiona R para reiniciar o ESC para salir", True, Color.GRAY)
        restart_rect = restart_text.get_rect(center=(center_x, center_y + 100))
        screen.blit(restart_text, restart_rect)

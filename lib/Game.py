import pygame
import lib.Var as Var
import lib.Color as Color
from lib.Player import Player
from lib.Gate import GateManager
from lib.UI import GameUI, GameOverScreen
from lib.SoundManager import SoundManager

class GameState:
    def __init__(self):
        self.score = Var.INITIAL_SCORE
        self.lives = Var.INITIAL_LIVES
        self.level = Var.INITIAL_LEVEL
        self.combo = Var.INITIAL_COMBO
        self.max_combo = 0
        self.speed = Var.INITIAL_SPEED
        self.game_over = False
        self.running = True
    
    def reset(self):
        self.score = Var.INITIAL_SCORE
        self.lives = Var.INITIAL_LIVES
        self.level = Var.INITIAL_LEVEL
        self.combo = Var.INITIAL_COMBO
        self.max_combo = 0
        self.speed = Var.INITIAL_SPEED
        self.game_over = False
    
    def update_level(self):
        new_level = min(Var.MAX_LEVEL, 1 + self.score // (Var.SCORE_GAIN_BASE * Var.COMBO_LEVEL_UP_INTERVAL))
        if new_level > self.level:
            self.level = new_level
            self.speed = min(Var.MAX_SPEED, Var.INITIAL_SPEED + (self.level - 1) * Var.SPEED_INCREASE)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Var.WIDTH, Var.HEIGHT))
        pygame.display.set_caption("Math Runner")
        self.clock = pygame.time.Clock()
        
        self.font_big = pygame.font.SysFont("arial", Var.FONT_SIZE_BIG, bold=True)
        self.font_med = pygame.font.SysFont("arial", Var.FONT_SIZE_MED, bold=True)
        self.font_small = pygame.font.SysFont("arial", Var.FONT_SIZE_SMALL)
        
        self.player = Player()
        self.gate_manager = GateManager()
        self.game_ui = GameUI()
        self.game_over_screen = GameOverScreen()
        self.sound_manager = SoundManager()
        self.game_state = GameState()
        
        self.sound_manager.play_background_music()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.game_state.game_over:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state.running = False
                else:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.move_to_lane("L")
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.move_to_lane("R")
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state.running = False
    
    def update_game_logic(self, dt):
        if self.game_state.game_over:
            return
        
        self.player.update(dt)
        self.gate_manager.update(dt, self.game_state.level, self.game_state.speed)
        
        collision_result = self.gate_manager.check_collisions(self.player)
        if collision_result is not None:
            if collision_result:
                self.handle_correct_answer()
            else:
                self.handle_wrong_answer()
        
        self.game_state.update_level()
        
        if self.game_state.lives <= 0:
            self.game_over()
    
    def handle_correct_answer(self):
        self.game_state.combo += 1
        if self.game_state.combo > self.game_state.max_combo:
            self.game_state.max_combo = self.game_state.combo
        
        score_gain = Var.SCORE_GAIN_BASE + (self.game_state.combo - 1) * Var.SCORE_GAIN_COMBO_MULTIPLIER
        self.game_state.score += score_gain
        
        self.sound_manager.play_sound('correct')
    
    def handle_wrong_answer(self):
        self.game_state.combo = 0
        self.game_state.lives -= 1
        self.game_state.score = max(0, self.game_state.score - Var.SCORE_PENALTY)
        
        self.sound_manager.play_sound('wrong')
    
    def game_over(self):
        self.game_state.game_over = True
        self.game_over_screen.set_game_over_data(
            self.game_state.score,
            self.game_state.max_combo,
            self.game_state.level
        )
    
    def restart_game(self):
        self.game_state.reset()
        self.gate_manager.clear()
        self.game_over_screen.show = False
        self.player.lane = Var.INITIAL_LANE
        self.player.x = Var.LANE_LEFT_X if self.player.lane == "L" else Var.LANE_RIGHT_X
        self.player.update_rect()
    
    def draw_background(self):
        self.screen.fill(Color.BG)
        
        road_rect = pygame.Rect(0, 0, Var.WIDTH, Var.HEIGHT)
        pygame.draw.rect(self.screen, Color.ROAD, road_rect)
        
        for y in range(0, Var.HEIGHT, 50):
            pygame.draw.line(self.screen, Color.GRAY, (Var.WIDTH//2, y), (Var.WIDTH//2, y + 25), 5)
    
    def render(self):
        self.draw_background()
        
        self.gate_manager.draw(self.screen, self.font_med)
        self.player.draw(self.screen)
        
        self.game_ui.score = self.game_state.score
        self.game_ui.level = self.game_state.level
        self.game_ui.lives = self.game_state.lives
        self.game_ui.combo = self.game_state.combo
        self.game_ui.max_combo = self.game_state.max_combo
        
        self.game_ui.draw(self.screen, self.font_big, self.font_med, self.font_small)
        self.game_over_screen.draw(self.screen, self.font_big, self.font_med, self.font_small)
        
        pygame.display.flip()
    
    def run(self):
        dt = 0
        
        game_loop_active = True
        while game_loop_active and self.game_state.running:
            dt = self.clock.tick(Var.FPS) / 1000.0
            
            self.handle_events()
            self.update_game_logic(dt)
            self.render()
            
            if not self.game_state.running:
                game_loop_active = False
        
        self.sound_manager.stop_background_music()
        pygame.quit()
import pygame
import lib.Var as Var
import lib.Color as Color
from lib.Player import Player
from lib.Gate import GateManager
from lib.UI import GameUI, GameOverScreen
from lib.SoundManager import SoundManager

class GameState:
    def __init__(self):
        self._score = Var.INITIAL_SCORE
        self._lives = Var.INITIAL_LIVES
        self._level = Var.INITIAL_LEVEL
        self._combo = Var.INITIAL_COMBO
        self._max_combo = 0
        self._speed = Var.INITIAL_SPEED
        self._game_over = False
        self._running = True
    
    def get_score(self):
        return self._score
    
    def set_score(self, score):
        self._score = score
    
    def get_lives(self):
        return self._lives
    
    def set_lives(self, lives):
        self._lives = lives
    
    def get_level(self):
        return self._level
    
    def set_level(self, level):
        self._level = level
    
    def get_combo(self):
        return self._combo
    
    def set_combo(self, combo):
        self._combo = combo
    
    def get_max_combo(self):
        return self._max_combo
    
    def set_max_combo(self, max_combo):
        self._max_combo = max_combo
    
    def get_speed(self):
        return self._speed
    
    def set_speed(self, speed):
        self._speed = speed
    
    def get_game_over(self):
        return self._game_over
    
    def set_game_over(self, game_over):
        self._game_over = game_over
    
    def get_running(self):
        return self._running
    
    def set_running(self, running):
        self._running = running
    
    def reset(self):
        self._score = Var.INITIAL_SCORE
        self._lives = Var.INITIAL_LIVES
        self._level = Var.INITIAL_LEVEL
        self._combo = Var.INITIAL_COMBO
        self._max_combo = 0
        self._speed = Var.INITIAL_SPEED
        self._game_over = False
    
    def update_level(self):
        new_level = min(Var.MAX_LEVEL, 1 + self._score // (Var.SCORE_GAIN_BASE * Var.COMBO_LEVEL_UP_INTERVAL))
        if new_level > self._level:
            self._level = new_level
            self._speed = min(Var.MAX_SPEED, Var.INITIAL_SPEED + (self._level - 1) * Var.SPEED_INCREASE)

class Game:
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((Var.WIDTH, Var.HEIGHT))
        pygame.display.set_caption("Math Runner")
        self._clock = pygame.time.Clock()
        
        self._font_big = pygame.font.SysFont("Baloo", Var.FONT_SIZE_BIG, bold=True)
        self._font_med = pygame.font.SysFont("Baloo", Var.FONT_SIZE_MED, bold=True)
        self._font_small = pygame.font.SysFont("Baloo", Var.FONT_SIZE_SMALL)
        
        self._player = Player()
        self._gate_manager = GateManager()
        self._game_ui = GameUI()
        self._game_over_screen = GameOverScreen()
        self._sound_manager = SoundManager()
        self._game_state = GameState()
        
        self._sound_manager.play_background_music()
    
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_state.set_running(False)
            
            elif event.type == pygame.KEYDOWN:
                if self._game_state.get_game_over():
                    if event.key == pygame.K_r:
                        self._restart_game()
                    elif event.key == pygame.K_ESCAPE:
                        self._game_state.set_running(False)
                else:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self._player.move_to_lane("L")
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self._player.move_to_lane("R")
                    elif event.key == pygame.K_ESCAPE:
                        self._game_state.set_running(False)
    
    def _update_game_logic(self, dt):
        if self._game_state.get_game_over():
            return
        
        self._player.update(dt)
        self._gate_manager.update(dt, self._game_state.get_level(), self._game_state.get_speed())
        
        collision_result = self._gate_manager.check_collisions(self._player)
        if collision_result is not None:
            if collision_result:
                self._handle_correct_answer()
            else:
                self._handle_wrong_answer()
        
        self._game_state.update_level()
        
        if self._game_state.get_lives() <= 0:
            self._game_over()
    
    def _handle_correct_answer(self):
        new_combo = self._game_state.get_combo() + 1
        self._game_state.set_combo(new_combo)
        if new_combo > self._game_state.get_max_combo():
            self._game_state.set_max_combo(new_combo)
        
        score_gain = Var.SCORE_GAIN_BASE + (new_combo - 1) * Var.SCORE_GAIN_COMBO_MULTIPLIER
        self._game_state.set_score(self._game_state.get_score() + score_gain)
        
        self._sound_manager.play_sound('correct')
    
    def _handle_wrong_answer(self):
        self._game_state.set_combo(0)
        self._game_state.set_lives(self._game_state.get_lives() - 1)
        self._game_state.set_score(max(0, self._game_state.get_score() - Var.SCORE_PENALTY))
        
        self._sound_manager.play_sound('wrong')
    
    def _game_over(self):
        self._game_state.set_game_over(True)
        self._game_over_screen.set_game_over_data(
            self._game_state.get_score(),
            self._game_state.get_max_combo(),
            self._game_state.get_level()
        )
    
    def _restart_game(self):
        self._game_state.reset()
        self._gate_manager.clear()
        self._game_over_screen.set_show(False)
        self._player.set_lane(Var.INITIAL_LANE)
        self._player.set_x(Var.LANE_LEFT_X if self._player.get_lane() == "L" else Var.LANE_RIGHT_X)
        self._player._update_rect()
    
    def _draw_background(self):
        self._screen.fill(Color.BG)
        
        road_margin = 70
        road_width = Var.WIDTH - (road_margin * 2)
        
        road_rect = pygame.Rect(road_margin, 0, road_width, Var.HEIGHT)
        pygame.draw.rect(self._screen, Color.ROAD, road_rect)
        
        pygame.draw.line(self._screen, Color.ROAD_BORDER, (road_margin, 0), (road_margin, Var.HEIGHT), 4)
        pygame.draw.line(self._screen, Color.ROAD_BORDER, (Var.WIDTH - road_margin, 0), (Var.WIDTH - road_margin, Var.HEIGHT), 4)
        
        for y in range(0, Var.HEIGHT, 50):
            pygame.draw.line(self._screen, Color.ROAD_LINE, (Var.WIDTH//2, y), (Var.WIDTH//2, y + 25), 5)
    
    def _render(self):
        self._draw_background()
        
        self._gate_manager.draw(self._screen, self._font_med)
        self._player.draw(self._screen)
        
        self._game_ui.set_score(self._game_state.get_score())
        self._game_ui.set_level(self._game_state.get_level())
        self._game_ui.set_lives(self._game_state.get_lives())
        self._game_ui.set_combo(self._game_state.get_combo())
        self._game_ui.set_max_combo(self._game_state.get_max_combo())
        
        next_gate = self._gate_manager.get_next_active_gate()
        if next_gate:
            self._game_ui.set_current_operation(next_gate.get_operation())
        else:
            self._game_ui.set_current_operation(None)
        
        self._game_ui.draw(self._screen, self._font_big, self._font_med, self._font_small)
        self._game_over_screen.draw(self._screen, self._font_big, self._font_med, self._font_small)
        
        pygame.display.flip()
    
    def run(self):
        dt = 0
        
        game_loop_active = True
        while game_loop_active and self._game_state.get_running():
            dt = self._clock.tick(Var.FPS) / 1000.0
            
            self._handle_events()
            self._update_game_logic(dt)
            self._render()
            
            if not self._game_state.get_running():
                game_loop_active = False
        
        self._sound_manager.stop_background_music()
        pygame.quit()

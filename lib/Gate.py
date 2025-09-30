import pygame
import random
import lib.Var as Var
import lib.Color as Color

class Gate:
    def __init__(self, operation, correct_answer, wrong_answer, correct_lane):
        self._operation = operation
        self._correct_answer = correct_answer
        self._wrong_answer = wrong_answer
        self._correct_lane = correct_lane
        
        self._y = -100
        self._width = 200
        self._height = 100
        self._speed = Var.INITIAL_SPEED
        
        self._left_x = Var.LANE_LEFT_X
        self._right_x = Var.LANE_RIGHT_X
        
        self._left_rect = pygame.Rect(self._left_x - self._width//2, self._y, self._width, self._height)
        self._right_rect = pygame.Rect(self._right_x - self._width//2, self._y, self._width, self._height)
        
        self._passed = False
        self._answered = False
        self._player_was_correct = False
        self._player_chosen_lane = None
    
    def get_operation(self):
        return self._operation
    
    def get_answered(self):
        return self._answered
    
    def get_y(self):
        return self._y
    
    def get_passed(self):
        return self._passed
    
    def update(self, dt, speed):
        self._speed = speed
        self._y += self._speed * dt * 60
        self._left_rect.y = self._y
        self._right_rect.y = self._y
        
        if self._y > Var.HEIGHT + 50:
            self._passed = True
    
    def check_collision(self, player):
        if player.get_lane() == "L":
            return self._left_rect.colliderect(player.get_rect())
        else:
            return self._right_rect.colliderect(player.get_rect())
    
    def is_correct_choice(self, player_lane):
        return player_lane == self._correct_lane
    
    def mark_answered(self, player_lane, was_correct):
        self._answered = True
        self._player_chosen_lane = player_lane
        self._player_was_correct = was_correct
    
    def draw(self, screen, font):
        if not self._answered:
            left_color = Color.GRAY
            right_color = Color.GRAY
        else:
            if self._player_chosen_lane == "L":
                left_color = Color.GREEN if self._player_was_correct else Color.RED
                right_color = Color.GREEN if self._correct_lane == "R" else Color.RED
            else:
                right_color = Color.GREEN if self._player_was_correct else Color.RED
                left_color = Color.GREEN if self._correct_lane == "L" else Color.RED
        
        self._draw_door(screen, self._left_rect, left_color)
        self._draw_door(screen, self._right_rect, right_color)
        left_answer = self._correct_answer if self._correct_lane == "L" else self._wrong_answer
        right_answer = self._correct_answer if self._correct_lane == "R" else self._wrong_answer
        
        big_font = pygame.font.SysFont("Baloo", 48, bold=True)
        
        left_text = big_font.render(str(left_answer), True, Color.WHITE)
        left_text_rect = left_text.get_rect(center=(self._left_x, self._y + self._height//2))
        screen.blit(left_text, left_text_rect)
        
        right_text = big_font.render(str(right_answer), True, Color.WHITE)
        right_text_rect = right_text.get_rect(center=(self._right_x, self._y + self._height//2))
        screen.blit(right_text, right_text_rect)
    
    def _draw_door(self, screen, rect, color):
        door_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        corner_radius = 20
        
        pygame.draw.rect(door_surface, color, (0, corner_radius, rect.width, rect.height - corner_radius))
        pygame.draw.rect(door_surface, color, (0, 0, rect.width, rect.height - corner_radius//2), 
                        border_top_left_radius=corner_radius, border_top_right_radius=corner_radius)
        pygame.draw.rect(door_surface, Color.DARK, (0, 0, rect.width, rect.height), 5,
                        border_top_left_radius=corner_radius, border_top_right_radius=corner_radius)
        
        screen.blit(door_surface, rect.topleft)

class GateManager:
    def __init__(self):
        self._gates = []
        self._spawn_timer = 0
        self._spawn_interval = Var.INITIAL_SPAWN_INTERVAL
    
    def get_gates(self):
        return self._gates
        
    def _generate_math_problem(self, level):
        difficulty = min(level, 10)
        
        if difficulty <= 3:
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            operation = f"{a} + {b}"
            correct = a + b
        elif difficulty <= 6:
            a = random.randint(1, 12)
            b = random.randint(1, 12)
            if random.choice([True, False]):
                operation = f"{a} + {b}"
                correct = a + b
            else:
                operation = f"{a} - {b}"
                correct = a - b
        else:
            a = random.randint(2, 12)
            b = random.randint(2, 12)
            op_type = random.choice(['add', 'sub', 'mul'])
            
            if op_type == 'add':
                operation = f"{a} + {b}"
                correct = a + b
            elif op_type == 'sub':
                if a < b:
                    a, b = b, a
                operation = f"{a} - {b}"
                correct = a - b
            else:
                operation = f"{a} × {b}"
                correct = a * b
        
        wrong_options = []
        for _ in range(10):
            wrong = correct + random.randint(-5, 5)
            if wrong != correct and wrong not in wrong_options:
                wrong_options.append(wrong)
        
        if not wrong_options:
            wrong_options = [correct + 1, correct - 1, correct + 2]
        
        wrong = random.choice(wrong_options)
        correct_lane = random.choice(["L", "R"])
        
        return operation, correct, wrong, correct_lane
    
    def update(self, dt, level, speed):
        self._spawn_timer += dt
        
        current_interval = max(
            Var.MIN_SPAWN_INTERVAL,
            Var.INITIAL_SPAWN_INTERVAL - (level - 1) * Var.SPAWN_INTERVAL_DECREASE
        )
        
        if self._spawn_timer >= current_interval:
            operation, correct, wrong, correct_lane = self._generate_math_problem(level)
            gate = Gate(operation, correct, wrong, correct_lane)
            self._gates.append(gate)
            self._spawn_timer = 0
        
        for gate in self._gates[:]:
            gate.update(dt, speed)
            if gate.get_passed():
                self._gates.remove(gate)
    
    def check_collisions(self, player):
        for gate in self._gates[:]:
            if gate.check_collision(player) and not gate.get_answered():
                is_correct = gate.is_correct_choice(player.get_lane())
                gate.mark_answered(player.get_lane(), is_correct)
                return is_correct
        return None
    
    def get_next_active_gate(self):
        active_gates = [gate for gate in self._gates if not gate.get_answered()]
        if active_gates:
            return max(active_gates, key=lambda g: g.get_y())
        return None
    
    def draw(self, screen, font):
        for gate in self._gates:
            gate.draw(screen, font)
    
    def clear(self):
        self._gates.clear()

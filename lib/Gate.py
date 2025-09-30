import pygame
import random
import lib.Var as Var
import lib.Color as Color

class Gate:
    def __init__(self, operation, correct_answer, wrong_answer, correct_lane):
        self.operation = operation
        self.correct_answer = correct_answer
        self.wrong_answer = wrong_answer
        self.correct_lane = correct_lane
        
        self.y = -100
        self.width = 200
        self.height = 100
        self.speed = Var.INITIAL_SPEED
        
        self.left_x = Var.LANE_LEFT_X
        self.right_x = Var.LANE_RIGHT_X
        
        self.left_rect = pygame.Rect(self.left_x - self.width//2, self.y, self.width, self.height)
        self.right_rect = pygame.Rect(self.right_x - self.width//2, self.y, self.width, self.height)
        
        self.passed = False
        self.answered = False
        self.player_was_correct = False
        self.player_chosen_lane = None
    
    def update(self, dt, speed):
        self.speed = speed
        self.y += self.speed * dt * 60
        self.left_rect.y = self.y
        self.right_rect.y = self.y
        
        if self.y > Var.HEIGHT + 50:
            self.passed = True
    
    def check_collision(self, player):
        if player.lane == "L":
            return self.left_rect.colliderect(player.rect)
        else:
            return self.right_rect.colliderect(player.rect)
    
    def is_correct_choice(self, player_lane):
        return player_lane == self.correct_lane
    
    def mark_answered(self, player_lane, was_correct):
        self.answered = True
        self.player_chosen_lane = player_lane
        self.player_was_correct = was_correct
    
    def draw(self, screen, font):
        if not self.answered:
            left_color = Color.GRAY
            right_color = Color.GRAY
        else:
            if self.player_chosen_lane == "L":
                left_color = Color.GREEN if self.player_was_correct else Color.RED
                right_color = Color.GREEN if self.correct_lane == "R" else Color.RED
            else:
                right_color = Color.GREEN if self.player_was_correct else Color.RED
                left_color = Color.GREEN if self.correct_lane == "L" else Color.RED
        
        pygame.draw.rect(screen, left_color, self.left_rect)
        pygame.draw.rect(screen, Color.DARK, self.left_rect, 3)
        
        pygame.draw.rect(screen, right_color, self.right_rect)
        pygame.draw.rect(screen, Color.DARK, self.right_rect, 3)
        
        operation_text = font.render(self.operation, True, Color.TEXT)
        operation_y = max(self.y - 22, Var.TOP_SAFE_ZONE)
        operation_rect = operation_text.get_rect(center=(Var.WIDTH//2, operation_y))
        screen.blit(operation_text, operation_rect)
        
        left_answer = self.correct_answer if self.correct_lane == "L" else self.wrong_answer
        right_answer = self.correct_answer if self.correct_lane == "R" else self.wrong_answer
        
        left_text = font.render(str(left_answer), True, Color.WHITE)
        left_text_rect = left_text.get_rect(center=(self.left_x, self.y + self.height//2))
        screen.blit(left_text, left_text_rect)
        
        right_text = font.render(str(right_answer), True, Color.WHITE)
        right_text_rect = right_text.get_rect(center=(self.right_x, self.y + self.height//2))
        screen.blit(right_text, right_text_rect)

class GateManager:
    def __init__(self):
        self.gates = []
        self.spawn_timer = 0
        self.spawn_interval = Var.INITIAL_SPAWN_INTERVAL
        
    def generate_math_problem(self, level):
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
        self.spawn_timer += dt
        
        current_interval = max(
            Var.MIN_SPAWN_INTERVAL,
            Var.INITIAL_SPAWN_INTERVAL - (level - 1) * Var.SPAWN_INTERVAL_DECREASE
        )
        
        if self.spawn_timer >= current_interval:
            operation, correct, wrong, correct_lane = self.generate_math_problem(level)
            gate = Gate(operation, correct, wrong, correct_lane)
            self.gates.append(gate)
            self.spawn_timer = 0
        
        for gate in self.gates[:]:
            gate.update(dt, speed)
            if gate.passed:
                self.gates.remove(gate)
    
    def check_collisions(self, player):
        for gate in self.gates[:]:
            if gate.check_collision(player) and not gate.answered:
                is_correct = gate.is_correct_choice(player.lane)
                gate.mark_answered(player.lane, is_correct)
                return is_correct
        return None
    
    def draw(self, screen, font):
        for gate in self.gates:
            gate.draw(screen, font)
    
    def clear(self):
        self.gates.clear()
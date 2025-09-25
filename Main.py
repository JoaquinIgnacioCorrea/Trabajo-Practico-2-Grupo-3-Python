# Punto de acceso al juego
import pygame
import random
import sys
import lib.Color as Color
import lib.Var  as Var

# -------------------------
# Configuración principal
# -------------------------
pygame.init()
screen = pygame.display.set_mode((Var.WIDTH, Var.HEIGHT))
pygame.display.set_caption("Math Runner - Prototype")
clock = pygame.time.Clock()

FONT_BIG = pygame.font.SysFont("arial", Var.FONT_SIZE_BIG, bold=True)
FONT_MED = pygame.font.SysFont("arial", Var.FONT_SIZE_MED, bold=True)
FONT_SMALL = pygame.font.SysFont("arial", Var.FONT_SIZE_SMALL)


# -------------------------
# Estado del juego
# -------------------------
class Gate:
    """Puertas con dos opciones. Caen hacia el jugador."""
    def __init__(self, question, correct, wrong, correct_side, speed):
        self.question = question
        self.correct  = correct
        self.wrong    = wrong
        self.correct_side = correct_side  # "L" o "R"
        self.y = -Var.GATE_Y  # arranca fuera de pantalla
        self.speed = speed
        self.hit_checked = False  # para evaluar una sola vez

    def update(self):
        self.y += self.speed

    def draw(self, surf):
        # Carretera (ya la dibuja el mundo, acá solo las puertas)
        gate_w, gate_h = 160, 120
        pad = 12

        # Puerta izquierda
        left_rect  = pygame.Rect(Var.LANE_LEFT_X - gate_w//2, self.y, gate_w, gate_h)
        # Puerta derecha
        right_rect = pygame.Rect(Var.LANE_RIGHT_X - gate_w//2, self.y, gate_w, gate_h)

        pygame.draw.rect(surf, Color.WHITE, left_rect, border_radius=18)
        pygame.draw.rect(surf, Color.WHITE, right_rect, border_radius=18)
        pygame.draw.rect(surf, Color.GRAY, left_rect, 3, border_radius=18)
        pygame.draw.rect(surf, Color.GRAY, right_rect, 3, border_radius=18)

        # Etiquetas de números
        left_val  = self.correct if self.correct_side == "L" else self.wrong
        right_val = self.correct if self.correct_side == "R" else self.wrong

        txt_l = FONT_BIG.render(str(left_val), True, Color.TEXT)
        txt_r = FONT_BIG.render(str(right_val), True, Color.TEXT)
        surf.blit(txt_l, txt_l.get_rect(center=left_rect.center))
        surf.blit(txt_r, txt_r.get_rect(center=right_rect.center))

        # La pregunta arriba de las puertas
        qsurf = FONT_MED.render(self.question, True, Color.DARK)
        qrect = qsurf.get_rect(center=(Var.WIDTH//2, self.y - 30))
        surf.blit(qsurf, qrect)

    def offscreen(self):
        return self.y > Var.HEIGHT + 40


def make_problem(level):
    """Genera una cuenta y respuestas según la dificultad (level)."""
    # Aumentamos el rango según level
    span = 5 + level * 3
    op = random.choice(["+", "-"]) if level < 4 else random.choice(["+", "-", "*"])

    if op == "+":
        a = random.randint(1, span)
        b = random.randint(1, span)
        ans = a + b
    elif op == "-":
        a = random.randint(2, span + 3)
        b = random.randint(1, a)  # evita negativos al inicio
        ans = a - b
    else:  # "*"
        a = random.randint(2, max(3, level + 2))
        b = random.randint(2, max(3, level + 2))
        ans = a * b

    # Distractor: cerca pero distinto
    delta_choices = {1, 2, 3, -1, -2, -3}
    if level >= 5:
        delta_choices |= {4, -4, 5, -5}
    wrong = ans + random.choice(tuple(delta_choices))
    while wrong == ans:
        wrong += random.choice([-2, -1, 1, 2])

    question = f"{a} {op} {b} = ?"
    correct_side = random.choice(["L", "R"])
    return question, ans, wrong, correct_side


def draw_world(surf, lane):
    surf.fill(Color.BG)
    # "Camino"
    road_rect = pygame.Rect(Var.WIDTH//2 - 240, 0, 480, Var.HEIGHT)
    pygame.draw.rect(surf, Color.ROAD, road_rect, border_radius=16)

    # Línea central punteada para dar sensación de movimiento
    dash_h = 35
    gap = 25
    for y in range(-dash_h, Var.HEIGHT + dash_h, dash_h + gap):
        pygame.draw.rect(surf, Color.WHITE, (Var.WIDTH//2 - 4, y + (Var.scroll_offset % (dash_h+gap)), 8, dash_h), border_radius=4)

    # Jugador (niño con mochila) como un rectángulo + "mochila"
    px = Var.LANE_LEFT_X if lane == "L" else Var.LANE_RIGHT_X
    body = pygame.Rect(0, 0, 46, 60)
    body.center = (px, Var.PLAYER_Y)
    pygame.draw.rect(surf, Color.ORANGE, body, border_radius=10)
    # cabeza simple
    pygame.draw.circle(surf, Color.WHITE, (px, Var.PLAYER_Y - 46), 20)
    pygame.draw.circle(surf, Color.DARK,  (px - 6, Var.PLAYER_Y - 50), 3)
    pygame.draw.circle(surf, Color.DARK,  (px + 6, Var.PLAYER_Y - 50), 3)
    # mochila
    backpack = pygame.Rect(0, 0, 30, 36)
    backpack.center = (px, Var.PLAYER_Y - 8)
    pygame.draw.rect(surf, (180, 200, 255), backpack, border_radius=6)
    pygame.draw.rect(surf, (120, 140, 200), backpack, 2, border_radius=6)


def draw_hud(surf, score, lives, level, speed, combo, last_feedback):
    # Score / Level / Speed
    hud = FONT_MED.render(f"Score: {score}   Lives: {lives}   Lv: {level}   Spd:{speed:.1f}   Combo:{combo}", True, Color.TEXT)
    surf.blit(hud, (20, 20))

    # Feedback de acierto/error
    if last_feedback:
        text, color, timer = last_feedback
        if timer > 0:
            fb = FONT_BIG.render(text, True, color)
            surf.blit(fb, fb.get_rect(center=(Var.WIDTH//2, 70)))


def evaluate_gate(gate, lane):
    """Devuelve (acerto: bool) comparando la elección con la puerta correcta."""
    return (lane == gate.correct_side)


# -------------------------
# Bucle principal
# -------------------------
def main():
    lane = Var.INITIAL_LANE
    score = Var.INITIAL_SCORE
    lives = Var.INITIAL_LIVES
    level = Var.INITIAL_LEVEL
    combo = Var.INITIAL_COMBO

    # Velocidad base y spawn
    speed = Var.INITIAL_SPEED
    spawn_cd = Var.INITIAL_SPAWN_CD
    spawn_interval = Var.INITIAL_SPAWN_INTERVAL

    gates = []
    last_feedback = None  # (texto, color, timer_frames)

    running = True
    while running:
        dt = clock.tick(Var.FPS) / 1000.0  # segundos
        # -------- eventos --------
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_LEFT, pygame.K_a):
                    lane = "L"
                elif e.key in (pygame.K_RIGHT, pygame.K_d):
                    lane = "R"
                elif e.key == pygame.K_ESCAPE:
                    running = False

        # -------- lógica --------
        # Spawnear puertas
        spawn_cd -= dt
        if spawn_cd <= 0:
            q, ans, wrong, side = make_problem(level)
            gates.append(Gate(q, ans, wrong, side, speed))
            spawn_cd = spawn_interval

        # Actualizar puertas
        for g in gates:
            g.speed = speed
            g.update()

        # Evaluar cuando la puerta pasa por el umbral del jugador
        # (solo una vez por puerta)
        for g in gates:
            # Umbral de "colisión" vertical
            if not g.hit_checked and (Var.PLAYER_Y - 40) <= (g.y + 60) <= (Var.PLAYER_Y + 20):
                correct = evaluate_gate(g, lane)
                g.hit_checked = True
                if correct:
                    gained = Var.SCORE_GAIN_BASE + Var.SCORE_GAIN_COMBO_MULTIPLIER * combo
                    score += gained
                    combo += 1
                    last_feedback = ("¡Correcto!", Color.GREEN, int(Var.FEEDBACK_DURATION_FRAMES * Var.FPS))
                    # subir dificultad levemente con racha
                    if combo % Var.COMBO_LEVEL_UP_INTERVAL == 0:
                        level = min(Var.MAX_LEVEL, level + 1)
                        speed = min(Var.MAX_SPEED, speed + Var.SPEED_INCREASE)
                        # a mayor velocidad, acortamos poquito el spawn
                        spawn_interval = max(Var.MIN_SPAWN_INTERVAL, spawn_interval - Var.SPAWN_INTERVAL_DECREASE)
                else:
                    score -= Var.SCORE_PENALTY
                    combo = 0
                    lives -= 1
                    last_feedback = ("Error", Color.RED, int(Var.FEEDBACK_DURATION_FRAMES * Var.FPS))
                    # pequeña penalización: bajar un toque la velocidad si te va mal
                    speed = max(Var.MIN_SPEED, speed - Var.SPEED_PENALTY)

        # Quitar puertas fuera de pantalla
        gates = [g for g in gates if not g.offscreen()]

        # Actualizar timer de feedback
        if last_feedback:
            text, color, timer = last_feedback
            timer -= 1
            last_feedback = (text, color, timer) if timer > 0 else None

        # Game Over
        if lives <= 0:
            game_over(screen, score)
            return

        # -------- render --------
        Var.scroll_offset += speed * 1.2
        draw_world(screen, lane)
        for g in gates:
            g.draw(screen)
        draw_hud(screen, score, lives, level, speed, combo, last_feedback)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


def game_over(surf, score):
    """Pantalla simple de fin."""
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                else:
                    main()  # reiniciar

        surf.fill(Color.BG)
        title = FONT_BIG.render("GAME OVER", True, Color.RED)
        msg1  = FONT_MED.render(f"Score final: {score}", True, Color.DARK)
        msg2  = FONT_SMALL.render("Enter/espacio para reiniciar | Esc para salir", True, Color.TEXT)

        surf.blit(title, title.get_rect(center=(Var.WIDTH//2, Var.HEIGHT//2 - 40)))
        surf.blit(msg1,  msg1.get_rect(center=(Var.WIDTH//2, Var.HEIGHT//2 + 20)))
        surf.blit(msg2,  msg2.get_rect(center=(Var.WIDTH//2, Var.HEIGHT//2 + 70)))
        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    main()

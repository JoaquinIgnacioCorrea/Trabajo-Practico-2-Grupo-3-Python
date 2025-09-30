import pygame
import sys
import os
import lib.Color as Color
import lib.Var as Var
from lib.Game import Game
from Creditos import CreditsScreen

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets", "ui")

class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Var.WIDTH, Var.HEIGHT))
        pygame.display.set_caption("Math Runner - Menú")
        self.clock = pygame.time.Clock()

        # Fuentes (fallback si no tenés Luckiest Guy / Baloo instaladas)
        self.font_title = pygame.font.SysFont("luckiest guy", 56, bold=True)
        self.font_small = pygame.font.SysFont("baloo", 22) or pygame.font.SysFont(None, 22)

        # Carga de imágenes del menú
        def load_img(name):
            path = os.path.join(ASSETS_DIR, name)
            return pygame.image.load(path).convert_alpha()

        # Fallback si faltan assets
        try:
            self.bg      = pygame.image.load(os.path.join(ASSETS_DIR, "menu_bg.png")).convert()
            self.title   = load_img("title.png")
            self.btn_j   = load_img("btn_jugar.png")
            self.btn_c   = load_img("btn_creditos.png")
            self.btn_s   = load_img("btn_salir.png")
        except Exception:
            # Fondo plano si faltan imágenes
            self.bg = pygame.Surface((Var.WIDTH, Var.HEIGHT))
            self.bg.fill(Color.BG)
            self.title = self._make_button("MATH RUNNER", (520,110), Color.GRAY)
            self.btn_j = self._make_button("JUGAR", (260,70), Color.GREEN)
            self.btn_c = self._make_button("CREDITOS", (260,70), Color.GRAY)
            self.btn_s = self._make_button("SALIR", (260,70), Color.RED)

        # Posiciones
        cx = Var.WIDTH // 2
        self.title_rect = self.title.get_rect(center=(cx, 170))
        self.buttons = [
            ("JUGAR",    self.btn_j, None),
            ("CREDITOS", self.btn_c, None),
            ("SALIR",    self.btn_s, None),
        ]
        gap = 90
        start_y = 300
        for i, (name, surf, _) in enumerate(self.buttons):
            rect = surf.get_rect(center=(cx, start_y + i*gap))
            self.buttons[i] = (name, surf, rect)

        self.selected = 0
        self.running = True

    def _make_button(self, text, size, fill):
        """Fallback: genera un botón rápido si falta el PNG"""
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(surf, fill, surf.get_rect(), border_radius=18)
        pygame.draw.rect(surf, Color.TEXT, surf.get_rect(), width=3, border_radius=18)
        font = pygame.font.SysFont("luckiest guy", 36, bold=True)
        txt = font.render(text, True, (255,255,255))
        surf.blit(txt, txt.get_rect(center=surf.get_rect().center))
        return surf

    # ---------------------- LOOP ----------------------
    def run(self):
        while self.running:
            dt = self.clock.tick(Var.FPS) / 1000.0
            self._handle_events()
            self._draw()
        pygame.quit()

    # ---------------------- INPUT ----------------------
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE,):
                    self.running = False
                elif event.key in (pygame.K_UP, pygame.K_w):
                    self.selected = (self.selected - 1) % len(self.buttons)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected = (self.selected + 1) % len(self.buttons)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self._activate(self.selected)

            elif event.type == pygame.MOUSEMOTION:
                # Hover con el mouse
                mx, my = event.pos
                for i, (_, _, rect) in enumerate(self.buttons):
                    if rect.collidepoint(mx, my):
                        self.selected = i

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for i, (_, _, rect) in enumerate(self.buttons):
                    if rect.collidepoint(mx, my):
                        self._activate(i)

    def _activate(self, index):
        name, _, _ = self.buttons[index]
        if name == "JUGAR":
            game = Game()
            game.run()     # vuelve al menú cuando termina
        elif name == "CREDITOS":
            CreditsScreen(self.screen, self.clock).run()
        elif name == "SALIR":
            self.running = False

    # ---------------------- DRAW ----------------------
    def _draw(self):
        # Fondo liso sin imagen de cabecera
        self.screen.fill(Color.BG)

        # Título
        self.screen.blit(self.title, self.title_rect)

        # Botones
        for i, (name, surf, rect) in enumerate(self.buttons):
            # Efecto hover: leve escala
            scaled = pygame.transform.smoothscale(
                surf, (int(rect.w * (1.04 if i == self.selected else 1.0)),
                       int(rect.h * (1.04 if i == self.selected else 1.0)))
            )
            draw_rect = scaled.get_rect(center=rect.center)
            self.screen.blit(scaled, draw_rect)

        # Instrucciones
        hint1 = self.font_small.render("IZQ/DER o A/D para mover, ENTER para seleccionar", True, Color.TEXT)
        hint2 = self.font_small.render("ESC para salir", True, Color.TEXT)
        self.screen.blit(hint1, (Var.WIDTH//2 - hint1.get_width()//2, Var.HEIGHT - 70))
        self.screen.blit(hint2, (Var.WIDTH//2 - hint2.get_width()//2, Var.HEIGHT - 45))

        pygame.display.flip()


if __name__ == "__main__":
    Menu().run()

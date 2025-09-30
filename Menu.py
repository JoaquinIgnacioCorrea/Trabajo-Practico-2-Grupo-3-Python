import pygame
import sys
import os
import lib.Color as Color
import lib.Var as Var
from lib.Game import Game
from Creditos import CreditsScreen

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "Sprites", "UI")
BACKGROUND_DIR = os.path.join(os.path.dirname(__file__), "Sprites", "Fondos")

class Menu:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self._screen = pygame.display.set_mode((Var.WIDTH, Var.HEIGHT))
        pygame.display.set_caption("Math Runner - Menú")
        self._clock = pygame.time.Clock()

        pygame.mixer.music.load("sounds/fondo.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        self._font_small = pygame.font.SysFont("Baloo", 22)

        def load_img(name):
            path = os.path.join(ASSETS_DIR, name)
            return pygame.image.load(path).convert_alpha()

        self._bg = pygame.image.load(os.path.join(BACKGROUND_DIR, "menu_bg.png")).convert()
        self._title = load_img("title.png")
        self._btn_j = load_img("btn_jugar.png")
        self._btn_c = load_img("btn_creditos.png")
        self._btn_s = load_img("btn_salir.png")
        self._maxi = load_img("maxi.png")
        self._instrucciones = load_img("instrucciones.png")

        cx = Var.WIDTH // 2
        self._title_rect = self._title.get_rect(center=(cx, 115))
        
        jugar_rect = self._btn_j.get_rect()
        jugar_rect.midleft = (50, 320)
        
        salir_rect = self._btn_s.get_rect()
        salir_rect.midleft = (50, 420)
        
        creditos_rect = self._btn_c.get_rect()
        creditos_rect.bottomright = (Var.WIDTH - 20, Var.HEIGHT - 20)
        
        self._buttons = [
            ("JUGAR",    self._btn_j, jugar_rect),
            ("CREDITOS", self._btn_c, creditos_rect),
            ("SALIR",    self._btn_s, salir_rect),
        ]

        self._maxi_rect = self._maxi.get_rect()
        self._maxi_rect.bottomright = (Var.WIDTH, Var.HEIGHT - 80)
        
        self._instrucciones_rect = self._instrucciones.get_rect()
        self._instrucciones_rect.midleft = (50, salir_rect.bottom + 120)
        
        self._selected = 0
        self._running = True

    def run(self):
        while self._running:
            dt = self._clock.tick(Var.FPS) / 1000.0
            self._handle_events()
            self._draw()
        pygame.mixer.music.stop()
        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE,):
                    self._running = False
                elif event.key in (pygame.K_UP, pygame.K_w):
                    self._selected = (self._selected - 1) % len(self._buttons)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self._selected = (self._selected + 1) % len(self._buttons)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self._activate(self._selected)

            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                for i, (_, _, rect) in enumerate(self._buttons):
                    if rect.collidepoint(mx, my):
                        self._selected = i

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for i, (_, _, rect) in enumerate(self._buttons):
                    if rect.collidepoint(mx, my):
                        self._activate(i)

    def _activate(self, index):
        name, _, _ = self._buttons[index]
        if name == "JUGAR":
            pygame.mixer.music.stop()
            game = Game()
            game.run()
            pygame.mixer.music.play(-1)
        elif name == "CREDITOS":
            CreditsScreen(self._screen, self._clock).run()
        elif name == "SALIR":
            self._running = False

    def _draw(self):
        self._screen.blit(self._bg, (0, 0))
        self._screen.blit(self._maxi, self._maxi_rect)
        self._screen.blit(self._title, self._title_rect)

        for i, (name, surf, rect) in enumerate(self._buttons):
            scaled = pygame.transform.smoothscale(
                surf, (int(rect.w * (1.04 if i == self._selected else 1.0)),
                       int(rect.h * (1.04 if i == self._selected else 1.0)))
            )
            draw_rect = scaled.get_rect(center=rect.center)
            self._screen.blit(scaled, draw_rect)

        self._screen.blit(self._instrucciones, self._instrucciones_rect)
        pygame.display.flip()


if __name__ == "__main__":
    Menu().run()

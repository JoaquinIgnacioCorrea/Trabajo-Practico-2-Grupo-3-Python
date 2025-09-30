"""
Math Runner - Juego Educativo de Matemáticas
============================================

INFORMACIÓN DEL JUEGO:
- Nombre: Math Runner
- Versión: 1.0.0
- Género: Educational Game / Endless Runner
- Plataforma: PC (Windows, Linux, Mac)
- Motor: Pygame
- Lenguaje: Python 3.11+

OBJETIVO EDUCATIVO:
Ayudar a los estudiantes a practicar y mejorar sus habilidades matemáticas
básicas (suma, resta, multiplicación) de manera divertida y interactiva.

DESARROLLADO PARA:
UAI - Universidad Abierta Interamericana
Materia: Python
Trabajo Práctico 2
Año: 2025

GRUPO 3:
Lucas Joaquin Carranza
Joaquín Ignacio Correa
Mariano Tomas Pocztaruk
Juan Manuel Stecklain

TECNOLOGÍAS UTILIZADAS:
- Python 3.11
- Pygame 2.6.1
- Git para control de versiones

AGRADECIMIENTOS:
- A los profesores de la materia Python
- A la comunidad de Pygame
- A todos los que contribuyeron al proyecto

LICENCIA:
Este proyecto es desarrollado con fines académicos.

FECHA DE DESARROLLO:
Septiembre 2025
"""

def mostrar_creditos():
    print(__doc__)

def obtener_info_juego():
    return {
        "nombre": "Math Runner",
        "version": "1.0.0",
        "genero": "Educational Game / Endless Runner",
        "motor": "Pygame",
        "lenguaje": "Python 3.11+",
        "grupo": "Grupo 3",
        "materia": "Python - UAI",
        "año": 2025
    }

if __name__ == "__main__":
    mostrar_creditos()

import pygame
import lib.Color as Color
import lib.Var as Var

class CreditsScreen:
    def __init__(self, screen=None, clock=None):
        pygame.init()
        self._owns_display = screen is None
        self._screen = screen or pygame.display.set_mode((Var.WIDTH, Var.HEIGHT))
        self._clock = clock or pygame.time.Clock()
        pygame.display.set_caption("Créditos - Math Runner")

        self._font_title = pygame.font.SysFont("Luckiest Guy", 48, bold=True)
        self._font_text = pygame.font.SysFont("Baloo", 24)
        self._font_btn = pygame.font.SysFont("Luckiest Guy", 28, bold=True)

        self._btn_rect = pygame.Rect(0, 0, 180, 54)
        self._btn_rect.center = (Var.WIDTH // 2, Var.HEIGHT - 80)

        self._running = True

    def run(self):
        while self._running:
            self._clock.tick(Var.FPS)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self._running = False
                elif e.type == pygame.KEYDOWN and e.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    self._running = False
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if self._btn_rect.collidepoint(e.pos):
                        self._running = False

            self._draw()

        if self._owns_display:
            pygame.quit()

    def _draw(self):
        self._screen.fill(Color.BG)

        title = self._font_title.render("CRÉDITOS", True, Color.TEXT)
        self._screen.blit(title, (Var.WIDTH//2 - title.get_width()//2, 40))

        lines = [
            "Math Runner — TP Grupo 3 (UAI)",
            "Versión: 1.0.0",
            "Programación / Arte / Sonido:",
            "— Equipo Grupo 3",
            "",
            "Gracias por jugar y aprender."
        ]
        y = 140
        for line in lines:
            txt = self._font_text.render(line, True, Color.TEXT)
            self._screen.blit(txt, (Var.WIDTH//2 - txt.get_width()//2, y))
            y += 36

        pygame.draw.rect(self._screen, Color.GRAY, self._btn_rect, border_radius=14)
        pygame.draw.rect(self._screen, Color.TEXT, self._btn_rect, 3, border_radius=14)
        lbl = self._font_btn.render("VOLVER", True, (255,255,255))
        self._screen.blit(lbl, lbl.get_rect(center=self._btn_rect.center))

        pygame.display.flip()

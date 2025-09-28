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
    """
    Función para mostrar los créditos del juego
    """
    print(__doc__)

def obtener_info_juego():
    """
    Retorna un diccionario con la información básica del juego
    """
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
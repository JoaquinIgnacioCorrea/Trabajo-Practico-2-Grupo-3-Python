# Variables globales

# ================================
# CONSTANTES DE CONFIGURACIÓN
# ================================
# Dimensiones de pantalla
WIDTH, HEIGHT = 900, 600
LANE_LEFT_X  = WIDTH // 2 - 120
LANE_RIGHT_X = WIDTH // 2 + 120
PLAYER_Y     = HEIGHT - 120
FPS          = 60

# Tamaños de fuente
FONT_SIZE_BIG = 64
FONT_SIZE_MED = 32
FONT_SIZE_SMALL = 22

# Posición de las puertas
GATE_Y = 160

# ================================
# CONSTANTES DEL JUEGO
# ================================
# Estado inicial del jugador
INITIAL_LANE = "L"
INITIAL_SCORE = 0
INITIAL_LIVES = 3
INITIAL_LEVEL = 1
INITIAL_COMBO = 0

# Velocidad y spawn
INITIAL_SPEED = 4.0
INITIAL_SPAWN_CD = 0.0
INITIAL_SPAWN_INTERVAL = 1.6  # segundos entre puertas

# Límites del juego
MAX_LEVEL = 20
MAX_SPEED = 12.0
MIN_SPEED = 3.5
MIN_SPAWN_INTERVAL = 0.9

# Puntuación
SCORE_GAIN_BASE = 10
SCORE_GAIN_COMBO_MULTIPLIER = 2
SCORE_PENALTY = 5

# Combo y dificultad
COMBO_LEVEL_UP_INTERVAL = 3
SPEED_INCREASE = 0.4
SPAWN_INTERVAL_DECREASE = 0.05
SPEED_PENALTY = 0.2

# Feedback timing
FEEDBACK_DURATION_FRAMES = 0.6

# ================================
# VARIABLES GLOBALES
# ================================
# Variable global para scroll
scroll_offset = 0.0
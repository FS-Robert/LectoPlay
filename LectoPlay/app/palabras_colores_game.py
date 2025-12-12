# app/palabras_colores_game.py

import random

# Lista de niveles del juego
LEVELS = [
    {"word": "Rojo", "color": "red"},
    {"word": "Azul", "color": "blue"},
    {"word": "Verde", "color": "green"},
    {"word": "Amarillo", "color": "yellow"},
    {"word": "Rosa", "color": "pink"},
    {"word": "Morado", "color": "purple"},
]

# Total de niveles
def total_levels():
    return len(LEVELS)

# Obtener nivel actual
def get_level(index):
    return LEVELS[index]

# Generar opciones (una correcta + 3 incorrectas)
def make_choices(correct_color):
    """Genera 4 colores mezclados donde uno es el correcto."""
    colores = ["red", "blue", "green", "yellow", "pink", "purple"]

    # Tomamos 3 colores aleatorios
    choices = random.sample(colores, 3)

    # Aseguramos que uno sea correcto
    if correct_color not in choices:
        choices[random.randint(0, 2)] = correct_color

    random.shuffle(choices)
    return choices

# Verificar respuesta
def check_choice(choice, level_idx, score):
   
    correct_color = LEVELS[level_idx]["color"]

    if choice == correct_color:
        score += 1
        message = "✔ ¡Correcto!"
        correct = True
    else:
        message = f"✘ Incorrecto. Era {correct_color}."
        correct = False

    # Pasar al siguiente nivel
    level_idx += 1

    # Verificar si se terminó el juego
    finished = level_idx >= len(LEVELS)

    return level_idx, score, correct, message, finished

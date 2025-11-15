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

def total_levels():
    return len(LEVELS)

def get_level(index):
    return LEVELS[index]

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

def check_choice(choice, level_idx, score):
    """
    choice: color elegido
    return: (nuevoNivel, nuevoScore, correct, mensaje)
    """
    correct_color = LEVELS[level_idx]["color"]

    if choice == correct_color:
        score += 1
        message = "✔ ¡Correcto!"
        correct = True
    else:
        message = "✘ Incorrecto"
        correct = False

    level_idx += 1

    return level_idx, score, correct, message

"""Lógica del juego 'Encuentra la letra'.

Este módulo expone funciones puras que no dependen de Django, de forma que
la vista puede delegar la lógica y ser más sencilla y testeable.
"""
import random
from typing import List, Dict, Tuple

# Definición de niveles 
LEVELS: List[Dict[str, str]] = [
    {"word": "gato", "target": "a"},
    {"word": "casa", "target": "s"},
    {"word": "sol", "target": "o"},
    {"word": "mesa", "target": "m"},
    {"word": "perro", "target": "p"},
    {"word": "papaya", "target": "y"},
    {"word": "flor", "target": "l"},
    {"word": "manzana", "target": "z"},
    {"word": "libro", "target": "b"},
    {"word": "silla", "target": "l"},
]


def total_levels() -> int:
    """Devuelve el número total de niveles."""
    return len(LEVELS)


def get_level(level_idx: int) -> Dict[str, str]:
    """Devuelve el diccionario del nivel, lanza IndexError si no existe."""
    return LEVELS[level_idx]


def spaced_word(word: str) -> str:
    """Devuelve la palabra con espacios entre letras para mostrar en la UI."""
    return ' '.join(list(word))


def make_choices(word: str, target: str, count: int = 6, rng=random) -> List[str]:
    """Genera una lista de 'count' letras que incluye la target y distractores.

    - Se incluyen letras únicas de la palabra como distractores.
    - Si faltan opciones se rellenan con letras aleatorias del alfabeto.
    - El resultado está barajado.
    """
    if not target or not isinstance(target, str):
        raise ValueError('target debe ser una cadena no vacía')

    uniq = list(dict.fromkeys(list(word))) if word else []
    letters = set(l.lower() for l in uniq if l.strip())
    letters.add(target.lower())

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    while len(letters) < count:
        letters.add(rng.choice(alphabet))

    choices = list(letters)
    rng.shuffle(choices)
    return choices


def check_choice(choice: str, level_idx: int, score: int) -> Tuple[int, int, bool, str]:
    """Comprueba la elección del usuario para un nivel dado.

    Retorna una tupla (new_level_idx, new_score, correct, message).
    - Si la elección es correcta: avanza el nivel y suma 10 puntos.
    - Si incorrecta: no avanza y devuelve un mensaje de error.
    """
    total = total_levels()
    if level_idx >= total:
        return level_idx, score, False, 'Juego ya completado.'

    lvl = get_level(level_idx)
    correct = lvl['target'].lower()
    if choice is None:
        return level_idx, score, False, 'No se envió ninguna elección.'

    if choice.lower() == correct:
        score += 10
        level_idx += 1
        return level_idx, score, True, '¡Correcto!'
    else:
        return level_idx, score, False, 'No es correcto. Intenta de nuevo.'

#Lógica del juego 'Encuentra la letra'.#

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
    {"word": "ventana", "target": "t"},
    {"word": "puerta", "target": "r"},
    {"word": "coche", "target": "h"},
    {"word": "avión", "target": "n"},
    {"word": "barco", "target": "c"},
    {"word": "árbol", "target": "b"},
    {"word": "estrella", "target": "r"},
    {"word": "nube", "target": "u"},
    {"word": "playa", "target": "y"},
    {"word": "montaña", "target": "t"},
    {"word": "río", "target": "í"},
    {"word": "lago", "target": "g"},
    {"word": "bosque", "target": "q"},
    {"word": "desierto", "target": "s"},
    {"word": "isla", "target": "s"},
    {"word": "cascada", "target": "d"},
    # --- Animales (16) ---
    {"word": "león", "target": "l"},
    {"word": "tigre", "target": "g"},
    {"word": "elefante", "target": "f"},
    {"word": "jirafa", "target": "j"},
    {"word": "mono", "target": "m"},
    {"word": "pato", "target": "p"},
    {"word": "vaca", "target": "v"},
    {"word": "oveja", "target": "j"},
    {"word": "conejo", "target": "c"},
    {"word": "tortuga", "target": "t"},
    {"word": "pez", "target": "z"},
    {"word": "ballena", "target": "b"},
    {"word": "delfín", "target": "f"},
    {"word": "oso", "target": "s"},
    {"word": "ratón", "target": "r"},
    {"word": "pájaro", "target": "j"},

    # --- Comida (14) ---
    {"word": "pan", "target": "p"},
    {"word": "leche", "target": "c"},
    {"word": "queso", "target": "q"},
    {"word": "huevo", "target": "h"},
    {"word": "sopa", "target": "s"},
    {"word": "ensalada", "target": "d"},
    {"word": "fruta", "target": "f"},
    {"word": "plátano", "target": "t"},
    {"word": "uva", "target": "v"},
    {"word": "naranja", "target": "j"},
    {"word": "limón", "target": "m"},
    {"word": "tomate", "target": "t"},
    {"word": "patata", "target": "p"},
    {"word": "maíz", "target": "z"},

    # --- Cuerpo y Ropa (15) ---
    {"word": "mano", "target": "n"},
    {"word": "pie", "target": "i"},
    {"word": "cabeza", "target": "z"},
    {"word": "ojo", "target": "j"},
    {"word": "nariz", "target": "z"},
    {"word": "boca", "target": "c"},
    {"word": "oreja", "target": "r"},
    {"word": "pelo", "target": "l"},
    {"word": "brazo", "target": "b"},
    {"word": "zapato", "target": "z"},
    {"word": "camisa", "target": "s"},
    {"word": "pantalón", "target": "n"},
    {"word": "vestido", "target": "v"},
    {"word": "sombrero", "target": "m"},
    {"word": "calcetín", "target": "c"},

    # --- Escuela y Objetos (15) ---
    {"word": "lápiz", "target": "z"},
    {"word": "goma", "target": "g"},
    {"word": "papel", "target": "p"},
    {"word": "tijeras", "target": "j"},
    {"word": "mochila", "target": "c"},
    {"word": "cuaderno", "target": "d"},
    {"word": "regla", "target": "g"},
    {"word": "reloj", "target": "j"},
    {"word": "teléfono", "target": "f"},
    {"word": "cama", "target": "m"},
    {"word": "plato", "target": "l"},
    {"word": "vaso", "target": "s"},
    {"word": "cuchara", "target": "h"},
    {"word": "juguete", "target": "j"},
    {"word": "muñeca", "target": "ñ"},

    # --- Naturaleza y Colores (14) ---
    {"word": "luna", "target": "n"},
    {"word": "cielo", "target": "c"},
    {"word": "lluvia", "target": "v"},
    {"word": "nieve", "target": "i"},
    {"word": "fuego", "target": "f"},
    {"word": "tierra", "target": "r"},
    {"word": "rojo", "target": "j"},
    {"word": "azul", "target": "z"},
    {"word": "verde", "target": "v"},
    {"word": "amarillo", "target": "ll"},
    {"word": "blanco", "target": "b"},
    {"word": "negro", "target": "g"},
    {"word": "pelota", "target": "p"},
    {"word": "tren", "target": "t"},
    
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
        score += 1
        level_idx += 1
        return level_idx, score, True, '¡Correcto!'
    else:
        return level_idx, score, False, 'No es correcto. Intenta de nuevo.'

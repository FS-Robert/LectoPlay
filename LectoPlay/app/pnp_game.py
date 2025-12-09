# pnp_game.py
import random

PARES = [
    ("gato", "tago"),
    ("casa", "saca"),
    ("perro", "preor"),
    ("mesa", "sema"),
    ("sol", "los"),
    ("libro", "ilbor"),
    ("escuela", "esceula"),
    ("flor", "folr"),
    ("nube", "bune"),
    ("camino", "cmaino"),
]


def total_levels():
    return len(PARES)


def get_level(idx):
    real, fake = PARES[idx]
    return {"real": real, "fake": fake}

#Mezcla las opciones para que no siempre estén en el mismo orden
def make_options(real, fake):
    opciones = [real, fake]
    random.shuffle(opciones)
    return opciones

#verifica si la elección del niño es correcta
def check_choice(choice, idx, score):
    """Revisa qué opción eligió el niño."""
    real, fake = PARES[idx]
    eleccion = (choice or "").strip().lower()

    if eleccion == real.lower():
        score += 1
        msg = "¡Correcto! Esa es la palabra real. 🎉"
        correct = True
    else:
        msg = f"No es correcto. La palabra real era «{real}»."
        correct = False

    idx += 1
    finished = idx >= len(PARES)

    return idx, score, correct, msg, finished

# desc_game.py

DESCS = [
    {"texto": "Animal que dice miau.", "respuesta": "gato"},
    {"texto": "Fruta amarilla y curva.", "respuesta": "banana"},
    {"texto": "Lugar donde estudias todos los días.", "respuesta": "escuela"},
    {"texto": "Objeto que usas para escribir en papel.", "respuesta": "lapiz"},
    {"texto": "Vehículo que lleva a muchos niños a la escuela.", "respuesta": "bus"},
    {"texto": "Animal grande que tiene trompa.", "respuesta": "elefante"},
    {"texto": "Bebida blanca que viene de la vaca.", "respuesta": "leche"},
    {"texto": "Persona que enseña en el aula.", "respuesta": "maestra"},
    {"texto": "Comida redonda con salsa y queso.", "respuesta": "pizza"},
    {"texto": "Estrella que vemos de día en el cielo.", "respuesta": "sol"},
]


def total_levels():
    return len(DESCS)


def get_level(idx):
    return DESCS[idx]

#compara la respuesta escrita con la palabra correcta y dira si es correcta o no.
def check_answer(answer, idx, score):
    
    ans = (answer or "").strip().lower()
    correcta = DESCS[idx]["respuesta"].lower()

    if ans == correcta:
        score += 1
        msg = "¡Correcto! 🎉"
        correct = True
    else:
        msg = f"No es correcto. La respuesta era: «{correcta}»."
        correct = False

    idx += 1
    finished = idx >= len(DESCS)

    return idx, score, correct, msg, finished

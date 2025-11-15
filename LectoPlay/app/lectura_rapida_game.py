# juegos/lectura_rapida_game.py
import random

CATEGORIAS = {
    "Animales": [
        {
            "frase": "Ana tiene un gato gris que duerme todo el día.",
            "pregunta": "¿De qué color es el gato?",
            "opciones": ["Gris", "Blanco", "Negro"],
            "correcta": "Gris",
        },
        {
            "frase": "El perro de Marta ladra cuando escucha la puerta.",
            "pregunta": "¿Cuándo ladra el perro?",
            "opciones": ["Cuando come", "Cuando escucha la puerta", "Cuando duerme"],
            "correcta": "Cuando escucha la puerta",
        },
    ],
    "Escuela": [
        {
            "frase": "Carla va a la escuela caminando todas las mañanas.",
            "pregunta": "¿Cómo va Carla a la escuela?",
            "opciones": ["En autobús", "En carro", "Caminando"],
            "correcta": "Caminando",
        },
        {
            "frase": "En el recreo, los niños juegan en el patio de la escuela.",
            "pregunta": "¿Dónde juegan los niños?",
            "opciones": ["En el aula", "En el patio", "En la calle"],
            "correcta": "En el patio",
        },
    ],
    "Rutinas": [
        {
            "frase": "Luis toma un vaso de jugo de naranja en el desayuno.",
            "pregunta": "¿Qué toma Luis?",
            "opciones": ["Leche", "Jugo de naranja", "Agua"],
            "correcta": "Jugo de naranja",
        },
        {
            "frase": "Pedro lee un libro de aventuras antes de dormir.",
            "pregunta": "¿Qué tipo de libro lee Pedro?",
            "opciones": ["De aventuras", "De cocina", "De ciencias"],
            "correcta": "De aventuras",
        },
    ],
}


def get_categorias():
    """Devuelve los nombres de las categorías disponibles."""
    return list(CATEGORIAS.keys())


def get_random_question(categoria):
    """Devuelve una pregunta aleatoria de la categoría indicada."""
    preguntas = CATEGORIAS.get(categoria, [])
    if not preguntas:
        return None, None, [], None
    q = random.choice(preguntas)
    return q["frase"], q["pregunta"], q["opciones"], q["correcta"]

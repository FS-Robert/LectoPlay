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
        {
            "frase": "Un pez naranja nada tranquilo en una pecera pequeña.",
            "pregunta": "¿Dónde está el pez?",
            "opciones": ["En un lago", "En una pecera", "En el mar"],
            "correcta": "En una pecera",
        },
        {
            "frase": "El conejo blanco salta rápido por el jardín.",
            "pregunta": "¿Qué hace el conejo?",
            "opciones": ["Duerme", "Salta", "Come"],
            "correcta": "Salta",
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
        {
            "frase": "La maestra escribe una suma en la pizarra verde.",
            "pregunta": "¿Qué escribe la maestra?",
            "opciones": ["Un cuento", "Una suma", "Un dibujo"],
            "correcta": "Una suma",
        },
        {
            "frase": "Tomás guarda sus cuadernos en una mochila azul.",
            "pregunta": "¿De qué color es la mochila?",
            "opciones": ["Roja", "Azul", "Verde"],
            "correcta": "Azul",
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
        {
            "frase": "Sofía se lava los dientes después de cada comida.",
            "pregunta": "¿Qué hace Sofía después de comer?",
            "opciones": ["Duerme", "Se lava los dientes", "Ve televisión"],
            "correcta": "Se lava los dientes",
        },
        {
            "frase": "Cada tarde, Diego saca a pasear a su perro.",
            "pregunta": "¿Cuándo saca Diego a su perro?",
            "opciones": ["En la mañana", "En la tarde", "En la noche"],
            "correcta": "En la tarde",
        },
    ],

    "Comida": [
        {
            "frase": "En el almuerzo, María come arroz con pollo y ensalada.",
            "pregunta": "¿Qué come María junto con el pollo?",
            "opciones": ["Pan", "Arroz", "Sopa"],
            "correcta": "Arroz",
        },
        {
            "frase": "A Pablo le gusta el helado de chocolate los domingos.",
            "pregunta": "¿De qué sabor es el helado?",
            "opciones": ["Vainilla", "Fresa", "Chocolate"],
            "correcta": "Chocolate",
        },
        {
            "frase": "La fruta favorita de Carla es la manzana roja.",
            "pregunta": "¿Cuál es la fruta favorita de Carla?",
            "opciones": ["Pera", "Manzana", "Uva"],
            "correcta": "Manzana",
        },
        {
            "frase": "En la mesa hay tres vasos de agua y un vaso de jugo.",
            "pregunta": "¿Cuántos vasos de agua hay?",
            "opciones": ["Dos", "Tres", "Cuatro"],
            "correcta": "Tres",
        },
    ],

    "Deportes": [
        {
            "frase": "Lucas juega fútbol en el parque con sus amigos.",
            "pregunta": "¿Qué deporte juega Lucas?",
            "opciones": ["Básquetbol", "Fútbol", "Tenis"],
            "correcta": "Fútbol",
        },
        {
            "frase": "Marta nada en la piscina cada sábado por la mañana.",
            "pregunta": "¿Dónde nada Marta?",
            "opciones": ["En el mar", "En un río", "En la piscina"],
            "correcta": "En la piscina",
        },
        {
            "frase": "Andrea monta en bicicleta por la calle de su barrio.",
            "pregunta": "¿Qué usa Andrea para pasear?",
            "opciones": ["Patines", "Bicicleta", "Moto"],
            "correcta": "Bicicleta",
        },
        {
            "frase": "El entrenador les pide a los niños que corran dos vueltas.",
            "pregunta": "¿Cuántas vueltas deben correr?",
            "opciones": ["Una", "Dos", "Tres"],
            "correcta": "Dos",
        },
    ],

    "Familia": [
        {
            "frase": "Julia visita a su abuela todos los domingos por la tarde.",
            "pregunta": "¿A quién visita Julia?",
            "opciones": ["A su tía", "A su abuela", "A su hermana"],
            "correcta": "A su abuela",
        },
        {
            "frase": "En la sala, la familia ve una película sentada en el sofá.",
            "pregunta": "¿Qué hace la familia en la sala?",
            "opciones": ["Lee libros", "Ve una película", "Cena"],
            "correcta": "Ve una película",
        },
        {
            "frase": "El hermano mayor ayuda a su hermana con la tarea de matemáticas.",
            "pregunta": "¿Con qué ayuda el hermano a su hermana?",
            "opciones": ["Con la tarea de ciencias", "Con la tarea de matemáticas", "Con la tarea de arte"],
            "correcta": "Con la tarea de matemáticas",
        },
        {
            "frase": "La familia cena junta en la mesa a las siete de la noche.",
            "pregunta": "¿A qué hora cena la familia?",
            "opciones": ["A las cinco", "A las siete", "A las nueve"],
            "correcta": "A las siete",
        },
    ],

    "Naturaleza": [
        {
            "frase": "En el parque hay muchos árboles verdes y flores de colores.",
            "pregunta": "¿Qué hay en el parque?",
            "opciones": ["Autos y casas", "Árboles y flores", "Tiendas y semáforos"],
            "correcta": "Árboles y flores",
        },
        {
            "frase": "El sol brilla fuerte en el cielo azul.",
            "pregunta": "¿De qué color es el cielo?",
            "opciones": ["Rojo", "Azul", "Gris"],
            "correcta": "Azul",
        },
        {
            "frase": "En la noche se pueden ver muchas estrellas pequeñas.",
            "pregunta": "¿Cuándo se ven las estrellas?",
            "opciones": ["En la mañana", "En la tarde", "En la noche"],
            "correcta": "En la noche",
        },
        {
            "frase": "La lluvia cae suave y moja las calles de la ciudad.",
            "pregunta": "¿Qué cae y moja las calles?",
            "opciones": ["Nieve", "Lluvia", "Arena"],
            "correcta": "Lluvia",
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

from django.shortcuts import render, redirect
from django.http import HttpResponse
import random


def home_view(request):
    return render(request, "home.html")


def about_view(request):
    return render(request, 'about.html')


def ejercicios(request):
    # Página de ejercicios: enlaces a los distintos juegos
    return render(request, 'ejercicios.html')


def contacts(request):
    return render(request, 'contacts.html')


# Juego "Encuentra la letra" implementado en el servidor (sin JS)
def encuentra(request):
    # Definir los niveles (palabra y letra objetivo)
    levels = [
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

    total = len(levels)

    # Manejar reinicio solicitado
    if request.method == 'POST' and request.POST.get('reset'):
        request.session.pop('enc_level', None)
        request.session.pop('enc_score', None)
        return redirect('encuentra')

    # Inicializar sesión si es necesario
    if 'enc_level' not in request.session:
        request.session['enc_level'] = 0
        request.session['enc_score'] = 0

    level_idx = request.session.get('enc_level', 0)
    score = request.session.get('enc_score', 0)
    message = None

    # Manejar intento del usuario
    if request.method == 'POST' and request.POST.get('choice'):
        choice = request.POST.get('choice')
        # asegurar que nivel actual no excede
        if level_idx < total:
            correct = levels[level_idx]['target']
            if choice == correct:
                # acierto
                score += 10
                request.session['enc_score'] = score
                level_idx += 1
                request.session['enc_level'] = level_idx
                # si ya no quedan niveles, mostramos resultados más abajo
            else:
                message = 'No es correcto. Intenta de nuevo.'

    # Si terminó el juego
    if level_idx >= total:
        context = {
            'finished': True,
            'score': score,
            'total': total,
        }
        return render(request, 'encuentra_letra.html', context)

    # Preparar opciones para el nivel actual (servidor crea distractores)
    lvl = levels[level_idx]
    word = lvl['word']
    target = lvl['target']

    # letras únicas de la palabra
    uniq = list(dict.fromkeys(list(word)))
    letters = set(l.lower() for l in uniq if l.strip())
    letters.add(target.lower())

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    while len(letters) < 6:
        letters.add(random.choice(alphabet))

    choices = list(letters)
    random.shuffle(choices)

    # construir palabra con espacios para mostrar
    spaced_word = ' '.join(list(word))

    context = {
        'level_num': level_idx + 1,
        'total': total,
        'score': score,
        'word': word,
        'spaced_word': spaced_word,
        'target': target,
        'choices': choices,
        'message': message,
    }

    return render(request, 'encuentra_letra.html', context)
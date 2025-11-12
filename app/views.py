from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
from . import encuentra_game


def home_view(request):
    return render(request, "home.html")


def about_view(request):
    return render(request, 'about.html')


def ejercicios(request):
    # Página de ejercicios: enlaces a los distintos juegos
    return render(request, 'ejercicios.html')


def contacts(request):
    return render(request, 'contacts.html')


# JUEGO: ENCUENTRA LA LETRA 
def encuentra(request):
    total = encuentra_game.total_levels()

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
        level_idx, score, correct, msg = encuentra_game.check_choice(choice, level_idx, score)
        request.session['enc_level'] = level_idx
        request.session['enc_score'] = score
        if not correct:
            message = msg

    # Si terminó el juego
    if level_idx >= total:
        context = {
            'finished': True,
            'score': score,
            'total': total,
        }
        return render(request, 'encuentra_letra.html', context)

    # Preparar datos para el nivel actual
    lvl = encuentra_game.get_level(level_idx)
    word = lvl['word']
    target = lvl['target']
    choices = encuentra_game.make_choices(word, target, count=6, rng=random)
    spaced_word = encuentra_game.spaced_word(word)

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


## FIN DE ENCUENTRA LA LETRA 
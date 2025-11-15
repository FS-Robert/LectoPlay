from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
from . import encuentra_game
from firebase_admin import auth
from django.shortcuts import render
from .lectura_rapida_game import get_categorias, get_random_question

def home_view(request):
    return render(request, "home.html")


def about_view(request):
    return render(request, 'about.html')


def ejercicios(request):
    return render(request, 'ejercicios.html')




def contacts(request):
    return render(request, 'contacts.html')


def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.create_user(
            email=email,
            password=password,
            display_name=name
        )
        return redirect('login')
    return render(request, 'register.html')



def login_view(request):
    return render(request, 'login.html')



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



# JUEGO: LECTURA RÁPIDA

def lectura_rapida_game(request):
    categorias = get_categorias()
    categoria = request.GET.get("categoria") or request.POST.get("categoria")
    action = request.POST.get("action")  # "responder" o "otra"

    # Inicializar marcador en sesión
    if "aciertos" not in request.session:
        request.session["aciertos"] = 0
        request.session["intentos"] = 0

    aciertos = request.session["aciertos"]
    intentos = request.session["intentos"]

    frase = pregunta = correcta = feedback = None
    opciones = []

    if request.method == "POST" and categoria:
        if action == "responder":
            respuesta_usuario = request.POST.get("respuesta")
            correcta_anterior = request.POST.get("correcta")

            intentos += 1
            if respuesta_usuario == correcta_anterior:
                aciertos += 1
                feedback = "¡Correcto! 🎉"
            else:
                feedback = f"No es correcto. La respuesta era: {correcta_anterior}."

            # Guardar marcador en sesión
            request.session["aciertos"] = aciertos
            request.session["intentos"] = intentos

        # En ambos casos cargamos una nueva pregunta
        frase, pregunta, opciones, correcta = get_random_question(categoria)

    elif categoria:
        # Primera vez que entra a la categoría
        frase, pregunta, opciones, correcta = get_random_question(categoria)

    context = {
        "categorias": categorias,
        "categoria_actual": categoria,
        "frase": frase,
        "pregunta": pregunta,
        "opciones": opciones,
        "correcta": correcta,
        "feedback": feedback,
        "aciertos": aciertos,
        "intentos": intentos,
    }
    return render(request, "lectura_rapida_game.html", context)
# FIN DE LECTURA RÁPIDA

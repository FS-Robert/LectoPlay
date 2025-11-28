from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
from .desc_game import get_level, total_levels, check_answer
from httpx import request
from matplotlib.style import context
from . import encuentra_game
from . import palabras_colores_game 
from django.shortcuts import render
from .lectura_rapida_game import get_categorias, get_random_question
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import chatbot as ai_service
from . import desc_game
from . import pnp_game
from .models import Contacto, Ticket, Message
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required  # Para seguridad
from django.contrib.auth.models import User  # Importar modelo de Usuarios de Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# ==========================================
#  PANEL DE ADMINISTRADOR (DASHBOARD)
# ==========================================

@staff_member_required(login_url='/login/')  # Si no es admin, lo manda al login
def admin_dashboard(request):
    # 1. Contar datos reales
    total_usuarios = User.objects.count()
    # Usamos Tickets como unidad de consulta (cada ticket representa una conversación)
    total_consultas = Ticket.objects.count()

    # Contar consultas sin responder: aquellas cuyo último mensaje fue enviado por el usuario
    consultas_sin_responder = 0
    for ticket in Ticket.objects.all():
        last_msg = ticket.mensajes.order_by('-creado').first()
        if last_msg and last_msg.autor == 'usuario':
            consultas_sin_responder += 1

    stats = {
        'total_usuarios': total_usuarios,
        'total_consultas': total_consultas,
        'consultas_sin_responder': consultas_sin_responder
    }

    return render(request, 'admin/admin_dashboard.html', {'stats': stats})


# --- Vistas de gestión de usuarios ---

@staff_member_required(login_url='/login/')
def admin_usuarios(request):
    usuarios = User.objects.all().order_by("username")
    context = {
        "usuarios": usuarios
    }
    return render(request, "admin/admin_usuarios.html", context)


@staff_member_required(login_url='/login/')
def admin_usuario_nuevo(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        #  Fuerza siempre a usuario normal
        user.is_staff = False
        user.is_superuser = False
        user.save()

        return redirect("admin_usuarios")

    return render(request, "admin/admin_usuario_form.html", {"modo": "crear"})


@staff_member_required(login_url='/login/')
def admin_usuario_editar(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        usuario.username = request.POST.get("username")
        usuario.email = request.POST.get("email")
        usuario.is_staff = bool(request.POST.get("is_staff"))
        usuario.is_superuser = bool(request.POST.get("is_superuser"))

        # Si se escribe una nueva contraseña, la cambiamos
        password = request.POST.get("password")
        if password:
            usuario.set_password(password)

        usuario.save()
        return redirect("admin_usuarios")

    context = {
        "modo": "editar",
        "usuario": usuario,
    }
    return render(request, "admin/admin_usuario_form.html", context)


@staff_member_required(login_url='/login/')
def admin_usuario_eliminar(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        usuario.delete()
        return redirect("admin_usuarios")

    # Pequeña pantalla de confirmación
    return render(request, "admin/admin_usuario_eliminar.html", {"usuario": usuario})


# --- FIN de vistas de gestión de usuarios ---


@staff_member_required(login_url='/login/')
def admin_consultas(request):
    # Preparamos una lista con metadata para facilitar el template
    tickets_qs = Ticket.objects.order_by('-creado')
    tickets = []
    for t in tickets_qs:
        last = t.mensajes.order_by('-creado').first()
        unread = True if last and last.autor == 'usuario' else False
        tickets.append({
            'ticket': t,
            'last': last,
            'unread': unread,
        })

    unread_count = sum(1 for x in tickets if x['unread'])

    return render(request, "admin/admin_consultas.html", {
        "tickets": tickets,
        "unread_count": unread_count,
    })


@csrf_exempt
@require_POST
def chatbot_ask(request):
    """
    Maneja las solicitudes POST del widget del chatbot.
    Delega la llamada a la API de Gemini al archivo ai_service.py.
    """
    try:
        # 1. Parsear el mensaje JSON entrante
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'El mensaje no puede estar vacío.'}, status=400)

        # 2. Obtener la API KEY de forma segura desde settings
        api_key = settings.GEMINI_API_KEY

        if not api_key:
            return JsonResponse({'error': 'Configuración del servidor incompleta (API Key).'}, status=500)

        # 3. Delegar la llamada de la IA a la capa de servicio
        ai_response = ai_service.get_ai_response(user_message, api_key)
        
        # 4. Retornar la respuesta de la IA al frontend
        return JsonResponse({'response': ai_response})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Formato de solicitud JSON inválido.'}, status=400)
    except ConnectionError:
        return JsonResponse({'error': 'Error de conexión con el servicio de IA.'}, status=500)
    except Exception as e:
        print(f"Internal Server Error in views.py: {e}")
        return JsonResponse({'error': 'Error interno del servidor.'}, status=500)



def inicio_view(request):
    return render(request, "inicio.html")


def about_view(request):
    return render(request, 'about.html')


def ejercicios(request):
    return render(request, 'ejercicios.html')


def contacts(request):
    return render(request, 'contacts.html')


def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')      # nombre del niño / usuario
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validaciones sencillas
        if not name or not email or not password:
            messages.error(request, "Por favor, completa todos los campos.")
            return render(request, 'register.html')

        # Evitar correos repetidos
        if User.objects.filter(email=email).exists():
            messages.error(request, "Ya existe un usuario con ese correo.")
            return render(request, 'register.html')

        # Usaremos el email como username
        username = email

        # Crear usuario en la base de datos SQLite
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name
        )

        messages.success(request, "Tu cuenta fue creada con éxito. Ahora inicia sesión.")
        return redirect('login')

    return render(request, 'register.html')



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Completa todos los campos.")
            return render(request, 'login.html')

        # Buscar usuario por email
        try:
            usuario = User.objects.get(email=email)
            username = usuario.username
        except User.DoesNotExist:
            username = None

        user = authenticate(request, username=username, password=password) if username else None

        if user is not None:
            login(request, user)
            return redirect('home')   # o la ruta que quieras después del login
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
            return render(request, 'login.html')

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


# =========================
#   JUEGO: ENCUENTRA LETRA
# =========================

def encuentra(request):
    total = encuentra_game.total_levels()

    if request.method == 'POST' and request.POST.get('reset'):
        request.session.pop('enc_level', None)
        request.session.pop('enc_score', None)
        return redirect('encuentra')

    if 'enc_level' not in request.session:
        request.session['enc_level'] = 0
        request.session['enc_score'] = 0

    level_idx = request.session['enc_level']
    score = request.session['enc_score']
    message = None

    if request.method == 'POST' and request.POST.get('choice'):
        choice = request.POST.get('choice')
        level_idx, score, correct, msg = encuentra_game.check_choice(choice, level_idx, score)
        request.session['enc_level'] = level_idx
        request.session['enc_score'] = score
        if not correct:
            message = msg

    if level_idx >= total:
        return render(request, 'encuentra_letra.html', {
            'finished': True,
            'score': score,
            'total': total,
        })

    lvl = encuentra_game.get_level(level_idx)

    context = {
        'level_num': level_idx + 1,
        'total': total,
        'score': score,
        'word': lvl['word'],
        'spaced_word': encuentra_game.spaced_word(lvl['word']),
        'target': lvl['target'],
        'choices': encuentra_game.make_choices(lvl['word'], lvl['target'], count=6, rng=random),
        'message': message,
    }

    return render(request, 'encuentra_letra.html', context)


# FIN DE ENCUENTRA LA LETRA 


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
# ====================================
#   JUEGO: PALABRAS Y COLORES
# ====================================

def palabras_colores(request):
    total = palabras_colores_game.total_levels()

    # Reinicio
    if request.method == 'POST' and request.POST.get('reset'):
        request.session.pop('pc_level', None)
        request.session.pop('pc_score', None)
        return redirect('palabras_colores')

    # Inicialización
    if 'pc_level' not in request.session:
        request.session['pc_level'] = 0
        request.session['pc_score'] = 0

    level_idx = request.session['pc_level']
    score = request.session['pc_score']
    message = None

    # Lógica del intento
    if request.method == 'POST' and request.POST.get('choice'):
        choice = request.POST.get('choice')
        # Se desempaquetan solo los primeros 4 valores para evitar errores
        result = palabras_colores_game.check_choice(choice, level_idx, score)
        level_idx, score, correct, msg = result[:4]

        request.session['pc_level'] = level_idx
        request.session['pc_score'] = score
        message = msg

    # Juego terminado
    if level_idx >= total:
        return render(request, "palabras_colores.html", {
            "finished": True,
            "score": score,
            "total": total,
        })

    # Cargar nivel
    lvl = palabras_colores_game.get_level(level_idx)
    word = lvl["word"]
    correct_color = lvl["color"]
    choices = palabras_colores_game.make_choices(correct_color)

    context = {
        "word": word,
        "choices": choices,
        "level_num": level_idx + 1,
        "total": total,
        "score": score,
        "message": message,
    }

    return render(request, "palabras_colores.html", context)



# FIN DE PALABRAS Y COLORES


# descripción de la palabra
def desc_palabra(request):
    total = desc_game.total_levels()

    # Reiniciar juego
    if request.method == "POST" and request.POST.get("reset"):
        request.session.pop("desc_level", None)
        request.session.pop("desc_score", None)
        return redirect("desc_palabra")

    # Iniciar sesión de juego si no existe
    if "desc_level" not in request.session:
        request.session["desc_level"] = 0
        request.session["desc_score"] = 0

    level_idx = request.session["desc_level"]
    score = request.session["desc_score"]
    message = None
    finished = level_idx >= total

    # Procesar respuesta
    if request.method == "POST" and request.POST.get("respuesta") and not finished:
        respuesta = request.POST.get("respuesta")
        level_idx, score, correct, msg, finished = desc_game.check_answer(
            respuesta, level_idx, score
        )
        request.session["desc_level"] = level_idx
        request.session["desc_score"] = score
        message = msg

    finished = level_idx >= total

    descripcion = None
    if not finished:
        level = desc_game.get_level(level_idx)
        descripcion = level["texto"]

    context = {
        "finished": finished,
        "total": total,
        "level_num": level_idx + 1 if not finished else total,
        "score": score,
        "descripcion": descripcion,
        "message": message,
    }
    return render(request, "desc_palabra.html", context)

# ---------------------- TTS -----------------------

def toggle_tts_pc(request):
    tts_enabled = request.session.get("tts_enabled", False)
    request.session["tts_enabled"] = not tts_enabled
    return JsonResponse({"tts_enabled": request.session["tts_enabled"]})


# FIN DE DESCRIPCIÓN DE LA PALABRA

# ==============================
#   JUEGO: PALABRA O NO PALABRA
# ==============================

def pnp(request):
    total = pnp_game.total_levels()

    # Reiniciar juego
    if request.method == "POST" and request.POST.get("reset"):
        request.session.pop("pnp_level", None)
        request.session.pop("pnp_score", None)
        return redirect("pnp")

    # Inicializar sesión si no existe
    if "pnp_level" not in request.session:
        request.session["pnp_level"] = 0
        request.session["pnp_score"] = 0

    level_idx = request.session["pnp_level"]
    score = request.session["pnp_score"]
    message = None
    finished = level_idx >= total

    opciones = []

    # Cargar nivel actual
    if not finished:
        lvl = pnp_game.get_level(level_idx)
        opciones = pnp_game.make_options(lvl["real"], lvl["fake"])

    # Procesar elección
    if request.method == "POST" and request.POST.get("choice") and not finished:
        choice = request.POST.get("choice")
        level_idx, score, correct, msg, finished = pnp_game.check_choice(
            choice, level_idx, score
        )
        request.session["pnp_level"] = level_idx
        request.session["pnp_score"] = score
        message = msg

        if not finished:
            lvl = pnp_game.get_level(level_idx)
            opciones = pnp_game.make_options(lvl["real"], lvl["fake"])

    finished = level_idx >= total

    context = {
        "finished": finished,
        "total": total,
        "level_num": level_idx + 1 if not finished else total,
        "score": score,
        "opciones": opciones,
        "message": message,
    }
    return render(request, "pnp.html", context)


# FIN DE PALABRA O NO PALABRA


# Función del formulario contactos
def contacto_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('name')
        email = request.POST.get('email')
        mensaje = request.POST.get('message')
        fecha = request.POST.get('fecha')

        contacto = Contacto.objects.create(
            nombre=nombre,
            correo=email,
            mensaje=mensaje,
            fecha_envio=fecha
        )

        ticket = Ticket.objects.create(
            contacto=contacto,
            estado='pendiente'
        )

        Message.objects.create(
            ticket=ticket,
            autor='usuario',
            contenido=mensaje
        )

        return render(request, 'contacto.html', {
            'success': True,
            'ticket_codigo': ticket.codigo_acceso
        })

    return render(request, 'contacto.html')


@staff_member_required(login_url='/login/')
def consulta_detalle(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    mensajes = ticket.mensajes.order_by("creado")

    if request.method == "POST":
        contenido = request.POST.get("respuesta")
        Message.objects.create(
            ticket=ticket,
            autor="admin",
            contenido=contenido
        )
        ticket.estado = "respondido"
        ticket.save()

        return redirect("consulta_detalle", ticket_id=ticket.id)

    return render(request, "admin/consulta_detalle.html", {
        "ticket": ticket,
        "mensajes": mensajes
    })


def usuario_ver_ticket(request, codigo):
    ticket = get_object_or_404(Ticket, codigo_acceso=codigo)
    mensajes = ticket.mensajes.order_by("creado")

    if request.method == "POST":
        contenido = request.POST.get("mensaje")
        if contenido.strip():
            Message.objects.create(
                ticket=ticket,
                autor="usuario",
                contenido=contenido
            )
        return redirect("usuario_ver_ticket", codigo=codigo)

    return render(request, "usuario_ticket.html", {
        "ticket": ticket,
        "mensajes": mensajes
    })



def finalizar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.estado = "finalizado"
    ticket.save()
    return redirect("consulta_detalle", ticket_id=ticket_id)


def cambiar_estado(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    nuevo = request.GET.get("estado")
    if nuevo:
        ticket.estado = nuevo
        ticket.save()
    return redirect("admin_consultas")


def escribe_palabra_game(request):
    idx = request.session.get("level_idx", 0)     # Nivel actual
    score = request.session.get("score", 0)
    narracion_activada = request.session.get("narracion_activada", False)   # Estado de voz (True/False)

    total = total_levels()

    if request.method == "POST":
        #  ACTIVAR / DESACTIVAR NARRACIÓN
        if request.POST.get("toggle_narracion"):
            narracion_activada = not narracion_activada
            request.session["narracion_activada"] = narracion_activada

        # REINICIAR JUEGO
        if request.POST.get("reset") == "1":
            request.session["level_idx"] = 0
            request.session["score"] = 0
            request.session["narracion_activada"] = False
            return redirect("escribe_palabra_game")  # 👈 NOMBRE DE TU URL

        #  REVISAR RESPUESTA
        if request.POST.get("respuesta"):
            respuesta = request.POST.get("respuesta", "")
            idx, score, correct, msg, finished = check_answer(respuesta, idx, score)
            request.session["level_idx"] = idx
            request.session["score"] = score

            if finished:
                return render(request, "escribe_palabra.html", {
                    "finished": True,
                    "score": score,
                    "total": total,
                })

            #  ENVIAR MENSAJE DE CORRECCIÓN
            nivel_data = get_level(idx)
            return render(request, "escribe_palabra.html", {
                "descripcion": nivel_data["texto"],
                "message": msg,
                "level_num": idx + 1,
                "score": score,
                "total": total,
                "correcta": nivel_data["respuesta"],
                "narracion_activada": narracion_activada,
            })

    #  CARGAR NIVEL INICIAL
    nivel_data = get_level(idx)
    return render(request, "escribe_palabra.html", {
        "descripcion": nivel_data["texto"],
        "level_num": idx + 1,
        "score": score,
        "total": total,
        "narracion_activada": narracion_activada,
    })
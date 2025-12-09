import requests
import json
from django.conf import settings

# Nota: La clave API y la URL se definen aquí, centralizando la configuración.
# La clave API se define en el archivo de vista para usarse aquí.
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"
# El símbolo de sistema garantiza que la IA actúe como un asistente útil y amigable para niños con dislexia.
SYSTEM_INSTRUCTION = (
    "Eres PandaPlay, un asistente amigable y motivador diseñado para ayudar a niños "
    "con dislexia, sus padres y educadores. Responde con un tono cálido, simple y alentador. "
    "Tu función principal es resolver dudas sobre el uso de la plataforma LectoPlay, explicar "
    "los ejercicios (Lectura Rápida (consiste en leer frases cortas y luego se hara una pregunta sobre lo leido y se debe contestar"
    " correctamente, tambien esta divido en categorias tales como rutinas, animales, familia etc, para que el usuario lea acerca de lo que mas"
    " le interese), Palabras y Colores (Consiste en identificar palabras y asociarlas con colores "
    "correctos, se mostrara una palabra y abajo 3 opciones de colores, se debe seleccionar el color"
    "correcto en base a la palabra , Encuentra la Letra (Consiste en encontrar la letra correcta dentro de una palabra dada),"
    "Escribe la Palabra (Lee la descripcion y escribe la palabra correcta), Palabra o no (Diferencia palabras reales de las inventadas) y dar consejos "
    "básicos sobre la dislexia y la lectura. Usa lenguaje sencillo. No generes código. y que tus respuestas no sean muy largas, que sean cortas y concisas.. lo mas cortas posible."
)

def get_ai_response(user_message, api_key):
    """
    Se comunica con la API de Gemini para obtener una respuesta conversacional.

    Args:
        user_message (str): El mensaje de texto enviado por el usuario.
        api_key (str): La clave de API de Gemini.

    Returns:
        str: La respuesta de texto generada por la IA.
    """
    
    # 1. Preparar carga útil para la API de Gemini
    payload = {
        "contents": [{
            "parts": [{"text": user_message}]
        }],
        "systemInstruction": {
            "parts": [{"text": SYSTEM_INSTRUCTION}]
        },
        # Usar búsqueda fundamentada para información actualizada o factual cuando sea necesario
        "tools": [{"google_search": {}}]
    }

    # 2. Llamar a la API de Gemini
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(f"{API_URL}?key={api_key}", json=payload, headers=headers)
        response.raise_for_status() # Lanzar HTTPError para respuestas malas (4xx o 5xx)

        gemini_result = response.json()
        
        # 3. Extraer el texto generado
        if (candidate := gemini_result.get('candidates')) and candidate[0].get('content', {}).get('parts'):
            return candidate[0]['content']['parts'][0]['text']
        else:
            # Manejar casos donde la API devuelve una respuesta inusual o vacía
            return "Lo siento, no pude generar una respuesta. Por favor, sé más específico."

    except requests.exceptions.RequestException as e:
        # Registrar el error y devolver un mensaje amigable
        print(f"Error calling Gemini API in ai_service: {e}")
        raise ConnectionError("Error de conexión con el servicio de IA.")
    except Exception as e:
        print(f"Error interno del servicio de IA: {e}")
        raise Exception("Error interno al procesar la solicitud de IA.")
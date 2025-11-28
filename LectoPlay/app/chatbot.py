import requests
import json
from django.conf import settings

# Nota: The API key and URL are defined here, centralizing the configuration.
# The API key is defined in the view file to be used here.
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"
# The system prompt ensures the AI acts as a helpful, friendly assistant for children with dyslexia.
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
    Communicates with the Gemini API to get a conversational response.

    Args:
        user_message (str): The text message sent by the user.
        api_key (str): The Gemini API key.

    Returns:
        str: The AI's generated text response.
    """
    
    # 1. Prepare payload for Gemini API
    payload = {
        "contents": [{
            "parts": [{"text": user_message}]
        }],
        "systemInstruction": {
            "parts": [{"text": SYSTEM_INSTRUCTION}]
        },
        # Use search grounding for up-to-date or factual information when needed
        "tools": [{"google_search": {}}]
    }

    # 2. Call the Gemini API
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(f"{API_URL}?key={api_key}", json=payload, headers=headers)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        gemini_result = response.json()
        
        # 3. Extract the generated text
        if (candidate := gemini_result.get('candidates')) and candidate[0].get('content', {}).get('parts'):
            return candidate[0]['content']['parts'][0]['text']
        else:
            # Handle cases where the API returns an unusual or empty response
            return "Lo siento, no pude generar una respuesta. Por favor, sé más específico."

    except requests.exceptions.RequestException as e:
        # Log the error and return a friendly message
        print(f"Error calling Gemini API in ai_service: {e}")
        raise ConnectionError("Error de conexión con el servicio de IA.")
    except Exception as e:
        print(f"Internal AI Service Error: {e}")
        raise Exception("Error interno al procesar la solicitud de IA.")
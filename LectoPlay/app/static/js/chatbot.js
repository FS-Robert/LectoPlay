document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('chatbot-toggle');
    const closeBtn = document.getElementById('close-chat-btn');
    const chatWindow = document.getElementById('chatbot-window');
    const chatForm = document.getElementById('chat-input-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendBtn = document.getElementById('chat-send-btn');
    

    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    const CSRF_TOKEN = csrfInput ? csrfInput.value : '';

    if (!CSRF_TOKEN) {
        console.error("No se encontró el token CSRF. Asegúrate de tener {% csrf_token %} en tu HTML.");
    }
    // -----------------------

    let isChatOpen = false;
    let isLoading = false;

    const API_ENDPOINT = '/api/chatbot_ask'; 
    
    // --- UI Handlers ---

    function openChat() {
        isChatOpen = true;
        chatWindow.classList.remove('hidden');
        chatInput.focus();
        scrollToBottom();
    }

    function closeChat() {
        isChatOpen = false;
        chatWindow.classList.add('hidden');
        // devolver el foco al botón flotante por accesibilidad
        if (toggleBtn) toggleBtn.focus();
    }

    function toggleChat() {
        if (isChatOpen) {
            closeChat();
        } else {
            openChat();
        }
    }

    // Asegurarse de que el botón existe
    if (toggleBtn) {
        toggleBtn.addEventListener('click', toggleChat);
        // permitir abrir con teclado
        toggleBtn.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleChat();
            }
        });
    }

    // Botón para cerrar el chat
    if (closeBtn) {
        closeBtn.addEventListener('click', (e) => {
            e.preventDefault();
            closeChat();
        });
        // permitir cerrar con teclado
        closeBtn.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                closeChat();
            }
        });
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addMessage(text, sender) {
        const bubble = document.createElement('div');
        bubble.classList.add('message-bubble', sender === 'user' ? 'user-message' : 'bot-message');

        const formattedText = String(text).replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        bubble.innerHTML = formattedText;
        chatMessages.appendChild(bubble);
        scrollToBottom();
    }

    function showLoadingIndicator() {
        const existing = document.getElementById('loading-indicator');
        if (existing) return;
        const loadingBubble = document.createElement('div');
        loadingBubble.id = 'loading-indicator';
        loadingBubble.classList.add('message-bubble', 'bot-message');
        loadingBubble.innerHTML = `
            <div class="flex items-center space-x-1">
                <span class="loading-dot"></span>
                <span class="loading-dot"></span>
                <span class="loading-dot"></span>
            </div>
        `;
        chatMessages.appendChild(loadingBubble);
        scrollToBottom();
    }

    function removeLoadingIndicator() {
        const indicator = document.getElementById('loading-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
    
    function setFormState(disabled) {
        isLoading = disabled;
        chatInput.disabled = disabled;
        sendBtn.disabled = disabled;
        sendBtn.textContent = disabled ? '...' : 'Enviar';
    }



    async function fetchGeminiResponse(userQuery, retries = 0) {
        const maxRetries = 5;
        const delay = Math.pow(2, retries) * 1000 + (Math.random() * 1000); // 2s, 4s, 8s... + jitter
        
        try {
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN 
                },
                body: JSON.stringify({ message: userQuery })
            });

            if (!response.ok) {
                // Manejo específico de errores HTTP
                if (response.status === 403) {
                     return "Error de permiso (CSRF). Intenta recargar la página.";
                }
                if (response.status === 404) {
                     return "Error de conexión: No encuentro la ruta de la API.";
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.error) {
                return `Lo siento, hubo un error al procesar tu solicitud: ${data.error}`;
            }

            // devolver el texto del asistente
            return data.response || "Lo siento, recibí una respuesta vacía.";
            
        } catch (error) {
            if (retries < maxRetries) {
                // Si falla, espera y reintenta
                await new Promise(resolve => setTimeout(resolve, delay));
                return fetchGeminiResponse(userQuery, retries + 1);
            } else {
                console.error('La llamada a la API falló tras varios intentos:', error);
                return "Lo siento, el asistente no pudo conectarse. Por favor, revisa tu conexión o inténtalo más tarde.";
            }
        }
    }

    // --- Manejo del envío del formulario ---

    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (isLoading) return;

            const userQuery = chatInput.value.trim();
            if (!userQuery) return;

            // 1. Mostrar mensaje del usuario
            addMessage(userQuery, 'user');
            chatInput.value = '';

            // 2. Deshabilitar input y mostrar cargando
            setFormState(true);
            showLoadingIndicator();

            // 3. Obtener respuesta de la IA
            const botResponse = await fetchGeminiResponse(userQuery);

            // 4. Quitar cargando, mostrar respuesta, rehabilitar input
            removeLoadingIndicator();
            addMessage(botResponse, 'bot');
            setFormState(false);
            
            // Foco de nuevo en el input para seguir escribiendo rápido
            chatInput.focus();
        });
    }

    // Accesibilidad: cerrar chat con Escape si está abierto
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && isChatOpen) {
            closeChat();
        }
    });

});
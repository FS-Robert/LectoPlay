    
    
        document.addEventListener('DOMContentLoaded', () => {
            const toggleBtn = document.getElementById('chatbot-toggle');
            const closeBtn = document.getElementById('close-chat-btn');
            const chatWindow = document.getElementById('chatbot-window');
            const chatForm = document.getElementById('chat-input-form');
            const chatInput = document.getElementById('chat-input');
            const chatMessages = document.getElementById('chat-messages');
            const sendBtn = document.getElementById('chat-send-btn');
            
            // Function to retrieve the Django CSRF token from cookies
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            
            // Retrieve the token once on load
            const CSRF_TOKEN = getCookie('csrftoken');

            let isChatOpen = false;
            let isLoading = false;

            // Define the API endpoint that your Django view will handle
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
                // move focus back to the floating button for accessibility
                if (toggleBtn) toggleBtn.focus();
            }

            function toggleChat() {
                if (isChatOpen) {
                    closeChat();
                } else {
                    openChat();
                }
            }

            // Ensure the toggle button exists (safety)
            if (toggleBtn) {
                toggleBtn.addEventListener('click', toggleChat);
                // allow keyboard opening
                toggleBtn.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        toggleChat();
                    }
                });
            }

           // Boton para cerrar el chat
            if (closeBtn) {
                closeBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    closeChat();
                });
                // allow keyboard closing
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
                // Simple markdown conversion for bold text (e.g., **word**)
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

            // --- API Call and Exponential Backoff ---

            async function fetchGeminiResponse(userQuery, retries = 0) {
                const maxRetries = 5;
                const delay = Math.pow(2, retries) * 1000 + (Math.random() * 1000); // 2s, 4s, 8s... + jitter
                
                try {
                    const response = await fetch(API_ENDPOINT, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            // Use the retrieved CSRF token
                            'X-CSRFToken': CSRF_TOKEN 
                        },
                        body: JSON.stringify({ message: userQuery })
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    const data = await response.json();
                    
                    if (data.error) {
                        return `Lo siento, hubo un error al procesar tu solicitud: ${data.error}`;
                    }

                    // return the assistant text
                    return data.response || "Lo siento, recibí una respuesta vacía.";
                    
                } catch (error) {
                    if (retries < maxRetries) {
                        await new Promise(resolve => setTimeout(resolve, delay));
                        return fetchGeminiResponse(userQuery, retries + 1);
                    } else {
                        console.error('API call failed after max retries:', error);
                        return "Lo siento, el asistente no pudo conectarse. Por favor, inténtalo de nuevo más tarde.";
                    }
                }
            }

            // --- Form Submission Handler ---

            if (chatForm) {
                chatForm.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    if (isLoading) return;

                    const userQuery = chatInput.value.trim();
                    if (!userQuery) return;

                    // 1. Display user message
                    addMessage(userQuery, 'user');
                    chatInput.value = '';

                    // 2. Disable input and show loading
                    setFormState(true);
                    showLoadingIndicator();

                    // 3. Get AI response
                    const botResponse = await fetchGeminiResponse(userQuery);

                    // 4. Remove loading, display bot response, re-enable input
                    removeLoadingIndicator();
                    addMessage(botResponse, 'bot');
                    setFormState(false);
                });
            }

            // Accessibility: close chat when pressing Escape while open
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && isChatOpen) {
                    closeChat();
                }
            });

        });
   
        
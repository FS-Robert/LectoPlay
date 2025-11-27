const utterance = new SpeechSynthesisUtterance(texto);
utterance.lang = 'es-ES'; // idioma
utterance.voice = speechSynthesis.getVoices()[1]; // índice de la voz
utterance.rate = 1; // velocidad
speechSynthesis.speak(utterance);

// --- Importaciones de Firebase ---
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

// --- Configuración de proyecto Firebase ---
const firebaseConfig = {
  apiKey: "AIzaSyC104WVyRbn8qqMyXECEurTMDjlH0qKj1I",
  authDomain: "lectorplay-ab1e0.firebaseapp.com",
  projectId: "lectorplay-ab1e0",
  storageBucket: "lectorplay-ab1e0.firebasestorage.app",
  messagingSenderId: "577582475679",
  appId: "1:577582475679:web:7c1c5f71df45490f9575aa"
};

// --- Inicialización de Firebase ---
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// --- Función para registrar usuario ---
window.registerUser = function() {
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!name || !email || !password) {
    alert("Por favor, completa todos los campos.");
    return;
  }

  createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      const user = userCredential.user;
      console.log("Usuario creado:", user);
      alert(`¡Bienvenido ${name}! Tu cuenta fue creada con éxito.`);
      window.location.href = "/login"; // redirige al login
    })
    .catch((error) => {
      console.error("Error al registrar usuario:", error.message);
      alert("Error al crear la cuenta: " + error.message);
    });
};

// --- Función para iniciar sesión ---
window.loginUser = function() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!email || !password) {
    alert("Por favor, completa todos los campos.");
    return;
  }

  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      const user = userCredential.user;
      console.log("Inicio de sesión exitoso:", user.email);

      // Guardar sesión localmente
      localStorage.setItem("userEmail", user.email);

      // Redirigir a la página principal
      window.location.href = "/";
    })
    .catch((error) => {
      console.error("Error al iniciar sesión:", error.message);
      alert("Error al iniciar sesión: " + error.message);
    });
};


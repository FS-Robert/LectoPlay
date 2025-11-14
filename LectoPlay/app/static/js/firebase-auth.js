// --- Importaciones de Firebase ---
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { 
  getAuth, 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  updateProfile,
  onAuthStateChanged,
  signOut,
  browserSessionPersistence, 
  setPersistence
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

// --- Configuración de Firebase ---
const firebaseConfig = {
  apiKey: "AIzaSyC104WVyRbn8qqMyXECEurTMDjlH0qKj1I",
  authDomain: "lectorplay-ab1e0.firebaseapp.com",
  projectId: "lectorplay-ab1e0",
  storageBucket: "lectorplay-ab1e0.firebasestorage.app",
  messagingSenderId: "577582475679",
  appId: "1:577582475679:web:7c1c5f71df45490f9575aa"
};

// --- Inicialización ---
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Sesión en pestaña abierta
setPersistence(auth, browserSessionPersistence);

// ===============================
// 🔥 LISTENER GLOBAL DE SESIÓN
// ===============================
onAuthStateChanged(auth, (user) => {
  window.currentUser = user;

  if (user) {
    localStorage.setItem("userEmail", user.email);
    localStorage.setItem("userName", user.displayName ?? "");
  }
});

// ===============================
// 🔥 Registrar usuario
// ===============================
window.registerUser = function() {
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!name || !email || !password) {
    alert("Por favor, completa todos los campos.");
    return;
  }

  createUserWithEmailAndPassword(auth, email, password)
    .then(async (userCredential) => {
      const user = userCredential.user;

      await updateProfile(user, { displayName: name });
      await user.reload();

      alert(`¡Bienvenido ${name}! Tu cuenta fue creada con éxito.`);
      window.location.href = "/login";
    })
    .catch((error) => {
      console.error("Error al registrar:", error.message);
      alert("Error: " + error.message);
    });
};

// ===============================
// 🔥 Iniciar sesión
// ===============================
window.loginUser = function() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!email || !password) {
    alert("Completa todos los campos.");
    return;
  }

  signInWithEmailAndPassword(auth, email, password)
    .then(async (userCredential) => {
      const user = userCredential.user;
      await user.reload();

      localStorage.setItem("userEmail", user.email);
      localStorage.setItem("userName", user.displayName ?? "");

      const redirect = localStorage.getItem("redirectAfterLogin");

      if (redirect) {
        localStorage.removeItem("redirectAfterLogin");
        window.location.href = redirect;
      } else {
        window.location.href = "/";
      }
    })
    .catch((error) => {
      console.error("Error al iniciar sesión:", error.message);
      alert("Error al iniciar sesión: " + error.message);
    });
};

// ===============================
// 🔥 Cerrar sesión
// ===============================
window.logoutUser = async function() {
  try {
    await signOut(auth);

    localStorage.removeItem("userEmail");
    localStorage.removeItem("userName");

    window.location.href = "/";
  } catch (error) {
    console.error("Error al cerrar sesión:", error);
  }
};

// ===================================================
// 🔥 PROTEGER RUTAS (Versión final, optimizada, sin bugs)
// ===================================================

// Esperar a que Firebase cargue la sesión real
function waitForAuthInit() {
  return new Promise((resolve) => {
    const unsub = onAuthStateChanged(auth, (user) => {
      unsub(); // Se ejecuta una sola vez
      resolve(user);
    });
  });
}

// Usado en /ejercicios, /perfil, etc.
window.protectRoute = async function(path) {
  console.log("⏳ protectRoute: Esperando restauración de sesión...");

  const user = await waitForAuthInit();

  console.log("protectRoute — usuario:", user);

  if (!user) {
    console.log("⚠ No logueado → redirigiendo al login");
    localStorage.setItem("redirectAfterLogin", path);
    window.location.href = "/login";
  } else {
    console.log("🔐 Usuario autenticado → acceso permitido");
  }
};

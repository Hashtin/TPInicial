// config.js

// Backend local (desarrollo)
const LOCAL_API = "http://127.0.0.1:5000/api";

// Backend en producción (Railway)
const PROD_API = "https://TU-PROYECTO.up.railway.app/api";

// Elegir automáticamente según el entorno
const API_URL = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
    ? LOCAL_API
    : PROD_API;

console.log("Usando API:", API_URL);

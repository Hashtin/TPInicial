// config.js

// Backend local (desarrollo)
const LOCAL_API = "http://127.0.0.1:5000/api";

// Backend en producción (Railway)
const PROD_API = "https://tpinicial.onrender.com/api";

// Elegir automáticamente según el entorno
const API_URL = PROD_API;

console.log("Usando API:", API_URL);

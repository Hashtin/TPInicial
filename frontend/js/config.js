// config.js

// Backend local (desarrollo)
const LOCAL_API = "http://127.0.0.1:5000/api";

// Backend en producción (Railway)
const PROD_API = "https://tpinicial.onrender.com/api";

// Detección automática de entorno
const isLocal = window.location.hostname === 'localhost' || 
                window.location.hostname === '127.0.0.1';

// URLs de la API
const API_URL = isLocal ? 
    "http://127.0.0.1:5000/api" : 
    "https://tpinicial.onrender.com/api";


console.log("Usando API:", API_URL);
import os
from dotenv import load_dotenv

# CARGAR EL ARCHIVO .env
load_dotenv()

class AppSettings:
    # CONFIGURACION DE LA API DE OPENWEATHER
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    GEOCODING_URL = os.getenv("OPENWEATHER_GEOCODING_URL")
    WEATHER_URL = os.getenv("OPENWEATHER_WEATHER_URL")
    
    #CONFIGURACION DE LLAMADAS HTTP
    TIMEOUT_SECONDS = 10
    UNITS = "metric"
    LANGUAGE = "es"
    
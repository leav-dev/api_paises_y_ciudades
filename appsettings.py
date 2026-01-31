"""
=============================================================================
CONFIGURACIÓN CENTRALIZADA DE LA APLICACIÓN
=============================================================================

Este módulo contiene la configuración global de la aplicación, cargando
las variables de entorno desde el archivo .env y exponiendo constantes
de configuración.

¿Por qué usar un archivo de configuración centralizado?
-------------------------------------------------------
1. FLEXIBILIDAD: Puedes cambiar configuraciones sin modificar código
2. AMBIENTES: Fácil de tener diferentes configuraciones (dev, staging, prod)
3. MANTENIBILIDAD: Un solo lugar para todas las configuraciones
4. CONSISTENCIA: Valores por defecto sensatos para toda la aplicación

Contenido del archivo .env (ejemplo):
-------------------------------------
RESTCOUNTRIES_BASE_URL=https://restcountries.com/v3.1
RESTCOUNTRIES_TIMEOUT=10

NOTA: La API de REST Countries es completamente gratuita y no requiere
API Key ni registro. El archivo .env es opcional para esta aplicación.

Autor: Ing. Luis E. ALbor Vega
Fecha: Enero 2026
=============================================================================
"""

# os proporciona funciones para interactuar con el sistema operativo
# Usamos os.getenv() para leer variables de entorno
import os

# python-dotenv permite cargar variables de entorno desde un archivo .env
# Esto es muy útil en desarrollo para no tener que configurar variables
# de entorno del sistema manualmente
from dotenv import load_dotenv


# =============================================================================
# CARGAR VARIABLES DE ENTORNO
# =============================================================================
# load_dotenv() busca un archivo llamado .env en el directorio actual
# y carga todas las variables definidas en él como variables de entorno
# 
# Ejemplo de contenido de .env:
# OPENWEATHER_API_KEY=abc123
# 
# Después de load_dotenv(), puedes acceder con os.getenv("OPENWEATHER_API_KEY")
load_dotenv()


class AppSettings:
    """
    Clase de configuración que contiene todas las constantes de la aplicación.
    
    Usamos una clase en lugar de variables sueltas por las siguientes razones:
    - Agrupa todas las configuraciones en un solo lugar
    - Permite validación y transformación de valores
    - Facilita el autocompletado en el IDE
    - Es más fácil de mockear en tests
    
    Uso:
        from appsettings import AppSettings
        
        base_url = AppSettings.RESTCOUNTRIES_BASE_URL
        timeout = AppSettings.TIMEOUT_SECONDS
    
    Nota: Todos los atributos son de clase (class attributes), no de instancia.
    Esto significa que no necesitas crear una instancia para usarlos:
        AppSettings.RESTCOUNTRIES_BASE_URL  # ✓ Correcto
        AppSettings().RESTCOUNTRIES_BASE_URL  # También funciona, pero innecesario
    """

    # =========================================================================
    # CONFIGURACIÓN DE LA API DE REST COUNTRIES
    # =========================================================================
    
    # URL base de la API de REST Countries - Versión 3.1
    # Documentación: https://restcountries.com/
    # Esta API es completamente gratuita y no requiere API Key
    RESTCOUNTRIES_BASE_URL = os.getenv("RESTCOUNTRIES_BASE_URL", "https://restcountries.com/v3.1")
    
    # Endpoints específicos de la API
    # Obtener todos los países: {BASE_URL}/all
    # Buscar por nombre: {BASE_URL}/name/{name}
    # Buscar por código: {BASE_URL}/alpha/{code}
    # Buscar por moneda: {BASE_URL}/currency/{currency}
    # Buscar por idioma: {BASE_URL}/lang/{language}

    # =========================================================================
    # CONFIGURACIÓN DE LLAMADAS HTTP
    # =========================================================================
    
    # Tiempo máximo de espera para las peticiones HTTP (en segundos)
    # Si la API de REST Countries no responde en este tiempo, se lanza un error
    # Un valor muy bajo puede causar errores en redes lentas
    # Un valor muy alto puede hacer que la aplicación parezca "colgada"
    TIMEOUT_SECONDS = int(os.getenv("RESTCOUNTRIES_TIMEOUT", "10"))
    
    # =========================================================================
    # CONFIGURACIÓN DE FILTROS Y CAMPOS
    # =========================================================================
    
    # Campos por defecto que queremos obtener de la API para optimizar respuestas
    # La API permite filtrar campos específicos para reducir el tamaño de respuesta
    # Ejemplo: ?fields=name,capital,population,currencies,languages,flags
    DEFAULT_FIELDS = "name,capital,population,currencies,languages,flags,region,subregion,cca2,cca3"
    
    # =========================================================================
    # CONFIGURACIÓN DE LA APLICACIÓN
    # =========================================================================
    
    # Información de la aplicación
    APP_NAME = os.getenv("APP_NAME", "Countries API")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    
    # Configuración de logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # =========================================================================
    # CONFIGURACIÓN DE CACHE (OPCIONAL)
    # =========================================================================
    
    # Tiempo de cache en segundos para respuestas de países
    # Los datos de países no cambian frecuentemente, por lo que podemos cachearlos
    CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))  # 1 hora por defecto
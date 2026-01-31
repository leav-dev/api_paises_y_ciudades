"""
=============================================================================
CLIENTE HTTP PARA LA API DE REST COUNTRIES
=============================================================================

Este módulo contiene la clase RestCountriesClient que se encarga de realizar
las peticiones HTTP a la API externa de REST Countries.

La API de REST Countries proporciona información completa sobre países:
- Información básica: nombre, capital, población
- Datos geográficos: región, subregión, coordenadas
- Datos culturales: idiomas, monedas, banderas
- Códigos estándar: ISO 2/3 letras, códigos de llamada

Documentación oficial: https://restcountries.com/

Ventajas de esta API:
- Completamente gratuita (no requiere API key)
- Sin límites de uso
- Datos actualizados y completos
- Múltiples endpoints para diferentes consultas

Autor: Ing. Eduardo Pimienta
Fecha: Enero 2026
=============================================================================
"""

# httpx es una librería moderna para hacer peticiones HTTP asíncronas en Python
# Es similar a 'requests' pero soporta async/await de forma nativa
import httpx

# HTTPException nos permite lanzar errores HTTP con códigos de estado específicos
# FastAPI los convierte automáticamente en respuestas HTTP apropiadas
from fastapi import HTTPException

# Importamos la configuración centralizada de la aplicación
# Contiene las URLs de la API, la API key y otros parámetros
from appsettings import AppSettings



class RestCountriesClient:
  """
  Cliente HTTP para interactuar con la API de REST Countries.
  
  Esta clase encapsula toda la lógica de comunicación con la API externa,
  siguiendo el patrón de diseño "Client" o "Gateway". Esto permite:
  
  - Separar la lógica de HTTP de la lógica de negocio
  - Facilitar el testing mediante mocks
  - Centralizar el manejo de errores de la API externa
  - Reutilizar el cliente en diferentes servicios si es necesario
  
  Ejemplo de uso:
    async with httpx.AsyncClient() as http_client:
      countries_client = RestCountriesClient()
      country = await countries_client.get_country_by_name("colombia", http_client)
      countries = await countries_client.get_countries_by_currency("usd", http_client)
  """

  def __init__(self):
    """
    Constructor de la clase.
    
    Actualmente no requiere inicialización especial, pero se mantiene
    por si en el futuro se necesita inyectar dependencias o configuración.
    """
    pass

  async def get_country_by_code(self, country_code: str, http_client: httpx.AsyncClient) -> dict:
    """
    Obtiene información completa de un país por su codigo.
    Args:
      country_name (str): Nombre del país a buscar (ej: "colombia", "spain")
      http_client (httpx.AsyncClient): Cliente HTTP asíncrono compartido.
    """
    url = f"{AppSettings.RESTCOUNTRIES_BASE_URL}/alpha/{country_code}"
    response = await http_client.get(url, params={"fields": AppSettings.DEFAULT_FIELDS}, timeout=AppSettings.TIMEOUT_SECONDS)
    # Convertimos la respuesta JSON a un diccionario
    data = response.json()
    # Verificamos si la respuesta fue exitosa
    if response.status_code == 404 and len(data)==0:
      raise HTTPException(status_code=404, detail=f"País '{country_code}' no encontrado. Verifica el nombre e intenta de nuevo.")
    elif response.status_code != 200:
      raise HTTPException(status_code=response.status_code, detail="Error al obtener información del país desde REST Countries API")

    return data  # Retornamos el primer país encontrado

  async def get_country_by_name(self, country_name: str, http_client: httpx.AsyncClient) -> dict:
    """
    Obtiene información completa de un país por su nombre.
    Args:
      country_name (str): Nombre del país a buscar (ej: "colombia", "spain")
      http_client (httpx.AsyncClient): Cliente HTTP asíncrono compartido.
    """
    # Construimos la URL para buscar por nombre
    url = f"{AppSettings.RESTCOUNTRIES_BASE_URL}/name/{country_name}"
    # Realizamos la petición GET a la API de REST Countries
    response = await http_client.get(url, params={"fields": AppSettings.DEFAULT_FIELDS}, timeout=AppSettings.TIMEOUT_SECONDS)
    # Convertimos la respuesta JSON a un diccionario
    data = response.json()
    # Verificamos si la respuesta fue exitosa
    if response.status_code == 404 and len(data)==0:
      raise HTTPException(status_code=404, detail=f"País '{country_name}' no encontrado. Verifica el nombre e intenta de nuevo.")
    elif response.status_code != 200:
      raise HTTPException(status_code=response.status_code, detail="Error al obtener información del país desde REST Countries API")

    return data  # Retornamos el primer país encontrado

  async def get_countries_by_currency(self, currency_code: str, http_client: httpx.AsyncClient) -> list[dict]:
    """
    Obtiene todos los países que usan una moneda específica.
    
    Args:
      currency_code (str): Código de moneda ISO (ej: "usd", "eur", "cop")
      http_client (httpx.AsyncClient): Cliente HTTP asíncrono compartido
    """
    url = f"{AppSettings.RESTCOUNTRIES_BASE_URL}/currency/{currency_code}"
    
    response = await http_client.get(url, params={"fields": AppSettings.DEFAULT_FIELDS}, timeout=AppSettings.TIMEOUT_SECONDS )
    data = response.json()
    if response.status_code == 404 and len(data) == 0:
      raise HTTPException(status_code=404, detail=f"No se encontraron países que usen la moneda '{currency_code}'")
    elif response.status_code != 200:
      raise HTTPException(status_code=response.status_code, detail="Error al obtener países por moneda desde REST Countries API"
      )

    return data

  async def get_countries_by_language(self, language_code: str, http_client: httpx.AsyncClient) -> list[dict]:
    """
    Obtiene todos los países que hablan un idioma específico.
    
    Args:
      language_code (str): Código de idioma ISO (ej: "spa", "eng", "fra")
      http_client (httpx.AsyncClient): Cliente HTTP asíncrono compartido
    """
    url = f"{AppSettings.RESTCOUNTRIES_BASE_URL}/lang/{language_code}"
    
    response = await http_client.get(url, params={"fields": AppSettings.DEFAULT_FIELDS}, timeout=AppSettings.TIMEOUT_SECONDS)

    data = response.json()
    if response.status_code == 404 and len(data) == 0:
      raise HTTPException(status_code=404, detail=f"No se encontraron países que hablen '{language_code}'")
    elif response.status_code != 200:
      raise HTTPException(status_code=response.status_code, detail="Error al obtener países por idioma desde REST Countries API")

    return data
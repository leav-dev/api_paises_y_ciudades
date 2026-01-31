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

    async def get_country_by_name(self, country_name: str, http_client: httpx.AsyncClient) -> dict:
        """
        Obtiene información completa de un país por su nombre.
        
        Args:
            country_name (str): Nombre del país a buscar (ej: "colombia", "spain")
            http_client (httpx.AsyncClient): Cliente HTTP asíncrono compartido.
        
        Returns:
            dict: Diccionario con toda la información del país
        
        Raises:
            HTTPException(404): Si el país no fue encontrado
            HTTPException(status_code): Si hay un error en la API
        
        Ejemplo:
            country = await client.get_country_by_name("colombia", http_client)
            print(country["name"]["common"])  # "Colombia"
        """
        # Construimos la URL para buscar por nombre
        url = f"{AppSettings.RESTCOUNTRIES_BASE_URL}/name/{country_name}"
        
        # Realizamos la petición GET a la API de REST Countries
        response = await http_client.get(
            url,
            params={
                "fields": AppSettings.DEFAULT_FIELDS  # Solo los campos que necesitamos
            },
            timeout=AppSettings.TIMEOUT_SECONDS
        )

        # Verificamos si la respuesta fue exitosa
        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"País '{country_name}' no encontrado. Verifica el nombre e intenta de nuevo."
            )
        elif response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error al obtener información del país desde REST Countries API"
            )

        # Convertimos la respuesta JSON a un diccionario
        data = response.json()
        
        # La API devuelve una lista, tomamos el primer resultado
        if not data or len(data) == 0:
            raise HTTPException(
                status_code=404,
                detail=f"País '{country_name}' no encontrado. Verifica el nombre e intenta de nuevo."
            )

        return data[0]  # Retornamos el primer país encontrado

    async def get_countries_by_currency(self, currency_code: str, http_client: httpx.AsyncClient) -> list[dict]:
        """
        Obtiene todos los países que usan una moneda específica.
        
        Args:
            currency_code (str): Código de moneda ISO (ej: "usd", "eur", "cop")
            http_client (httpx.AsyncClient): Cliente HTTP asíncrono compartido
        
        Returns:
            list[dict]: Lista de países que usan la moneda especificada
        
        Raises:
            HTTPException(404): Si no se encuentran países con esa moneda
            HTTPException(status_code): Si hay un error en la API
        """
        url = f"{AppSettings.RESTCOUNTRIES_BASE_URL}/currency/{currency_code}"
        
        response = await http_client.get(
            url,
            params={
                "fields": AppSettings.DEFAULT_FIELDS
            },
            timeout=AppSettings.TIMEOUT_SECONDS
        )

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron países que usen la moneda '{currency_code}'"
            )
        elif response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error al obtener países por moneda desde REST Countries API"
            )

        return response.json()

    async def get_countries_by_language(self, language_code: str, http_client: httpx.AsyncClient) -> list[dict]:
        """
        Obtiene todos los países que hablan un idioma específico.
        
        Args:
            language_code (str): Código de idioma ISO (ej: "spa", "eng", "fra")
            http_client (httpx.AsyncClient): Cliente HTTP asíncrono compartido
        
        Returns:
            list[dict]: Lista de países que hablan el idioma especificado
        
        Raises:
            HTTPException(404): Si no se encuentran países con ese idioma
            HTTPException(status_code): Si hay un error en la API
        """
        url = f"{AppSettings.RESTCOUNTRIES_BASE_URL}/lang/{language_code}"
        
        response = await http_client.get(
            url,
            params={
                "fields": AppSettings.DEFAULT_FIELDS
            },
            timeout=AppSettings.TIMEOUT_SECONDS
        )

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron países que hablen '{language_code}'"
            )
        elif response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error al obtener países por idioma desde REST Countries API"
            )

        return response.json()
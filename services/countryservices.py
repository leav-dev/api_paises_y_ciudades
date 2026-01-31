"""
=============================================================================
SERVICIO DE PAÍSES (CAPA DE LÓGICA DE NEGOCIO)
=============================================================================

Este módulo contiene la clase CountriesService que implementa la lógica de
negocio para obtener información sobre países del mundo.

En una arquitectura de capas (Layered Architecture), este servicio actúa
como intermediario entre:
- Controladores (reciben las peticiones HTTP)
- Clientes (se comunican con APIs externas)
- DTOs (definen la estructura de los datos de respuesta)

Responsabilidades de este servicio:
1. Validar la entrada del usuario
2. Coordinar las llamadas al cliente de REST Countries
3. Transformar los datos crudos de la API en DTOs estructurados
4. Manejar errores de configuración y validación

Autor: Ing. Eduardo Pimienta
Fecha: Enero 2026
=============================================================================
"""

# httpx es la librería para peticiones HTTP asíncronas
# La usamos para tipar el parámetro http_client
import httpx

# HTTPException permite lanzar errores HTTP que FastAPI convierte en respuestas
from fastapi import HTTPException

# Importamos el cliente que se comunica con la API de REST Countries
# Este cliente encapsula toda la lógica de HTTP
from clients.countryClient import RestCountriesClient

# Importamos el DTO (Data Transfer Object) que define la estructura de respuesta
# Usar DTOs garantiza que siempre devolvamos datos con el formato correcto
from DTOs.countryDtos import CountryResponseDTO


class CountriesService:
  """
  Servicio principal para obtener información sobre países.
  
  Esta clase implementa el patrón de diseño "Service Layer", que separa
  la lógica de negocio de los controladores y los clientes HTTP.
  
  Ventajas de usar un servicio:
  - Los controladores quedan simples (solo reciben y responden)
  - La lógica de negocio es reutilizable
  - Facilita el testing unitario
  - Permite agregar validaciones, caché, logging, etc.
  
  Atributos:
    client (RestCountriesClient): Instancia del cliente HTTP para REST Countries
  
  Ejemplo de uso:
    async with httpx.AsyncClient() as http_client:
      service = CountriesService()
      country = await service.get_country("colombia", http_client)
      print(country.population)
  """

  def __init__(self):
    """
    Constructor del servicio.
    
    Inicializa el servicio creando una instancia del cliente de REST Countries.
    A diferencia de otras APIs, REST Countries no requiere API key.
    """
    # Creamos una instancia del cliente de REST Countries
    # Este cliente se reutilizará en todas las llamadas del servicio
    self.client = RestCountriesClient()

  async def get_country(self, country_name: str, http_client: httpx.AsyncClient) -> CountryResponseDTO:
    """    
    Ejemplo de respuesta:
      CountryResponseDTO(
        name="Colombia",
        official_name="Republic of Colombia",
        capital="Bogotá",
        population=50882884,
        region="Americas",
        subregion="South America",
        currencies=[{"code": "COP", "name": "Colombian peso", "symbol": "$"}],
        languages=["Spanish"],
        flag="https://flagcdn.com/w320/co.png",
        country_code="CO"
      )
    """
    # limpiamos la entrada
    country_name = country_name.strip()
    # Consultamos la pai para obtener el pail
    country_data = await self.client.get_country_by_name(country_name, http_client)
    country_data = country_data[0]
    # Convertimos los datos al D
    currencies = []
    if "currencies" in country_data:
      for code, currency_info in country_data["currencies"].items():
        currencies.append({
          "code": code,
          "name": currency_info.get("name", ""),
          "symbol": currency_info.get("symbol", "")
        })
    # Extraer idiomas
    languages = []
    if "languages" in country_data:
      languages = list(country_data["languages"].values())
    # Obtener capital (puede ser una lista)
    capital = ""
    if "capital" in country_data and country_data["capital"]:
      capital = country_data["capital"][0] if isinstance(country_data["capital"], list) else country_data["capital"]
    
    return CountryResponseDTO(
      name=country_data["name"]["common"],
      official_name=country_data["name"]["official"],
      capital=capital,
      population=country_data.get("population", 0),
      region=country_data.get("region", ""),
      subregion=country_data.get("subregion", ""),
      currencies=currencies,
      languages=languages,
      flag=country_data.get("flags", {}).get("png", ""),
      country_code=country_data.get("cca2", "")
    )

  async def get_country_by_code(self, country_code: str, http_client: httpx.AsyncClient) -> CountryResponseDTO:
    """
    Obtiene información de un país por su código ISO (ej: "CO", "US", "FR").
    
    Args:
      country_code (str): Código ISO de 2 letras del país
      http_client (httpx.AsyncClient): Cliente HTTP para realizar peticiones
    
    Returns:
      CountryResponseDTO: Información estructurada del país
    
    Raises:
      HTTPException: Si el país no existe o hay error en la API
    """
    country_code = country_code.strip().upper()
    country_data = await self.client.get_country_by_code(country_code, http_client)

    currencies = []
    if "currencies" in country_data:
      for code, currency_info in country_data["currencies"].items():
        currencies.append({
          "code": code,
          "name": currency_info.get("name", ""),
          "symbol": currency_info.get("symbol", "")
        })
    
    # Extraer idiomas
    languages = []
    if "languages" in country_data:
      languages = list(country_data["languages"].values())
    
    # Obtener capital (puede ser una lista)
    capital = ""
    if "capital" in country_data and country_data["capital"]:
      capital = country_data["capital"][0] if isinstance(country_data["capital"], list) else country_data["capital"]
    
    return CountryResponseDTO(
      name=country_data["name"]["common"],
      official_name=country_data["name"]["official"],
      capital=capital,
      population=country_data.get("population", 0),
      region=country_data.get("region", ""),
      subregion=country_data.get("subregion", ""),
      currencies=currencies,
      languages=languages,
      flag=country_data.get("flags", {}).get("png", ""),
      country_code=country_data.get("cca2", "")
    )

  async def get_countries_by_currency(self, currency_code: str, http_client: httpx.AsyncClient) -> list[CountryResponseDTO]:
    """
    Obtiene todos los países que usan una moneda específica.
    """
    currency_code = currency_code.strip().upper()
    countries_data = await self.client.get_countries_by_currency(currency_code, http_client)
    
    # Lista para almacenar todos los países procesados
    countries_list = []
    
    # Iterar sobre cada país en la respuesta
    for country_data in countries_data:  # ← ESTE ES EL BUCLE QUE TE FALTA
        
        # Procesar monedas para este país
        currencies = []
        if "currencies" in country_data:
            for code, currency_info in country_data["currencies"].items():
                currencies.append({
                    "code": code,
                    "name": currency_info.get("name", ""),
                    "symbol": currency_info.get("symbol", "")
                })
        
        # Extraer idiomas para este país
        languages = []
        if "languages" in country_data:
            languages = list(country_data["languages"].values())
        
        # Obtener capital para este país
        capital = ""
        if "capital" in country_data and country_data["capital"]:
            capital = country_data["capital"][0] if isinstance(country_data["capital"], list) else country_data["capital"]
        
        # Crear el DTO para este país y agregarlo a la lista
        country_dto = CountryResponseDTO(
            name=country_data["name"]["common"],
            official_name=country_data["name"]["official"],
            capital=capital,
            population=country_data.get("population", 0),
            region=country_data.get("region", ""),
            subregion=country_data.get("subregion", ""),
            currencies=currencies,
            languages=languages,
            flag=country_data.get("flags", {}).get("png", ""),
            country_code=country_data.get("cca2", "")
        )
        
        countries_list.append(country_dto)
    
    return countries_list

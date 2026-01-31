"""
=============================================================================
DTOs (DATA TRANSFER OBJECTS) - MODELOS DE DATOS
=============================================================================

Este módulo contiene los DTOs (Data Transfer Objects) utilizados para
estructurar los datos de respuesta de la API de países.

¿Qué es un DTO?
---------------
Un DTO es un objeto que define la estructura de los datos que se transfieren
entre capas de la aplicación o hacia/desde clientes externos.

¿Por qué usar DTOs en FastAPI?
------------------------------
1. VALIDACIÓN AUTOMÁTICA: Pydantic valida que los datos cumplan el esquema
2. DOCUMENTACIÓN: FastAPI genera docs automáticos (Swagger) basados en los DTOs
3. SERIALIZACIÓN: Convierte automáticamente objetos Python a JSON
4. TYPE HINTS: Mejora el autocompletado y detección de errores en el IDE
5. CONSISTENCIA: Garantiza que todas las respuestas tengan el mismo formato

Ejemplo de respuesta generada:
{
  "name": "Colombia",
  "official_name": "Republic of Colombia",
  "capital": "Bogotá",
  "population": 50882884,
  "region": "Americas",
  "subregion": "South America",
  "currencies": [
    {
      "code": "COP",
      "name": "Colombian peso",
      "symbol": "$"
    }
  ],
  "languages": ["Spanish"],
  "flag": "https://flagcdn.com/w320/co.png",
  "country_code": "CO"
}

Autor: Ing. Luis E. Albor Vega
Fecha: Enero 2026
=============================================================================
"""

# BaseModel es la clase base de Pydantic para definir modelos de datos
# Proporciona validación automática, serialización y documentación
from pydantic import BaseModel, Field
from typing import List


class CurrencyDTO(BaseModel):
  """
  DTO para representar una moneda.
  
  Atributos:
    code (str): Código ISO de la moneda (ej: "COP", "USD")
    name (str): Nombre completo de la moneda
    symbol (str): Símbolo de la moneda (ej: "$", "€")
  """
  code: str = Field(..., description="Código ISO de la moneda", examples=["COP", "USD", "EUR"])
  name: str = Field(..., description="Nombre completo de la moneda", examples=["Colombian peso", "US Dollar"])
  symbol: str = Field(..., description="Símbolo de la moneda", examples=["$", "€", "£"])  

class CountryResponseDTO(BaseModel):
  name: str = Field(..., description="Nombre común del país", examples=["Colombia", "Spain", "United States"])
  official_name: str = Field(..., description="Nombre oficial completo del país", examples=["Republic of Colombia", "Kingdom of Spain", "United States of America"])
  capital: str = Field(..., description="Capital principal del país", examples=["Bogotá", "Madrid", "Washington, D.C."])
  population: int = Field(..., description="Población total del país", examples=[50882884, 47351567, 331900000])
  region: str = Field(..., description="Región geográfica del país", examples=["Americas", "Europe", "Asia", "Africa", "Oceania"])
  subregion: str = Field(..., description="Subregión específica del país", examples=["South America", "Western Europe", "Northern America"])
  currencies: List[CurrencyDTO] = Field(..., description="Lista de monedas utilizadas en el país")
  languages: List[str] = Field(..., description="Lista de idiomas oficiales del país", examples=[["Spanish"], ["English"], ["Spanish", "Catalan", "Galician"]])
  flag: str = Field(..., description="URL de la imagen de la bandera del país", examples=["https://flagcdn.com/w320/co.png", "https://flagcdn.com/w320/es.png"])
  country_code: str = Field(..., description="Código de país de 2 letras (ISO 3166-1 alpha-2)", examples=["CO", "ES", "US"])
  class Config:
    """
    Configuración adicional del modelo Pydantic.
    
    json_schema_extra: Permite agregar ejemplos completos que aparecen en la documentación de Swagger UI.
    """
    json_schema_extra = {
      "example": {
        "name": "Colombia",
        "official_name": "Republic of Colombia",
        "capital": "Bogotá",
        "population": 50882884,
        "region": "Americas",
        "subregion": "South America",
        "currencies": [
          {
            "code": "COP",
            "name": "Colombian peso",
            "symbol": "$"
          }
        ],
        "languages": ["Spanish"],
        "flag": "https://flagcdn.com/w320/co.png",
        "country_code": "CO"
      }
    }
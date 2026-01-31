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

Autor: Ing. Eduardo Pimienta
Fecha: Enero 2026
=============================================================================
"""

# BaseModel es la clase base de Pydantic para definir modelos de datos
# Proporciona validación automática, serialización y documentación
from pydantic import BaseModel, Field
from typing import List, Dict, Any


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
    """
    DTO para la respuesta de información de países.
    
    Este modelo define la estructura exacta de los datos que se devuelven
    cuando un usuario consulta información de un país.
    
    Características:
    - Todos los campos son obligatorios (no tienen valor por defecto)
    - FastAPI valida automáticamente que los datos cumplan este esquema
    - Se genera documentación automática en Swagger UI
    
    Atributos:
        name (str): Nombre común del país
        official_name (str): Nombre oficial completo del país
        capital (str): Capital principal del país
        population (int): Población total del país
        region (str): Región geográfica (Americas, Europe, Asia, etc.)
        subregion (str): Subregión específica (South America, Western Europe, etc.)
        currencies (List[CurrencyDTO]): Lista de monedas utilizadas en el país
        languages (List[str]): Lista de idiomas oficiales
        flag (str): URL de la imagen de la bandera del país
        country_code (str): Código de país de 2 letras (ISO 3166-1 alpha-2)
    
    Ejemplo:
        >>> country = CountryResponseDTO(
        ...     name="Colombia",
        ...     official_name="Republic of Colombia",
        ...     capital="Bogotá",
        ...     population=50882884,
        ...     region="Americas",
        ...     subregion="South America",
        ...     currencies=[{"code": "COP", "name": "Colombian peso", "symbol": "$"}],
        ...     languages=["Spanish"],
        ...     flag="https://flagcdn.com/w320/co.png",
        ...     country_code="CO"
        ... )
        >>> country.model_dump()  # Convierte a diccionario
    """

    # =========================================================================
    # CAMPO: name (nombre común del país)
    # =========================================================================
    name: str = Field(
        ...,
        description="Nombre común del país",
        examples=["Colombia", "Spain", "United States"]
    )

    # =========================================================================
    # CAMPO: official_name (nombre oficial del país)
    # =========================================================================
    official_name: str = Field(
        ...,
        description="Nombre oficial completo del país",
        examples=["Republic of Colombia", "Kingdom of Spain", "United States of America"]
    )

    # =========================================================================
    # CAMPO: capital (capital del país)
    # =========================================================================
    capital: str = Field(
        ...,
        description="Capital principal del país",
        examples=["Bogotá", "Madrid", "Washington, D.C."]
    )

    # =========================================================================
    # CAMPO: population (población total)
    # =========================================================================
    population: int = Field(
        ...,
        description="Población total del país",
        examples=[50882884, 47351567, 331900000]
    )

    # =========================================================================
    # CAMPO: region (región geográfica)
    # =========================================================================
    region: str = Field(
        ...,
        description="Región geográfica del país",
        examples=["Americas", "Europe", "Asia", "Africa", "Oceania"]
    )

    # =========================================================================
    # CAMPO: subregion (subregión específica)
    # =========================================================================
    subregion: str = Field(
        ...,
        description="Subregión específica del país",
        examples=["South America", "Western Europe", "Northern America"]
    )

    # =========================================================================
    # CAMPO: currencies (monedas del país)
    # =========================================================================
    currencies: List[CurrencyDTO] = Field(
        ...,
        description="Lista de monedas utilizadas en el país"
    )

    # =========================================================================
    # CAMPO: languages (idiomas oficiales)
    # =========================================================================
    languages: List[str] = Field(
        ...,
        description="Lista de idiomas oficiales del país",
        examples=[["Spanish"], ["English"], ["Spanish", "Catalan", "Galician"]]
    )

    # =========================================================================
    # CAMPO: flag (URL de la bandera)
    # =========================================================================
    flag: str = Field(
        ...,
        description="URL de la imagen de la bandera del país",
        examples=["https://flagcdn.com/w320/co.png", "https://flagcdn.com/w320/es.png"]
    )

    # =========================================================================
    # CAMPO: country_code (código de país)
    # =========================================================================
    country_code: str = Field(
        ...,
        description="Código de país de 2 letras (ISO 3166-1 alpha-2)",
        examples=["CO", "ES", "US"]
    )

    # =========================================================================
    # CONFIGURACIÓN DEL MODELO
    # =========================================================================
    class Config:
        """
        Configuración adicional del modelo Pydantic.
        
        json_schema_extra: Permite agregar ejemplos completos que aparecen
                          en la documentación de Swagger UI.
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
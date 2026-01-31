"""
=============================================================================
CONTROLADOR DE PAÍSES (CAPA DE PRESENTACIÓN)
=============================================================================

Este módulo contiene los endpoints HTTP para consultar información sobre países.
Los controladores son la capa de presentación en una arquitectura de capas.

Responsabilidades:
- Recibir peticiones HTTP
- Validar parámetros de entrada
- Delegar la lógica de negocio al servicio
- Devolver respuestas HTTP estructuradas

Endpoints disponibles:
- GET /api/countries/{country} - Información de un país específico
- GET /api/countries/currency/{currency} - Países por moneda
- GET /api/countries/language/{language} - Países por idioma

Autor: Ing. Eduardo Pimienta
Fecha: Enero 2026
=============================================================================
"""

import httpx
from fastapi import APIRouter
from services.countryservices import CountriesService
from DTOs.countryDtos import CountryResponseDTO

# Creamos el router con prefijo para agrupar todos los endpoints de países
router = APIRouter(prefix="/api")

@router.get("/countries/{country}", response_model=CountryResponseDTO)
async def get_country(country: str):
    """
    Obtiene información detallada de un país específico.
    
    Args:
        country (str): Nombre del país a consultar (ej: "colombia", "spain")
    
    Returns:
        CountryResponseDTO: Información completa del país
    
    Raises:
        HTTPException(404): Si el país no existe
        HTTPException(500): Si hay errores del servidor
    """
    async with httpx.AsyncClient() as http_client:
        countries_service = CountriesService()
        country_response = await countries_service.get_country(country, http_client)
        return country_response
    
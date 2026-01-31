import httpx
from fastapi import HTTPException
from appsettings import AppSettings

class OpenWeatherClient:
    def __init__(self):
        
        async def get_coordinates(self, city: str):
            response = httpx.get(
                AppSettings.GEOCODING_URL,
                params={
                    "q": city,
                    "limit": 1,
                    "appid": AppSettings.OPENWEATHER_API_KEY
                },
                timeout=AppSettings.TIMEOUT_SECONDS
            )
            
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Error al obtener coordenadas")
            
            data = response.json()
            
            if not data:
                raise HTTPException(status_code=404, detail="Ciudad no encontrada")
            
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            
            return lat, lon
    
        async def get_weather(self, lat: float, lon: float):
            response = httpx.get(
                AppSettings.WEATHER_URL,
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": AppSettings.OPENWEATHER_API_KEY,
                    "units": AppSettings.UNITS,
                    "lang": AppSettings.LANGUAGE
                },
                timeout=AppSettings.TIMEOUT_SECONDS
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Error al obtener datos meteorológicos")
            
            return response.json()
                
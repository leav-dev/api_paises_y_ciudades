import httpx
from fastapi import HTTPException
from clients.weatherClient import OpenWeatherClient
from DTOs.weatherDtos import WeatherResponseDTO
from appsettings import appsettings

class WeatherService:
    def __init__(self):
        if not appsettings.OPENWEATHER_API_KEY:
            raise HTTPException(status_code=500, detail="OPENWEATHER_API_KEY no está configurado")
        self.client = OpenWeatherClient()

    async def get_weather(self, city: str, http_client: httpx.AsyncClient) -> WeatherResponseDTO:
        city = city.strip()
        
        lat, lon = await self.client.get_coordinates(city, http_client)
        weather_data = await self.client.get_weather(lat, lon, http_client)
        
        return WeatherResponseDTO(
            city=city,
            temperature=weather_data["main"]["temp"],
            humidity=weather_data["main"]["humidity"],
            description=weather_data["weather"][0]["description"]
        )

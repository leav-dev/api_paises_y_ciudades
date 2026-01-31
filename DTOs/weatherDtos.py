from pydantic import BaseModel, Field

class WeatherResponseDto(BaseModel):
    city: str = Field(..., description="nombre de la ciudad")
    temperature: float 
    humidity: int 
    description: str 
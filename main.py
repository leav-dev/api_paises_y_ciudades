from fastapi import FastAPI
from controllers.weathercontroller import router as weather_router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the Weather API"}
app.include_router(weather_router)
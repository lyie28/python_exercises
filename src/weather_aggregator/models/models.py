from pydantic import BaseModel, Field

class WeatherResult(BaseModel):
    city: str
    temperature: float = Field(gt=-100.0, lt=100.0)
    weather: str
    response_time: float = Field(gt=0.0)

class WeatherResponse(BaseModel):
    results: list[WeatherResult]
    total_time: float = Field(ge=0.0)
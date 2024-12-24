from .services.weather_service import WeatherService
from .models.models import WeatherResponse, WeatherResult
from time import time
import asyncio

class AsyncWeatherAggregator:
    def __init__(self) -> None:
        self.service = WeatherService()

    async def async_weather(self, cities: list[str]) -> WeatherResponse:
        if not all(isinstance(city, str) for city in cities):
            raise TypeError("Cities must be strings")
        start_time = time()
        if len(cities) < 1:
            raise ValueError("Cities list is empty")
        
        ret = WeatherResponse(results=[], total_time=0.0)
        tasks = [self.service.async_get_temperature(city) for city in cities]
        results = await asyncio.gather(*tasks)

        for city, (weather, temperature, response_time) in zip(cities, results):
            next = WeatherResult(city=city, weather=weather, temperature=temperature, response_time=response_time)
            ret.results.append(next)
            
        total_time = time() - start_time
        ret.total_time = total_time
        return ret


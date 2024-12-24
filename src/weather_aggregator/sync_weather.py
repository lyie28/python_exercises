from .services.weather_service import WeatherService
from .models.models import WeatherResponse, WeatherResult
from time import time

class WeatherAggregator:
    def __init__(self):
        self.service = WeatherService()

    def sync_weather(self, cities: list) -> WeatherResponse:
        if not all(isinstance(city, str) for city in cities):
            raise TypeError("Cities must be strings")
        start_time = time()
        if len(cities) < 1:
            raise ValueError("Cities list is empty")
        
        ret = WeatherResponse(results=[], total_time=0.0)
        for city in cities:
            weather, temperature, response_time = self.service.sync_get_temperature(city)
            next = WeatherResult(city=city, weather=weather, temperature=temperature, response_time=response_time)
            ret.results.append(next)
            
        total_time = time() - start_time
        ret.total_time = total_time
        return ret


from random import uniform, randrange
import asyncio
from time import sleep
from typing import Tuple

class WeatherService:
    
    def __init__(self) -> None:
        self.temps: dict[str, Tuple[float, float]] = {
            "Birmingham": (-5.0, 34.5),
            "London": (-3.0, 38.5),
            "Manchester": (-7.0, 33.5),
            "Liverpool": (-6.0, 33.5),
            "Leeds": (-7.0, 33.0)
        }

        self.mild_weathers = ["rainy", "windy", "cloudy"]
    
    def get_weather_type(self, temp: float) -> str:
        if temp < 1.0:
            return "snowing"
        elif temp > 20.0:
            return "sunny"
        return self.mild_weathers[randrange(0,len(self.mild_weathers))]

    def sync_get_temperature(self, city: str) -> Tuple[str, float, float]:
        if city not in self.temps.keys():
            raise ValueError("Invalid city name")
        random_delay = uniform(0.5, 2.5)
        sleep(random_delay)
        min_temp, max_temp = self.temps[city]
        temp = uniform(min_temp, max_temp)
        weather = self.get_weather_type(temp)
        return weather, temp, random_delay
    
    async def async_get_temperature(self, city:str) -> Tuple[str, float, float]:
        if city not in self.temps.keys():
            raise ValueError("Invalid city name")
        random_delay = uniform(0.5, 2.5)
        await asyncio.sleep(random_delay)
        min_temp, max_temp = self.temps[city]
        temp = uniform(min_temp, max_temp)
        weather = self.get_weather_type(temp)
        return weather, temp, random_delay

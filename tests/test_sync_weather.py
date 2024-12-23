from weather_dashboard.weather_aggregator.sync_weather import sync_weather
from pydantic import BaseModel
import pytest

class WeatherResult(BaseModel):
    city: str
    temperature: float
    weather: str
    response_time: float

class WeatherResponse(BaseModel):
    results: list[WeatherResult]
    total_time: float


def test_basic() -> None:
    """ Basic test that checks the sync_weather function with a single city """
    cities: list[str] = ["Birmingham"]
    results_list, total_time = sync_weather(cities)
    weather_response = WeatherResponse(results=results_list, total_time=total_time)
    assert len(results_list) == 1

def test_multiple_cities() -> None:
    """ Test that checks the sync_weather function with multiple cities """
    cities: list[str] = ["Birmingham", "London", "Manchester", "Liverpool", "Leeds"]
    results_list, total_time = sync_weather(cities)
    weather_response = WeatherResponse(results=results_list, total_time=total_time)
    assert len(results_list) == len(cities)
    # {} is set notation
    assert {result.city for result in weather_response.results} == set(cities)
    for result in weather_response.results:
        assert -100 < result.temperature < 100
    # assert all(-100 < result.temperature < 100 for result in weather_response.results)

def test_timing() -> None:
    """ Test that checks the sync_weather timings"""
    cities: list[str] = ["Birmingham", "London", "Manchester"]
    weather_response = WeatherResponse(sync_weather(cities))
    cities_time = weather_response.total_time
    assert abs(cities_time - sum(result.response_time for result in weather_response)) < 0.1

def test_empty_cities() -> None:
    """ Test that checks the sync_weather function with an empty list of cities """
    with pytest.raises(ValueError, match="Cities list is empty"):
        cities: list[str] = []
        sync_weather(cities)

def test_invalid_city() -> None:
    """ Test that checks the sync_weather function with an invalid city """
    with pytest.raises(ValueError, match="Invalid city name"):
        cities: list[str] = ["InvalidCity"]
        sync_weather(cities)
   
def test_non_string_input() -> None:
    """ Test that checks the sync_weather function with a non-string input """
    with pytest.raises(TypeError, match="Cities must be strings"):
        cities: list[int] = [1, 2, 3]
        sync_weather(cities)
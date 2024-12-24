from weather_aggregator.sync_weather import WeatherAggregator
from weather_aggregator.models.models import WeatherResponse
import pytest

@pytest.fixture
def weather_aggregator() -> WeatherAggregator:
    return WeatherAggregator()

def test_basic(weather_aggregator: WeatherAggregator) -> None:    
    """ Basic test that checks the sync_weather function with a single city """
    cities: list[str] = ["Birmingham"]
    weather_response: WeatherResponse = weather_aggregator.sync_weather(cities)
    assert len(weather_response.results) == 1

def test_multiple_cities(weather_aggregator: WeatherAggregator) -> None:
    """ Test that checks the WeatherAggregator.sync_weather function with multiple cities """
    cities: list[str] = ["Birmingham", "London", "Manchester", "Liverpool", "Leeds"]
    weather_response: WeatherResponse = weather_aggregator.sync_weather(cities)
    assert len(weather_response.results) == len(cities)
    # {} is set notation
    assert {result.city for result in weather_response.results} == set(cities)
    for result in weather_response.results:
        assert -100 < result.temperature < 100
    # assert all(-100 < result.temperature < 100 for result in weather_response.results)

def test_timing(weather_aggregator: WeatherAggregator) -> None:
    """ Test that checks the sync_weather timings"""
    cities: list[str] = ["Birmingham", "London", "Manchester"]
    weather_response: WeatherResponse = weather_aggregator.sync_weather(cities)
    cities_time = weather_response.total_time
    sum_response_time = sum(result.response_time for result in weather_response.results)
    assert abs(cities_time - sum_response_time) < 0.1
    print(
        f"Sync total time ({weather_response.total_time:.2f}s) should be very similar to"
        f"sum of individual times ({sum_response_time:.2f}s)"
    )

def test_empty_cities(weather_aggregator: WeatherAggregator) -> None:
    """ Test that checks the sync_weather function with an empty list of cities """
    with pytest.raises(ValueError, match="Cities list is empty"):
        cities: list[str] = []
        weather_aggregator.sync_weather(cities)

def test_invalid_city(weather_aggregator: WeatherAggregator) -> None:
    """ Test that checks the sync_weather function with an invalid city """
    with pytest.raises(ValueError, match="Invalid city name"):
        cities: list[str] = ["InvalidCity"]
        weather_aggregator.sync_weather(cities)
   
def test_non_string_input(weather_aggregator: WeatherAggregator) -> None:
    """ Test that checks the sync_weather function with a non-string input """
    with pytest.raises(TypeError, match="Cities must be strings"):
        cities: list[int] = [1, 2, 3]
        weather_aggregator.sync_weather(cities)
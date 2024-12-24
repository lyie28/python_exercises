from weather_aggregator.async_weather import AsyncWeatherAggregator
from weather_aggregator.models.models import WeatherResponse
import pytest

@pytest.fixture
def weather_aggregator() -> AsyncWeatherAggregator:
    return AsyncWeatherAggregator()

@pytest.mark.asyncio
async def test_basic(weather_aggregator: AsyncWeatherAggregator) -> None:
    """ Basic test that checks the async_weather function with a single city """
    cities: list[str] = ["Birmingham"]
    weather_response = await weather_aggregator.async_weather(cities)
    assert len(weather_response.results) == 1

@pytest.mark.asyncio
async def test_multiple_cities(weather_aggregator: AsyncWeatherAggregator) -> None:
    """ Test that checks the async_weather function with multiple cities """
    cities: list[str] = ["Birmingham", "London", "Manchester", "Liverpool", "Leeds"]
    weather_response = await weather_aggregator.async_weather(cities)
    assert len(weather_response.results) == len(cities)
    # {} is set notation
    assert {result.city for result in weather_response.results} == set(cities)

@pytest.mark.asyncio
async def test_timing(weather_aggregator: AsyncWeatherAggregator) -> None:
    """ Test that checks the aasync_weather timings"""
    cities: list[str] = ["Birmingham", "London", "Manchester"]
    weather_response = await weather_aggregator.async_weather(cities)
    cities_time = weather_response.total_time
    sum_response_time = sum(result.response_time for result in weather_response.results)
    assert cities_time < sum_response_time
    print(
        f"Async total time ({weather_response.total_time:.2f}s) should be less than "
        f"sum of individual times ({sum_response_time:.2f}s)"
    )

@pytest.mark.asyncio
async def test_empty_cities(weather_aggregator: AsyncWeatherAggregator) -> None:
    """ Test that checks the async_weather function with an empty list of cities """
    with pytest.raises(ValueError, match="Cities list is empty"):
        await weather_aggregator.async_weather([])

@pytest.mark.asyncio
async def test_invalid_city(weather_aggregator: AsyncWeatherAggregator) -> None:
    """ Test that checks the async_weather function with an invalid city """
    with pytest.raises(ValueError, match="Invalid city name"):
        cities: list[str] = ["InvalidCity"]
        await weather_aggregator.async_weather(cities)

@pytest.mark.asyncio
async def test_non_string_input(weather_aggregator: AsyncWeatherAggregator) -> None:
    """ Test that checks the async_weather function with a non-string input """
    with pytest.raises(TypeError, match="Cities must be strings"):
        cities: list[int] = [1, 2, 3]
        await weather_aggregator.async_weather(cities)
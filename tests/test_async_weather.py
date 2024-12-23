from weather_dashboard.weather_aggregator.async_weather import async_weather
from pydantic import BaseModel, Field
import pytest

class WeatherResult(BaseModel):
    city: str
    temperature: float = Field(gt=-100, lt=100)
    weather: str
    response_time: float = Field(gt=0)

class WeatherResponse(BaseModel):
    results: list[WeatherResult]
    total_time: float = Field(gt=0)

@pytest.mark.asyncio
async def test_basic() -> None:
    """ Basic test that checks the async_weather function with a single city """
    cities: list[str] = ["Birmingham"]
    results_list, total_time = await async_weather(cities)
    weather_response = WeatherResponse(results=results_list, total_time=total_time)
    assert len(results_list) == 1

@pytest.mark.asyncio
async def test_multiple_cities() -> None:
    """ Test that checks the async_weather function with multiple cities """
    cities: list[str] = ["Birmingham", "London", "Manchester", "Liverpool", "Leeds"]
    results_list, total_time = await async_weather(cities)
    weather_response = WeatherResponse(results=results_list, total_time=total_time)
    assert len(results_list) == len(cities)
    # {} is set notation
    assert {result.city for result in weather_response.results} == set(cities)

@pytest.mark.asyncio
async def test_timing() -> None:
    """ Test that checks the aasync_weather timings"""
    cities: list[str] = ["Birmingham", "London", "Manchester"]
    weather_response = await async_weather(cities)
    weather_response = WeatherResponse(results=weather_response, total_time=weather_response.total_time)
    cities_time = weather_response.total_time
    sum_response_time = sum(result.response_time for result in weather_response.results)
    assert cities_time < sum_response_time, (
        f"Async total time ({weather_response.total_time:.2f}s) should be less than "
        f"sum of individual times ({sum_response_time:.2f}s)"
    )

@pytest.mark.asyncio
async def test_empty_cities() -> None:
    """ Test that checks the async_weather function with an empty list of cities """
    with pytest.raises(ValueError, match="Cities list is empty"):
        await async_weather([])

@pytest.mark.asyncio
async def test_invalid_city() -> None:
    """ Test that checks the async_weather function with an invalid city """
    with pytest.raises(ValueError, match="Invalid city name"):
        cities: list[str] = ["InvalidCity"]
        await async_weather(cities)

@pytest.mark.asyncio
async def test_non_string_input() -> None:
    """ Test that checks the async_weather function with a non-string input """
    with pytest.raises(TypeError, match="Cities must be strings"):
        cities: list[int] = [1, 2, 3]
        await async_weather(cities)
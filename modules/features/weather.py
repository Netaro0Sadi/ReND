import requests
import re


WEATHER_CODES = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "cloudy",
    45: "fog",
    48: "fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    61: "light rain",
    63: "moderate rain",
    65: "heavy rain",
    80: "light showers",
    81: "moderate showers",
    82: "heavy showers",
    95: "thunderstorm"
}


def normalize_city(city):
    city = city.lower().strip()
    city = re.sub(r"[?!.]", "", city)

    replacements = {
        "londres": ("london", "GB"),
        "londres inglaterra": ("london", "GB"),
        "londres, inglaterra": ("london", "GB"),
        "london": ("london", "GB"),
        "paris": ("paris", "FR"),
        "roma": ("rome", "IT"),
        "lisboa": ("lisbon", "PT")
    }

    return replacements.get(city, (city, None))


def extract_city(message):

    message = message.lower().strip()

    message = re.sub(
        r"[?!.]",
        "",
        message
    )

    patterns = [

        r"weather in (.+)",
        r"weather of (.+)",

        r"temperature in (.+)",
        r"temperature of (.+)",

        r"climate in (.+)",
        r"climate of (.+)",

        r"clima em (.+)",
        r"clima de (.+)",
        r"clima (.+)",

        r"tempo em (.+)",
        r"tempo de (.+)",
        r"tempo (.+)",

        r"temperatura em (.+)",
        r"temperatura de (.+)",
        r"temperatura (.+)",

        r"quantos graus em (.+)",
        r"quantos graus faz em (.+)",

        r"e em (.+)",
        r"and in (.+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            message
        )

        if match:

            city = match.group(
                1
            ).strip()

            return normalize_city(
                city
            )

    return None, None


def get_coordinates(city, country_code=None):
    try:
        params = {
            "name": city,
            "count": 10,
            "language": "en",
            "format": "json"
        }

        if country_code:
            params["countryCode"] = country_code

        response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params=params,
            timeout=10
        )

        data = response.json()

        if "results" not in data:
            return None

        result = data["results"][0]

        return {
            "name": result.get("name"),
            "country": result.get("country"),
            "latitude": result.get("latitude"),
            "longitude": result.get("longitude")
        }

    except:
        return None


def get_weather_data(latitude, longitude):
    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "weather_code,"
                    "wind_speed_10m"
                )
            },
            timeout=10
        )

        data = response.json()

        return data.get("current")

    except:
        return None


def handle_weather(message):
    city, country_code = extract_city(message)

    if not city:
        return "Please tell me the city. Example: weather in Campinas."

    location = get_coordinates(city, country_code)

    if not location:
        return "I couldn't find that city."

    weather = get_weather_data(
        location["latitude"],
        location["longitude"]
    )

    if not weather:
        return "I couldn't access the weather data right now."

    temperature = weather.get("temperature_2m")
    humidity = weather.get("relative_humidity_2m")
    wind = weather.get("wind_speed_10m")
    code = weather.get("weather_code")

    condition = WEATHER_CODES.get(
        code,
        "unknown weather condition"
    )

    return (
        f"The weather in {location['name']}, "
        f"{location['country']} is {condition}. "
        f"Temperature: {temperature}°C. "
        f"Humidity: {humidity}%. "
        f"Wind speed: {wind} km/h."
    )
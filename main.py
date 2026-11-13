import os
from dotenv import load_dotenv
import requests

BASE_URL = "https://api.weatherapi.com/v1/current.json"

def request_data(city):
    api_key = os.getenv("API_KEY")

    if not api_key:
        raise ValueError("API_KEY not found. Check your .env file.")

    params = {
        "key": api_key,
        "q": city
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if "error" in data:
            raise ValueError(data["error"]["message"])

        return data

    except requests.exceptions.Timeout as err:
        raise RuntimeError("Request timed out. Try again.") from err

    except requests.exceptions.ConnectionError as err:
        raise RuntimeError(
            "Unable to connect. Check your internet connection."
        ) from err

    except requests.exceptions.HTTPError as err:
        raise RuntimeError("HTTP request failed. Check your API request.") from err

    except requests.exceptions.JSONDecodeError as err:
        raise RuntimeError("Unable to decode server response.") from err

    except requests.exceptions.RequestException as err:
        raise RuntimeError("Weather API request failed.") from err


def get_data(res):
    try:
        current = res["current"]
        condition = current["condition"]

        return (
            current["feelslike_c"],
            current["wind_kph"],
            current["humidity"],
            current["temp_c"],
            condition["text"]
        )

    except (KeyError, TypeError) as err:
        raise ValueError("Invalid weather data received from API.") from err


def feels_like(city, res):
    return f"Feels-like temperature in {city}: {res} Celsius"


def check_windspeed(city, res):
    return f"Wind speed in {city}: {res} kmph"


def check_humidity(city, res):
    return f"Humidity in {city}: {res}%"


def check_temperature(city, res):
    return f"Temperature in {city}: {res} Celsius"


def check_condition(city, res):
    return f"Weather condition in {city}: {res}"


def get_city():
    city = input("Enter the city: ").strip()

    if not city:
        raise ValueError("City name cannot be empty.")

    return city


def get_choice():
    try:
        return int(
            input(
                "\n1. Check humidity"
                "\n2. Check wind speed"
                "\n3. Check feels-like temperature"
                "\n4. Check temperature"
                "\n5. Check weather condition"
                "\n6. Exit"
                "\nEnter your choice: "
            )
        )
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None


def main():
    try:
        city = get_city()
        data = request_data(city)

        (
            f_temp,
            wind_speed,
            humidity,
            temperature,
            weather_condition
        ) = get_data(data)

        print(f"\nWeather information for {city}")

        while True:
            choice = get_choice()

            if choice is None:
                continue

            match choice:
                case 1:
                    print(check_humidity(city, humidity))

                case 2:
                    print(check_windspeed(city, wind_speed))

                case 3:
                    print(feels_like(city, f_temp))

                case 4:
                    print(check_temperature(city, temperature))

                case 5:
                    print(check_condition(city, weather_condition))

                case 6:
                    print("Exiting application...")
                    break

                case _:
                    print("Invalid choice. Select between 1-6.")

    except (ValueError, RuntimeError) as err:
        print("Error:", err)


if __name__ == "__main__":
    load_dotenv()
    main()

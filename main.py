import os
from dotenv import load_dotenv
import requests
import json

def request_data(city):
    api_key = os.getenv("API_KEY")
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data

def get_data(res):
    return (res["current"]["feelslike_c"], res["current"]["wind_kph"], res["current"]["humidity"], res["current"]["temp_c"], res["current"]["condition"]["text"])

def feels_like(city, res):
    return (f"feels like temperature of {city} is {res} Celcius")

def check_windspeed(city, res):
    return (f"wind speed in {city} is {res} kmph")

def check_humidity(city, res):
    return (f"humidity of {city} is {res}")

def check_temperature(city, res):
    return (f"temperature of {city} is {res} Celcius")

def check_condition(city, res):
    return (f"weather condition of {city} is {res}")


def main():
    choose = True
    city = input("enter the city: ")
    data = request_data(city)
    (f_temp, wind_speed, humidity, temperature, weather_condition) = get_data(data)
    while choose:
        choice = int(input("enter your choice: \n1 check the weather \n2 check the wind speed \n3 check the humidity \n4 check the temperature \n5 check the weather condition \n6 exit "))
        match(choice):
            case 1:
                print(feels_like(city, f_temp))
            case 2:
                print(check_windspeed(city, wind_speed))
            case 3:
                print(check_humidity(city, humidity))
            case 4:
                print(check_temperature(city, temperature))
            case 5:
                print(check_condition(city, weather_condition))
            case 6:
                choose = False
            case _:
                print("invalid choice")


if __name__ == "__main__":
    load_dotenv()
    main()
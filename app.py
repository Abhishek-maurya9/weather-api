
import streamlit as st
from dotenv import load_dotenv

from main import request_data, get_data


# Load environment variables
load_dotenv()


# ---------------- STREAMLIT CONFIGURATION ----------------

st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="centered"
)


# ---------------- APPLICATION UI ----------------

st.title("🌤️ Weather Dashboard")

st.write("Get real-time weather information for any city.")

st.divider()


# ---------------- CITY INPUT ----------------

with st.form("weather_form"):

    city = st.text_input(
        "Enter City Name",
        placeholder="Example: Delhi, London, Tokyo"
    ).strip()

    submitted = st.form_submit_button(
        "Get Weather",
        use_container_width=True
    )


# ---------------- FETCH WEATHER DATA ----------------

if submitted:

    if not city:
        st.warning("Please enter a city name.")

    else:
        try:
            with st.spinner("Fetching weather information..."):

                data = request_data(city)

                (
                    feels_like_temp,
                    wind_speed,
                    humidity,
                    temperature,
                    weather_condition
                ) = get_data(data)

                # Store weather information
                st.session_state.weather = {
                    "feels_like": feels_like_temp,
                    "wind_speed": wind_speed,
                    "humidity": humidity,
                    "temperature": temperature,
                    "condition": weather_condition
                }

                st.session_state.city = city

        except (ValueError, RuntimeError) as err:

            st.session_state.pop("weather", None)
            st.session_state.pop("city", None)

            st.error(str(err))


# ---------------- DISPLAY WEATHER INFORMATION ----------------

if "weather" in st.session_state:

    weather = st.session_state.weather
    city = st.session_state.city

    st.subheader(f"Weather in {city}")

    st.markdown(f"### {weather['condition']}")

    st.metric(
        label="Temperature",
        value=f"{weather['temperature']} °C"
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            label="Feels Like",
            value=f"{weather['feels_like']} °C"
        )

        st.metric(
            label="Humidity",
            value=f"{weather['humidity']}%"
        )

    with col2:

        st.metric(
            label="Wind Speed",
            value=f"{weather['wind_speed']} km/h"
        )

    st.divider()

    st.caption("Weather data provided by WeatherAPI.")

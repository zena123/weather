# Weather

fetch real-time weather data for multiple cities across the world

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Acknowledgements](#acknowledgements)

## Introduction
Django web application which can show the current weather for any city in a JSON API.
The user can enter the city for which he wants to know the current weather. This is done by interacting 
with the OpenWeatherMap API  https://openweathermap.org
## Features


- fetch weather data for a given city
- show result data in jason format

## Getting Started


### Prerequisites

- Python >= 3.8
- Django>=4.2,<4.3
- djangorestframework

### Installation

install via docker with one command : sudo docker compose up

## Usage
- Clone this repository to your local machine

- **Configure OpenWeatherMap API Key:**
   - Open `settings.py` .
   - Replace the placeholder value for `OPEN_WEATHER_API_KEY` with your valid OpenWeatherMap API key.
- run: 
  ```bash
     sudo docker compose up
     ``` 
- The project will be accessible at [http://localhost:8000/]
- **Fetch Weather Data:**
   - Open your web browser and navigate to [http://localhost:8000/core/weather/london/](http://localhost:8000/core/weather/london/) (replace "london" with the desired city).
   - You should see JSON-formatted weather data for the specified city.
- 
8. **Run Tests:**
   - Run the included tests:

     ```bash
     python manage.py test
     ```
- Now you have the Django project set up locally, and you can explore weather data for different cities via the provided API endpoints.

## Acknowledgements

- **OpenWeatherMap:** providing the OpenWeatherMap API, allowing to fetch real-time weather data for various cities around the world.

- **Django:**  robust and flexible web framework that simplifies the development of web applications.

- **Django Rest Framework:** making it easy to build RESTful APIs in Django.

- **Aiohttp and asyncio:** using asynchronous features of Aiohttp and asyncio.

- **Docker:** the project utilizes Docker for containerization and simplifying deployment.

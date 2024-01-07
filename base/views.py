from django.shortcuts import render
import requests
import json

# Create your views here.
def getWeather(city):
    baseUrl = "https://api.openweathermap.org/data/2.5/weather?&lang=es"
    apiKey = "43821be4a398a30aa611c403d557cfd3"
    parameters = {
        'q': city,
        'appid':apiKey,
        'units':'metric'
    }
    response = requests.get(baseUrl, params = parameters)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def traducir(weather):
    traducciones = {
        'Clouds': 'Nubes',
        'Clear': 'Despejado',
        'Rain': 'Lluvia',
        'Snow': 'Nieve',
        'Thunderstorm': 'Tormenta',
        'Tornado': 'Tornado',
        'Ash': 'Ceniza',
        'Dust': 'Polvo',
        'Sand': 'Arena',
        'Fog': 'Niebla',
        'Smoke': 'Humo',
        'Haze': 'Bruma',
        'Mist': 'Neblina',
        'Drizzle': 'Llovizna'
    }
    return(traducciones.get(weather))

def home(request):
    city = request.GET.get('city')
    iconUrl = 'https://openweathermap.org/img/wn/10d@2x.png'

    if not city:
        city="getafe"
        
    if city:
        weatherDataResult = getWeather(city)

        if weatherDataResult is not None:
            iconId = weatherDataResult['weather'][0]['icon']
            iconUrl = f"https://openweathermap.org/img/wn/{iconId}@2x.png"
            weatherData = json.dumps(weatherDataResult, indent=4)
            print(weatherData)

            # Extract values for display
            weather = weatherDataResult['weather'][0]['main']
            weatherDescription = weatherDataResult['weather'][0]['description']
            city = weatherDataResult['name']
            country = weatherDataResult['sys']['country']
            windSpeed = weatherDataResult['wind']['speed']
            pressure = weatherDataResult['main']['pressure']
            humidity = weatherDataResult['main']['humidity']
            temperature = weatherDataResult['main']['temp']
            sensacionTerm = weatherDataResult['main']['feels_like']

            traduccionTiempo = traducir(weather)
        else:
            return render(request, 'noExiste.html')
            
    return render(request, 'index.html', {
        'iconUrl': iconUrl,
        'weather': traduccionTiempo,
        'weather_description': weatherDescription,
        'city': city,
        'country': country,
        'wind_speed': windSpeed,
        'pressure': pressure,
        'humidity': humidity,
        'temperature': temperature,
        'sensacion': sensacionTerm,
    })

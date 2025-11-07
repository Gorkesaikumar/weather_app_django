from django.shortcuts import render
from django.contrib import messages
from decouple import config
import requests
import datetime

def home(request):
    city = request.POST.get('city', 'indore')

    API_KEY = config('OPENWEATHER_KEY')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    params = {'units': 'metric'}

    try:
        data = requests.get(url, params=params).json()

        # if city not found
        if data.get("cod") != 200:
            raise ValueError("Invalid city")

        context = {
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'temp': data['main']['temp'],
            'day': datetime.date.today(),
            'city': city,
            'exception_occurred': False,
            'image_url': 'https://images.pexels.com/photos/1107717/pexels-photo-1107717.jpeg?auto=compress&cs=tinysrgb&w=1600'
        }

    except Exception:
        messages.error(request, 'City not found')

        context = {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': datetime.date.today(),
            'city': 'indore',
            'exception_occurred': True,
            'image_url': 'https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600'
        }

    return render(request, 'weatherapp/index.html', context)

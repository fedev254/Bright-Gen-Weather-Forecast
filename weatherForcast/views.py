from django.shortcuts import render
import requests
import datetime


# Create your views here.

def forcast(request):
    default_city = 'Bungoma'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=d48a8488df875a790872dfc3a21175a0'
    geo_url = 'https://api.openweathermap.org/geo/1.0/direct?q={}&limit=1&appid=d48a8488df875a790872dfc3a21175a0'

    if request.method == 'POST':
        city = request.POST.get('city', default_city)

    else:
        city = default_city
        

    #Fetch longitude and latitude
    geo_data = requests.get(geo_url.format(city)).json()
    if geo_data:
        longitude = "{:.2f}°{}".format(abs(geo_data[0]['lon']), 'E' if geo_data[0]['lon'] >= 0 else 'W')
        latitude = "{:.2f}°{}".format(abs(geo_data[0]['lat']), 'N' if geo_data[0]['lat'] >= 0 else 'S')
    else:
        return render(request, 'error.html', {'error_message': 'City Not Found.'})

    city_weather = requests.get(url.format(city)).json()
    # request the API data and convert the JSON to Python data types

    weather = {
        'city': city,
        'temperature': city_weather['main']['temp'],
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon'],
        'temperature_max': city_weather['main']['temp_max'],
        'temperature_min': city_weather['main']['temp_min'],
        'feelslike_weather': city_weather['main']['feels_like'],
        'wind': city_weather['wind']['speed'],
        'humidity': city_weather['main']['humidity']

    }

    v = 'https://api.openweathermap.org/data/2.5/forecast?q={}&&units=metric&appid=d48a8488df875a790872dfc3a21175a0'
    a = v.format(city)
    #Fetch forecast
    full = requests.get(a).json()

    day = datetime.datetime.today()
    today_date = int(day.strftime('%d'))

    forcast_data_list = {}

    for c in range(0, full['cnt']):
        date_var1 = full['list'][c]['dt_txt']
        date_time_obj1 = datetime.datetime.strptime(date_var1, '%Y-%m-%d %H:%M:%S')
        # print t
        if int(date_time_obj1.strftime('%d')) == today_date or int(date_time_obj1.strftime('%d')) == today_date + 1:
            # print(date_time_obj1.strftime('%d %a'))
            if int(date_time_obj1.strftime('%d')) == today_date + 1:
                today_date += 1
            forcast_data_list[today_date] = {}
            forcast_data_list[today_date]['day'] = date_time_obj1.strftime('%A')
            forcast_data_list[today_date]['date'] = date_time_obj1.strftime('%d %b, %Y')
            forcast_data_list[today_date]['time'] = date_time_obj1.strftime('%I:%M %p')
            forcast_data_list[today_date]['FeelsLike'] = full['list'][c]['main']['feels_like']

            forcast_data_list[today_date]['Wind'] = full['list'][c]['wind']['speed']
            forcast_data_list[today_date]['Humidity'] = full['list'][c]['main']['humidity']

            forcast_data_list[today_date]['temperature'] = full['list'][c]['main']['temp']
            forcast_data_list[today_date]['temperature_max'] = full['list'][c]['main']['temp_max']
            forcast_data_list[today_date]['temperature_min'] = full['list'][c]['main']['temp_min']

            forcast_data_list[today_date]['description'] = full['list'][c]['weather'][0]['description']
            forcast_data_list[today_date]['icon'] = full['list'][c]['weather'][0]['icon']

            today_date += 1
        else:
            pass

    context = {
        'city_weather': city_weather,
        'city': city,
        'longitude': longitude,
        'latitude': latitude,
        'weather': weather, 'forcast_data_list': forcast_data_list
    }

    return render(request, 'index.html', context)


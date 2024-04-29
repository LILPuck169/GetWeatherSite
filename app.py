import time
import requests
from plyer import notification
from flask import Flask, render_template, request

app = Flask(__name__)

# Замените на ваш API ключ от OpenWeather
API_KEY = 'e36350e02830b5e9ba90dc4198f8a1db'

weather_rus = {
    'Clouds': 'Облачно',
    'Rain': 'Дождь',
    'Snow': 'Снег',
    'Sunny': 'Солнечно',
    'Clear': 'Ясно'
}

# Список популярных городов России
POPULAR_CITIES = [
    'Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань',
    'Нижний Новгород', 'Челябинск', 'Самара', 'Омск', 'Ростов-на-Дону',
    'Уфа', 'Красноярск', 'Пермь', 'Воронеж', 'Волгоград', 'Краснодар',
    'Саратов', 'Тюмень', 'Тольятти', 'Ижевск'
]


def get_weather():
    # Ваш код для получения прогноза погоды, например, с использованием API
    # В данном примере я буду использовать сайт OpenWeatherMap
    api_key = 'e36350e02830b5e9ba90dc4198f8a1db'
    city = 'Moscow'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()

    weather_description = data['weather'][0]['description']
    temp = data['main']['temp']

    return f'Погода в {city}: {weather_description}, Температура: {temp}°C'


@app.route('/')
def index():
    return render_template('index.html', cities=POPULAR_CITIES)


@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    units = request.form['units']
    print(units)
    params = request.form.getlist('params')  # Получаем выбранные параметры

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_data = {
            'city': city,
        }

        if 'temperature' in params:
            weather_data['temperature'] = data['main']['temp']
        if 'wind_speed' in params:
            weather_data['wind_speed'] = data['wind']['speed']
        if 'wind_direction' in params:
            weather_data['wind_direction'] = data['wind']['deg']
        if 'humidity' in params:
            weather_data['humidity'] = data['main']['humidity']
        if 'pressure' in params:
            weather_data['pressure'] = data['main']['pressure']
        if 'cloudy' in params:
            weather_data['weather_main'] = weather_rus[data['weather'][0]['main']]
        if 'feels_like' in params:
            weather_data['feels_like'] = data['main']['feels_like']

        if len(weather_data) == 1:
            error_message = "change it please!"
            return render_template('error.html', error_message=error_message)

        return render_template('weather.html', weather_data=weather_data)
    else:
        error_msg = f'Ошибка: {data["message"]}'
        return render_template('error.html', error_msg=error_msg)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')


from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error = None

    if request.method == 'POST':
        city = request.form['city']
        api_key = '6e4307ee3cd392d2f6a7978c166982d8'  # Replace with your actual OpenWeatherMap API key
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            weather = {
                'city': city,
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon']
            }
        else:
            error = 'City not found or unable to retrieve weather data.'

    return render_template('index.html', weather=weather, error=error)

if __name__ == '__main__':
    app.run(debug=True)

import unittest
from app import app
import requests_mock

class WeatherAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @requests_mock.Mocker()
    def test_valid_city(self, mock):
        city = "London"
        api_key = '6e4307ee3cd392d2f6a7978c166982d8'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        
        mock_response = {
            "weather": [{"description": "clear sky", "icon": "01d"}],
            "main": {"temp": 15.0, "humidity": 56},
            "wind": {"speed": 4.6}
        }
        
        mock.get(url, json=mock_response)
        
        response = self.app.post('/', data=dict(city=city))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Weather in London', response.data)
        self.assertIn(b'Temperature: 15.0 \xc2\xb0C', response.data)
        self.assertIn(b'Humidity: 56%', response.data)
        self.assertIn(b'Wind Speed: 4.6 m/s', response.data)
        self.assertIn(b'Description: clear sky', response.data)

    @requests_mock.Mocker()
    def test_invalid_city(self, mock):
        city = "InvalidCity"
        api_key = '6e4307ee3cd392d2f6a7978c166982d8'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        
        mock.get(url, status_code=404, json={"cod": "404", "message": "city not found"})
        
        response = self.app.post('/', data=dict(city=city))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'City not found or unable to retrieve weather data.', response.data)

    
if __name__ == '__main__':
    unittest.main()

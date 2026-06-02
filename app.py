import os
import requests
from flask import Flask, jsonify, request
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

app = Flask(__name__)

# Leer API key desde .env
API_KEY = os.getenv('OPENWEATHER_API_KEY')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
PORT = int(os.getenv('PORT', 5000))

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'Weather API',
        'environment': FLASK_ENV,
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Weather API - OpenWeather',
        'environment': FLASK_ENV,
        'endpoints': {
            'GET /health': 'Health check',
            'GET /weather?city=London': 'Get weather by city',
            'GET /weather?lat=51.5&lon=-0.1': 'Get weather by coordinates',
            'POST /weather/multiple': 'Get weather for multiple cities'
        }
    }), 200

@app.route('/weather', methods=['GET'])
def get_weather():
    try:
        # Validar que tenemos API key
        if not API_KEY or API_KEY == 'demo':
            return jsonify({
                'error': 'API key not configured. Get one at openweathermap.org',
                'note': 'Set OPENWEATHER_API_KEY in .env file'
            }), 503
       
        city = request.args.get('city')
        lat = request.args.get('lat')
        lon = request.args.get('lon')
       
        if not city and not (lat and lon):
            return jsonify({
                'error': 'Provide city OR lat/lon parameters',
                'example': '/weather?city=London'
            }), 400
       
        base_url = 'https://api.openweathermap.org/data/2.5/weather'
       
        if city:
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'
            }
        else:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': API_KEY,
                'units': 'metric'
            }
       
        response = requests.get(base_url, params=params, timeout=5)
       
        if response.status_code == 401:
            return jsonify({
                'error': 'Invalid API key',
                'hint': 'Check your OPENWEATHER_API_KEY in .env'
            }), 401
       
        if response.status_code == 404:
            return jsonify({
                'error': 'City not found'
            }), 404
       
        if response.status_code != 200:
            return jsonify({
                'error': f'OpenWeather API error: {response.status_code}'
            }), response.status_code
       
        data = response.json()
       
        weather_data = {
            'city': data.get('name'),
            'country': data.get('sys', {}).get('country'),
            'temperature': data.get('main', {}).get('temp'),
            'feels_like': data.get('main', {}).get('feels_like'),
            'humidity': data.get('main', {}).get('humidity'),
            'pressure': data.get('main', {}).get('pressure'),
            'weather': data.get('weather', [{}])[0].get('main'),
            'description': data.get('weather', [{}])[0].get('description'),
            'wind_speed': data.get('wind', {}).get('speed'),
            'cloudiness': data.get('clouds', {}).get('all'),
            'timestamp': datetime.utcnow().isoformat()
        }
       
        return jsonify(weather_data), 200
   
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'OpenWeather API timeout'
        }), 504
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/weather/multiple', methods=['POST'])
def get_multiple_weather():
    try:
        # Validar que tenemos API key
        if not API_KEY or API_KEY == 'demo':
            return jsonify({
                'error': 'API key not configured'
            }), 503
       
        data = request.get_json()
        cities = data.get('cities', [])
       
        if not cities:
            return jsonify({
                'error': 'No cities provided',
                'example': '{"cities": ["London", "Paris", "Tokyo"]}'
            }), 400
       
        results = []
        base_url = 'https://api.openweathermap.org/data/2.5/weather'
       
        for city in cities:
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'
            }
           
            try:
                response = requests.get(base_url, params=params, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    results.append({
                        'city': data.get('name'),
                        'temperature': data.get('main', {}).get('temp'),
                        'weather': data.get('weather', [{}])[0].get('main'),
                        'status': 'success'
                    })
                else:
                    results.append({
                        'city': city,
                        'status': 'error',
                        'error': f'HTTP {response.status_code}'
                    })
            except Exception as e:
                results.append({
                    'city': city,
                    'status': 'error',
                    'error': str(e)
                })
       
        return jsonify({'results': results}), 200
   
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=FLASK_ENV == 'development', host='0.0.0.0', port=PORT)
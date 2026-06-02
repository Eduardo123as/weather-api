# Weather API

A simple and efficient Python-based Weather API that provides current weather information and forecasts. Built with Flask, this API integrates with external weather data sources to deliver real-time weather conditions.

## Features

- 🌤️ Real-time weather data
- 📍 Location-based queries
- 🔄 Multiple weather parameters (temperature, humidity, pressure, wind speed)
- 🐳 Docker support for easy deployment
- 📝 Environment-based configuration

## Requirements

- Python 3.7+
- Flask
- Requests library
- Environment variables configuration

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/Eduardo123as/weather-api.git
cd weather-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Docker Setup

Build and run using Docker:
```bash
docker build -t weather-api .
docker run -p 5000:5000 weather-api
```

## Configuration

Create a `.env` file based on `.env.example`:
```env
WEATHER_API_KEY=your_api_key_here
DEBUG=False
HOST=0.0.0.0
PORT=5000
```

## API Endpoints

### Get Current Weather
```
GET /weather?city=<city_name>
```

**Response Example:**
```json
{
  "city": "New York",
  "temperature": 72,
  "humidity": 65,
  "pressure": 1013,
  "wind_speed": 8,
  "condition": "Partly Cloudy"
}
```

## Project Structure

```
weather-api/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── .env.example       # Environment variables template
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

## Dependencies

See `requirements.txt` for a complete list of dependencies.

## Usage Examples

### Using Python Requests
```python
import requests

response = requests.get('http://localhost:5000/weather', params={'city': 'London'})
weather_data = response.json()
print(weather_data)
```

### Using cURL
```bash
curl "http://localhost:5000/weather?city=Paris"
```

## Error Handling

The API returns appropriate HTTP status codes:
- `200` - Successful request
- `400` - Bad request (missing or invalid parameters)
- `404` - City not found
- `500` - Server error

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Last Updated:** June 2, 2026

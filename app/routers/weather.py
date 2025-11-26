import os
import httpx 
from fastapi import Request, APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from dotenv import load_dotenv
load_dotenv()

# --- Configuration ---
# Use the Base URL provided in the API documentation
WEATHERAPI_BASE_URL = "http://api.weatherapi.com/v1"
WEATHERAPI_ENDPOINT = "/current.json" # For current weather data
DEFAULT_CITY = "London" 

templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/weather", response_class=HTMLResponse)
async def weather_home(request: Request, city: str = DEFAULT_CITY):
    # 1. Get the API Key from environment variables
    # The .env key name "weather" is used as per your previous snippet
    api_key = os.getenv("weather")
    
    if not api_key:
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "message": "Weather API key not configured in environment variables ('weather')."},
            status_code=500
        )

    # 2. Construct the full API URL
    full_url = f"{WEATHERAPI_BASE_URL}{WEATHERAPI_ENDPOINT}"

    # 3. Define query parameters: key (required) and q (query/location)
    params = {
        "key": api_key,
        "q": city,
        # The API documentation implies 'units' are handled by default fields (temp_c, temp_f)
    }

    # 4. Make the asynchronous API call using httpx
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(full_url, params=params)
            response.raise_for_status() # Raise exception for bad status codes (4xx/5xx)
            raw_data = response.json()
            
            # --- 5. Extract and process the data from the WeatherAPI.com JSON structure ---
            
            # Check for API error structure (e.g., 400 Bad Request for invalid city)
            if 'error' in raw_data:
                error_detail = raw_data['error']['message']
                # WeatherAPI returns 400 for bad queries, we can reflect that status
                raise HTTPException(status_code=400, detail=f"Weather API Error: {error_detail}")

            # Extract data from the 'location' and 'current' objects
            location = raw_data['location']
            current = raw_data['current']

            weather_data = {
                "city_name": location.get('name', city),
                "region": location.get('region'),
                "country": location.get('country'),
                "temperature_c": current.get('temp_c'), # Temperature in Celsius
                "temperature_f": current.get('temp_f'), # Temperature in Fahrenheit
                "description": current['condition']['text'],
                "icon": current['condition']['icon'], # Path to the weather icon
            }
            
            # 6. Render the template with the fetched data
            return templates.TemplateResponse(
                "weather.html", 
                {"request": request, "weather": weather_data}
            )

    except httpx.HTTPStatusError as e:
        # Handle network or HTTP errors (e.g., 404, 500 from the external API or network issues)
        error_message = f"External API or Network Error: {e.response.status_code} - {e.response.text}"
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "message": error_message},
            status_code=e.response.status_code
        )

    except HTTPException as e:
        # Handle the specific 400 API error raised inside the try block
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "message": e.detail},
            status_code=e.status_code
        )
        
    except Exception as e:
        # Handle general errors (e.g., parsing JSON)
        error_message = f"An unexpected internal error occurred: {e}"
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "message": error_message},
            status_code=500
        )
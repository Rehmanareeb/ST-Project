from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)


def test_home():
    response = client.get(
        "/", headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Welcome to FastAPI Website Starter Demo" in response.content
    response = client.get("/static/css/style3.css")
    assert response.status_code == 200


def test_page_about():
    response = client.get("/page/about",
                          headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"About" in response.content


def test_unsplash():
    response = client.get("/unsplash",
                          headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Unsplash Finder" in response.content


def test_two_forms():
    response = client.get("/twoforms",
                          headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Two Forms" in response.content


def test_accordion():
    response = client.post("/accordion", data={"tag": "flower"}, headers={
                           "Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    assert b"Accordion" in response.content


def test_page_contact():
    response = client.get("/page/contact",
                          headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Contact" in response.content


def test_page_home():
    response = client.get("/page/home",
                          headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Home" in response.content


def test_page_info():
    response = client.get("/page/info",
                          headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Information" in response.content


def test_page_portfolio():
    response = client.get("/page/portfolio",
                          headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Portfolio" in response.content


def test_unsplash_key():
    response = client.get("/unsplash",
                          headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Unsplash Finder" in response.content
    # Check if the Unsplash key is being loaded correctly
    assert b"key" in response.content


def test_weather_default_city():
    response = client.get("/weather")
    assert response.status_code == 200
    assert b"London" in response.content  # Default city is London
    assert b"temperature_c" in response.content or b"temperature_f" in response.content


def test_weather_specific_city():
    response = client.get("/weather?city=New York")
    assert response.status_code == 200
    assert b"New York" in response.content
    assert b"temperature_c" in response.content or b"temperature_f" in response.content


def test_weather_invalid_city():
    response = client.get("/weather?city=InvalidCityName")
    assert response.status_code == 400  # Bad Request for invalid city
    assert b"Weather API Error" in response.content


def test_weather_missing_api_key():
    # Temporarily unset the API key for this test
    os.environ["weather"] = ""
    response = client.get("/weather")
    assert response.status_code == 500  # Internal Server Error for missing API key
    assert b"Weather API key not configured" in response.content
    # Restore the API key after the test
    os.environ["weather"] = "your_actual_api_key_here"


def test_weather_network_error(mocker):
    # Simulate a network error using mocker
    mocker.patch("httpx.AsyncClient.get", side_effect=Exception("Network Error"))
    response = client.get("/weather")
    assert response.status_code == 500
    assert b"An unexpected internal error occurred" in response.content


def test_weather_london():
    response = client.get("/weather?city=London")
    assert response.status_code == 200
    assert b"London" in response.content  # Check if the city name is in the response
    assert b"temperature_c" in response.content or b"temperature_f" in response.content


def test_weather_new_york():
    response = client.get("/weather?city=New York")
    assert response.status_code == 200
    assert b"New York" in response.content  # Check if the city name is in the response
    assert b"temperature_c" in response.content or b"temperature_f" in response.content


def test_weather_tokyo():
    response = client.get("/weather?city=Tokyo")
    assert response.status_code == 200
    assert b"Tokyo" in response.content  # Check if the city name is in the response
    assert b"temperature_c" in response.content or b"temperature_f" in response.content


def test_weather_sydney():
    response = client.get("/weather?city=Sydney")
    assert response.status_code == 200
    assert b"Sydney" in response.content  # Check if the city name is in the response
    assert b"temperature_c" in response.content or b"temperature_f" in response.content


def test_weather_mumbai():
    response = client.get("/weather?city=Mumbai")
    assert response.status_code == 200
    assert b"Mumbai" in response.content  # Check if the city name is in the response
    assert b"temperature_c" in response.content or b"temperature_f" in response.content


def test_form1_value_1():
    response = client.post("/form1", data={"number": 1}, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    assert b"3" in response.content  # 1 + 2 = 3


def test_form1_value_10():
    response = client.post("/form1", data={"number": 10}, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    assert b"12" in response.content  # 10 + 2 = 12


def test_form1_value_50():
    response = client.post("/form1", data={"number": 50}, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    assert b"52" in response.content  # 50 + 2 = 52


def test_form1_value_100():
    response = client.post("/form1", data={"number": 100}, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    assert b"102" in response.content  # 100 + 2 = 102


def test_form1_value_200():
    response = client.post("/form1", data={"number": 200}, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    assert b"202" in response.content  # 200 + 2 = 202


def test_form2_value_1():
    response = client.post("/form2", data={"number": 1}, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    assert b"101" in response.content  # 1 + 100 = 101


def test_form2_value_10():
    response = client.post("/form2", data={"number": 10}, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    assert b"110" in response.content  # 10 + 100 = 110


def test_form2_value_50():
    response = client.post("/form2", data={"number": 50}, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    assert b"150" in response.content  # 50 + 100 = 150


def test_form2_value_100():
    response = client.post("/form2", data={"number": 100}, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    assert b"200" in response.content  # 100 + 100 = 200


def test_form2_value_200():
    response = client.post("/form2", data={"number": 200}, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    assert b"300" in response.content  # 200 + 100 = 300

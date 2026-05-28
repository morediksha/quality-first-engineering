import requests
import json
from playwright.sync_api import sync_playwright

def test_get_api_requests():

    url = 'https://reqres.in'
    API_KEY = 'free_user_3DXHR1WCnUfNlbduOW1b9bRwpDt'
    headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-api-key": API_KEY
    }
    response = requests.get(url, API_KEY, headers=headers)
    print("Response: ", response)
    assert response.status_code == 200
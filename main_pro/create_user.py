import requests
import json

url = "http://127.0.0.1:8000/api/maintenance/register/"
data = {
    "username": "user_test",
    "password": "bypass12",
    "email": "test@example.com",
    "role": "support_video",
    "telephone": "0123456789"
}
response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
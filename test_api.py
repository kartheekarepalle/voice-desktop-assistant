import requests

url = "https://voice-desktop-assistant.vercel.app/api/command?text=what%27s%20the%20time"
response = requests.get(url)
print("Status Code:", response.status_code)
print("Response:", response.json())

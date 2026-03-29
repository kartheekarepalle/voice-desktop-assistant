import sys
sys.path.insert(0, '/c:/Users/karth.AMMULU/projects/voice-desktop-assistant')

from api.index import app

# Test the home route
with app.test_client() as client:
    response = client.get('/')
    print("Status Code:", response.status_code)
    print("Content-Type:", response.content_type)
    print("Is HTML:", b'<!DOCTYPE' in response.data)
    print("First 200 bytes:", response.data[:200])

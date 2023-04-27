import requests

headers = {'Authorization': 'Token 3225005c531262c6c646021638371075ded1a494'}
response = requests.get('http://127.0.0.1:8000/api/v1/events/', headers=headers)
print(response.json())
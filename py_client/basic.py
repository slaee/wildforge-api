import requests

endpoint = "http://localhost:8000/api/classes/2"

get_response = requests.delete(endpoint)
print(get_response.json())
import requests

url = "http://localhost:9696/predict"

client = {
    "lead_source": "organic_search",
    "number_of_courses_viewed": 4,
    "annual_income": 80304.0
}

response = requests.post(url, json=client)
prediction = response.json()

print(prediction)
if prediction['lead conversion']:
    print(f'This lead is LIKELY to convert, probability={prediction['lead conversion probability']}')
else:
    print(f'This lead is NOT LIKELY to convert, probability={prediction['lead conversion probability']}')
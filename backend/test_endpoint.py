import requests
import json

url = "http://127.0.0.1:8000/api/v1/ai/ask"

payload = {
    "question": "How many students are there?"
}

print(f"📡 Testing Endpoint: {url}")
try:
    response = requests.post(url, json=payload)
    print(f"🔄 Status Code: {response.status_code}")
    print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"❌ Error: {e}")

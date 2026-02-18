import requests
import json

BASE_URL = "http://localhost:8000/api/v1/ai/ask"
USER_ID = "35"
USER_ROLE = 7

def test_query(question):
    payload = {
        "question": question,
        "user_id": USER_ID,
        "user_role": USER_ROLE,
        "model": "deepseek-chat"
    }
    print(f"\nTESTING: {question}")
    response = requests.post(BASE_URL, json=payload)
    if response.status_code == 200:
        print(f"ANSWER: {response.json().get('answer')[:200]}...")
        if response.json().get('sql'):
            print(f"SQL: {response.json().get('sql')}")
    else:
        print(f"FAILED: {response.status_code} - {response.text}")

# Test 1: Marketplace (The most complex hierarchy logic)
test_query("List all available marketplace courses.")

# Test 2: Own Results
test_query("Show my latest coding question scores.")

# Test 3: Allocation
test_query("Who are the trainers allocated to my section?")

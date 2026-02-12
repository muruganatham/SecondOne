"""
Test script to verify the AI pre-analysis feature
"""
import requests
import json

# Your auth token (replace with a valid one)
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoJpaGFyYW4uYW4uMjNAc3JlYy5hYy5pbiIsImV4cCI6MTczOTI1MjAxNn0.rXrMNTAzMkU4NzQ3OTQzNjE2ODU4NzE2ODU4NzE2ODU4"

BASE_URL = "http://localhost:8000/api/v1/ai"

def test_query(question):
    """Test a query and print the results"""
    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"{'='*60}")
    
    response = requests.post(
        f"{BASE_URL}/ask",
        headers={
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "question": question,
            "model": "deepseek-chat"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Answer: {data.get('answer', 'N/A')}")
        print(f"\n📝 SQL: {data.get('sql', 'N/A')}")
        print(f"\n📊 Data Rows: {len(data.get('data', []))}")
        if data.get('follow_ups'):
            print(f"\n💡 Follow-ups: {', '.join(data['follow_ups'])}")
    else:
        print(f"\n❌ Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    # Test 1: Question that might use non-existent tables
    test_query("how many assessments so far i done?")
    
    # Test 2: Ask about available tables
    test_query("What tables are available?")
    
    # Test 3: Simple query
    test_query("show me all courses")

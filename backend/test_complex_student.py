import requests
import json
import os

# Configuration
API_URL = "http://127.0.0.1:8005/api/v1/ai/ask"
USER_ID = 35
USER_ROLE = 7  # Student

def test_complex_query(question):
    print(f"\n--- Testing Complex Question: '{question}' for User ID: {USER_ID} ---")
    
    payload = {
        "question": question,
        "user_id": USER_ID,
        "user_role": USER_ROLE,
        "model": "deepseek-chat"
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        print("\n--- AI RESPONSE ---")
        print(f"Answer: {result.get('answer')}")
        
        if result.get('sql'):
            print(f"\n--- GENERATED SQL ---\n{result.get('sql')}")
        
        if result.get('data'):
            print("\n--- DATA PREVIEW ---")
            print(json.dumps(result.get('data')[:3], indent=2))
            
        with open("test_complex_student_result.txt", "w", encoding="utf-8") as f:
            f.write(f"Question: {question}\n")
            f.write(f"Answer: {result.get('answer')}\n")
            if result.get('sql'):
                f.write(f"SQL: {result.get('sql')}\n")
            
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # A query requiring: user_academics -> batches -> course_wise_segregations -> courses
    query = "Show my current rank and average score for all my courses, and how do I compare to others in my batch?"
    test_complex_query(query)

import os
import requests
import json

def test_retell_agent_creation():
    """
    Test creating an agent using the Retell provider
    """
    url = "https://api.retellai.com/create-agent"
    
    # Payload for creating the agent
    payload = {
        "response_engine": {
            "llm_id": "llm_4b0b0e1268d8b6782562ccc78ccc",
            "type": "retell-llm"
        },
        "voice_id": "11labs-Adrian",
        "agent_name": "Rohith"
    }
    
    # Include Authorization header for API authentication
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY"  # Replace YOUR_API_KEY with your actual API key
    }
    
    # Sending the POST request to the Retell API
    response = requests.post(url, json=payload, headers=headers)
    
    # Print the status code and the response body
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    # Check if the agent creation was successful
    if response.status_code == 200:
        print("✅ Retell agent created successfully!")
    else:
        print("❌ Failed to create Retell agent")
    
    return response.json()

if __name__ == "__main__":
    test_retell_agent_creation()

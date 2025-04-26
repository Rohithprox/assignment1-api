import os
import requests
import json

def test_vapi_agent_creation():
    """
    Test creating an agent using the VAPI provider
    """
    # Corrected API URL
    url = "https://api.vapi.ai/assistant"
    
    # The payload to create the agent
    payload = {
        "name": "Rohith",
        "voice": {
            "provider": "azure",
            "voiceId": "andrew"
        },
        "model": {
            "provider": "anyscale",
            "model": ""
        },
        "voicemailDetection": {
            "provider": "google",
            "voicemailExpectedDurationSeconds": 25
        }
    }
    
    # Adding Authorization header
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer d3d1b191-841d-4d8e-8d4b-f609fdb79502"  # Your API key
    }
    
    # Sending the POST request to the API
    response = requests.post(url, json=payload, headers=headers)
    
    # Printing the status code and response
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    # Handling response based on status code
    if response.status_code == 200:
        print("✅ Vapi agent created successfully!")
    else:
        print("❌ Failed to create Vapi agent")
    
    return response.json()

if __name__ == "__main__":
    test_vapi_agent_creation()

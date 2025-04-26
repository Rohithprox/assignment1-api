# Unified Agent API 
Overview

The **Unified Agent API** is a powerful and flexible solution to create and manage AI agents across two popular platforms: **Vapi** and **Retell**. By providing a unified interface, this API simplifies the creation process of agents with customizable parameters like voice, models, and webhooks.

Whether you are building a customer service assistant, a virtual agent for your business, or any other AI-powered solution, the Unified Agent API offers a seamless way to manage everything from a single endpoint.

---

##  Key Features

- **Single Interface for Multiple Providers**: Create agents for both **Vapi** and **Retell** with just one API. 
- **Customizable Agent Parameters**: Configure the agent's voice, model, description, and additional parameters.
- **Asynchronous Operation**: Non-blocking, fast agent creation with FastAPI and HTTPX. 
- **Easy Integration**: Simple API calls that fit seamlessly into your existing systems. 
- **Error Handling & Debugging**: Detailed error messages make it easy to track issues and fix them. 

---

## ⚙️ Technologies Used

- **FastAPI**: For building the fast and modern web API. 
- **HTTPX**: Async HTTP requests for fast, non-blocking interactions. 
- **Python 3.x**: The core language driving the application. 
- **Pydantic**: For automatic data validation and serialization. 

---

##  Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Rohithprox/assignment1-api
2. Install Dependencies
Create a virtual environment and install the necessary Python packages:


cd unified-agent-api
pip install -r requirements.txt

3. Set Up Your Environment Variables
You will need to set up two environment variables for your API keys:

VAPI_API_KEY: Your Vapi API key 

RETELL_API_KEY: Your Retell API key 

For local development, you can set them in .env or directly in your terminal session:

bash
Copy
Edit
export VAPI_API_KEY="your_vapi_key"
export RETELL_API_KEY="your_retell_key"
4. Run the API
Start the FastAPI app with:
uvicorn main:app --reload
Now you can access the API at http://localhost:8000.

 API Endpoints
POST /create-agent
Create an agent on Vapi or Retell by sending the following JSON payload:

json

{
  "provider": "vapi",  // or "retell"
  "name": "Agent Name",
  "description": "Optional description for the agent",
  "voice_id": "optional_voice_id",
  "model": "optional_model",
  "instructions": "optional_instructions"
}
provider: The provider for the agent (vapi or retell). 🌐

name: Name of the agent. 🏷️

description: (Optional) Description of the agent. ✏️

voice_id: (Optional) Voice ID for the agent's voice (if supported by the provider). 🎤

model: (Optional) The model you want to use (e.g., GPT-4, etc.). 🧠

instructions: (Optional) Custom instructions for the agent. 📜

GET /
A simple welcome endpoint to test the API and see instructions. 🏠

🔧 Example Usage
Create an agent by sending a POST request to /create-agent with the required parameters.

You'll receive a response indicating success or failure, along with additional details.

Example Request:


curl -X POST http://localhost:8000/create-agent \
     -H "Content-Type: application/json" \
     -d '{
           "provider": "vapi",
           "name": "Rohith",
           "description": "A smart agent for customer service",
           "voice_id": "andrew",
           "model": "gpt-4",
           "instructions": "Handle customer queries effectively"
         }'
🌍 Deploy to Production
If you want to deploy the Unified Agent API to production, we recommend using services like Heroku, AWS Lambda, or DigitalOcean. Just make sure to configure your environment variables and you're good to go! ☁️

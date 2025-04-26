# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from enum import Enum
import httpx
import os
from typing import Optional, List, Dict, Any, Union
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Unified Agent API", 
              description="A common wrapper for Vapi and Retell agent creation APIs")

class Provider(str, Enum):
    VAPI = "vapi"
    RETELL = "retell"

class CreateAgentRequest(BaseModel):
    # Common parameters
    provider: Provider
    name: str
    description: Optional[str] = None
    
    # Voice parameters
    voice_type: Optional[str] = None
    voice_id: Optional[str] = None
    
    # Model parameters
    model: Optional[str] = None
    instructions: Optional[str] = None
    
    # Other parameters that might be specific to one provider
    webhook_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    # Provider-specific parameters can be passed directly
    provider_specific_params: Optional[Dict[str, Any]] = Field(default_factory=dict)

@app.post("/create-agent")
async def create_agent(request: CreateAgentRequest):
    """
    Create an agent on either Vapi or Retell based on the provider parameter.
    Returns the API response from the selected provider.
    """
    if request.provider == Provider.VAPI:
        return await create_vapi_agent(request)
    elif request.provider == Provider.RETELL:
        return await create_retell_agent(request)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported provider: {request.provider}")

async def create_vapi_agent(request: CreateAgentRequest):
    """
    Create an assistant using Vapi's API
    """
    # Get Vapi API key from environment variable
    api_key = os.environ.get("VAPI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="VAPI_API_KEY environment variable not set")
    
    # Map common parameters to Vapi-specific format
    vapi_payload = {
        "name": request.name,
        "model": request.model or "gpt-4",  # Default to GPT-4 if not specified
    }
    
    # Add optional parameters if provided
    if request.description:
        vapi_payload["description"] = request.description
    
    if request.instructions:
        vapi_payload["instructions"] = request.instructions
    
    if request.voice_id:
        vapi_payload["voice"] = {
            "provider": "openai",  # Default provider, can be overridden in provider_specific_params
            "voice_id": request.voice_id
        }
    
    if request.webhook_url:
        vapi_payload["webhook_url"] = request.webhook_url
    
    if request.metadata:
        vapi_payload["metadata"] = request.metadata
    
    # Add any provider-specific parameters
    vapi_payload.update(request.provider_specific_params)
    
    logger.info(f"Creating Vapi assistant with payload: {vapi_payload}")
    
    # Call Vapi API
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.vapi.ai/assistants",
            json=vapi_payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        )
        
        if response.status_code >= 400:
            logger.error(f"Vapi API error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Vapi API error: {response.text}"
            )
        
        return {
            "provider": "vapi",
            "response": response.json(),
            "status": "success"
        }

async def create_retell_agent(request: CreateAgentRequest):
    """
    Create an agent using Retell's API
    """
    # Get Retell API key from environment variable
    api_key = os.environ.get("RETELL_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="RETELL_API_KEY environment variable not set")
    
    # Map common parameters to Retell-specific format
    retell_payload = {
        "name": request.name,
    }
    
    # Map voice parameters
    if request.voice_type or request.voice_id:
        retell_payload["voice_id"] = request.voice_id
        retell_payload["voice_type"] = request.voice_type or "eleven_labs"  # Default to ElevenLabs
    
    # Add description as a Retell llm_webhook param if provided
    if request.description:
        if "llm_webhook" not in retell_payload:
            retell_payload["llm_webhook"] = {}
        retell_payload["llm_webhook"]["system_prompt"] = request.description
    
    # Map instructions to Retell format
    if request.instructions:
        if "llm_webhook" not in retell_payload:
            retell_payload["llm_webhook"] = {}
        retell_payload["llm_webhook"]["instructions"] = request.instructions
    
    # Add model if provided
    if request.model:
        if "llm_webhook" not in retell_payload:
            retell_payload["llm_webhook"] = {}
        retell_payload["llm_webhook"]["model"] = request.model
    
    # Add webhook URL if provided
    if request.webhook_url:
        retell_payload["webhook_url"] = request.webhook_url
    
    # Add metadata if provided
    if request.metadata:
        retell_payload["metadata"] = request.metadata
    
    # Add any provider-specific parameters
    retell_payload.update(request.provider_specific_params)
    
    logger.info(f"Creating Retell agent with payload: {retell_payload}")
    
    # Call Retell API
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.retellai.com/agents",
            json=retell_payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        )
        
        if response.status_code >= 400:
            logger.error(f"Retell API error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Retell API error: {response.text}"
            )
        
        return {
            "provider": "retell",
            "response": response.json(),
            "status": "success"
        }

@app.get("/")
async def root():
    return {"message": "Welcome to the Unified Agent API. Use /create-agent to create agents on Vapi or Retell."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
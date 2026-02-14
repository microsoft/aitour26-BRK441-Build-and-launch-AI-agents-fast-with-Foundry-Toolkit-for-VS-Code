# http://localhost:8000

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import json
import asyncio
from typing import List, Dict, Optional
import logging
import base64
import os
import sys
from contextlib import AsyncExitStack
import uuid
from pathlib import Path

# Resolve shared asset paths relative to this file (web_app.py)
BASE_SRC_DIR = Path(__file__).resolve().parents[2]  # -> /workspace/src
SHARED_STATIC_DIR = BASE_SRC_DIR / "shared" / "static"

# Use shared/static when present; fall back to project-root static/templates
STATIC_DIR = SHARED_STATIC_DIR if SHARED_STATIC_DIR.exists() else Path("static")
TEMPLATES_DIR = STATIC_DIR if STATIC_DIR.exists() else Path("templates")

# Agent Framework imports
from agent_framework import RawAgent, MCPStdioTool, Message, Content
from agent_framework.azure import AzureAIClient
from azure.identity.aio import DefaultAzureCredential


from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into os.environ

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def encodeImage(path, mime_type):
    """Encode image file to base64 for use with AI models"""
    with open(path, "rb") as image:
        encoded = base64.b64encode(image.read())
    return f"data:{mime_type};base64,{encoded.decode()}"

def get_image_mime_type(filename: str) -> str:
    """Get MIME type based on file extension"""
    extension = filename.lower().split('.')[-1]
    mime_types = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp',
        'bmp': 'image/bmp'
    }
    return mime_types.get(extension, 'image/jpeg')

# Agent Framework Configuration - matching cora-agent-demo.py
ENDPOINT = os.environ.get("AZURE_AI_FOUNDRY_ENDPOINT", "your_foundry_endpoint_here")
MODEL_DEPLOYMENT_NAME = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4.1-mini")
AGENT_NAME = "cora-web-agent"
MCP_PYTHON_COMMAND = os.environ.get("MCP_PYTHON_COMMAND", sys.executable)

def create_mcp_tools() -> list[MCPStdioTool]:
    """Create MCP tools for the agent"""
    return [
        MCPStdioTool(
            name="zava_customer_sales_stdio",
            description="MCP server for Zava customer sales analysis",
            command=MCP_PYTHON_COMMAND,
            args=[
                "/workspace/src/python/mcp_server/customer_sales/customer_sales.py",
                "--stdio",
                "--RLS_USER_ID=00000000-0000-0000-0000-000000000000",
            ]
        ),
    ]

app = FastAPI(title="AI Agent Chat Demo", version="1.0.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Global agent instance and session storage
agent_instance = None
credential_instance = None
agent_sessions = {}  # Store sessions per session ID

# Agent instructions for Cora AI assistant
AGENT_INSTRUCTIONS = """You are Cora, an intelligent and friendly AI assistant for Zava, a home improvement brand. You help customers with their DIY projects by understanding their needs and recommending the most suitable products from Zava's catalog.

Your role is to:
- Engage with the customer in natural conversation to understand their DIY goals.
- Ask thoughtful questions to gather relevant project details.
- Be brief in your responses.
- Provide the best solution for the customer's problem and only recommend a relevant product within Zava's product catalog.
- Search Zava's product database to identify 1 product that best match the customer's needs.
- Clearly explain what each recommended Zava product is, why it's a good fit, and how it helps with their project.
- When users provide images, analyze them carefully to understand what they show and how it relates to their DIY project.

Your personality is:
- Warm and welcoming, like a helpful store associate
- Professional and knowledgeable, like a seasoned DIY expert
- Curious and conversational—never assume, always clarify
- Transparent and honest—if something isn't available, offer support anyway

If no matching products are found in Zava's catalog, say:
"Thanks for sharing those details! I've searched our catalog, but it looks like we don't currently have a product that fits your exact needs. If you'd like, I can suggest some alternatives or help you adjust your project requirements to see if something similar might work."
"""

async def initialize_agent():
    """Initialize the Agent Framework agent using AzureAIClient"""
    global agent_instance, credential_instance
    if agent_instance is None:
        try:
            # Use DefaultAzureCredential for better token refresh handling
            credential_instance = DefaultAzureCredential()
            await credential_instance.__aenter__()
            
            # Create AzureAIClient for Foundry project endpoint
            client = AzureAIClient(
                project_endpoint=ENDPOINT,
                model_deployment_name=MODEL_DEPLOYMENT_NAME,
                credential=credential_instance,
                agent_name=AGENT_NAME,
            )
            
            # Create agent with the Azure AI client using as_agent()
            agent_instance = client.as_agent(
                name=AGENT_NAME,
                instructions=AGENT_INSTRUCTIONS,
                tools=[
                    *create_mcp_tools(),
                ],
            )
            logger.info("Agent Framework initialized successfully with AzureAIClient")
        except Exception as e:
            logger.error(f"Failed to initialize Agent Framework: {e}")
            import traceback
            traceback.print_exc()
            agent_instance = None

# Store active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """Handle image upload"""
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            return {"error": "Please upload a valid image file"}
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Save file
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Return file URL
        file_url = f"/uploads/{unique_filename}"
        
        logger.info(f"Image uploaded: {file_url}")
        return {"success": True, "file_url": file_url, "filename": unique_filename}
        
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        return {"error": f"Upload failed: {str(e)}"}

@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    """Serve the main chat interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AI Agent Chat Demo"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_message = message_data.get("message", "")
            image_url = message_data.get("image_url")  # Optional image URL
            
            logger.info(f"Received message: {user_message}")
            if image_url:
                logger.info(f"With image: {image_url}")
            
            # Process message with AI agent
            ai_response = await simulate_ai_agent(user_message, image_url)
            
            # Send response back to client
            response_data = {
                "type": "ai_response",
                "message": ai_response,
                "timestamp": asyncio.get_event_loop().time()
            }
            
            await manager.send_personal_message(json.dumps(response_data), websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected")

async def simulate_ai_agent(user_message: str, image_url: Optional[str] = None, session_id: str = "default") -> str:
    """
    Process user message using Cora AI agent with Agent Framework
    """
    global agent_instance, agent_sessions
    
    # Initialize agent if not already done
    if agent_instance is None:
        await initialize_agent()
    
    # If agent is still None, fall back to simple responses
    if agent_instance is None:
        return "I'm sorry, I'm having trouble connecting to my tools right now. Please try again later."
    
    try:
        # Get or create session for this session ID
        if session_id not in agent_sessions:
            agent_sessions[session_id] = agent_instance.create_session(session_id=session_id)

        session = agent_sessions[session_id]
        
        # Prepare message with image if provided
        if image_url:
            logger.info(f"Processing message with image: {image_url}")
            
            # Convert relative URL to file path
            if image_url.startswith("/uploads/"):
                filename = image_url.replace("/uploads/", "")
                file_path = UPLOAD_DIR / filename
                
                if file_path.exists():
                    # Get MIME type and read image as bytes
                    mime_type = get_image_mime_type(filename)
                    
                    # Read image file as raw bytes
                    with open(file_path, "rb") as image_file:
                        image_bytes = image_file.read()
                    
                    logger.info(f"Image loaded: {len(image_bytes)} bytes, MIME type: {mime_type}")
                    
                    # Create a Message with multimodal content using Content factory methods
                    # Note: use 'contents' (plural) not 'content'
                    message_with_image = [
                        Message(
                            role="user",
                            contents=[
                                Content.from_text(user_message),
                                Content.from_data(image_bytes, media_type=mime_type)
                            ]
                        )
                    ]
                    
                    logger.info(f"Sending message with image to agent: {user_message}")
                    
                    response = await agent_instance.run(message_with_image, session=session)
                    response_text = response.text or ""
                else:
                    logger.warning(f"Image file not found: {file_path}")
                    # Fall back to text-only processing
                    response = await agent_instance.run(user_message, session=session)
                    response_text = response.text or ""
            else:
                logger.warning(f"Invalid image URL format: {image_url}")
                # Fall back to text-only processing
                response = await agent_instance.run(user_message, session=session)
                response_text = response.text or ""
        else:
            response = await agent_instance.run(user_message, session=session)
            response_text = response.text or ""
        
        return response_text if response_text else "I processed your request, but I'm having trouble generating a response. Please try rephrasing your question."
            
    except Exception as e:
        logger.error(f"Error in AI agent processing: {e}")
        import traceback
        traceback.print_exc()
        
        # Clear corrupted session to prevent state mismatch errors
        if session_id in agent_sessions:
            del agent_sessions[session_id]
            logger.info(f"Cleared corrupted session for session_id: {session_id}")
        
        return f"I encountered an error while processing your request: {str(e)}. Please try again."

@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup"""
    await initialize_agent()

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    global agent_instance, credential_instance
    if agent_instance:
        try:
            # Agent cleanup if needed
            pass
        except Exception as e:
            logger.error(f"Error during agent cleanup: {e}")
        agent_instance = None
    
    if credential_instance:
        try:
            await credential_instance.close()
        except Exception as e:
            logger.error(f"Error during credential cleanup: {e}")
        credential_instance = None

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
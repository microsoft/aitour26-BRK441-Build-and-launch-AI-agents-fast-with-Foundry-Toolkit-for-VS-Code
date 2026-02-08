# http://localhost:8000

from dotenv import load_dotenv
from azure.identity.aio import AzureCliCredential
from agent_framework.azure import AzureAIAgentClient
from agent_framework import ChatAgent, MCPStdioTool, ToolProtocol, ChatMessage, Content
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
ENDPOINT = os.environ.get("AZURE_AI_FOUNDRY_ENDPOINT",
                          "your_foundry_endpoint_here")
MODEL_DEPLOYMENT_NAME = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4.1-mini-1")
AGENT_NAME = "cora-web-agent"


def create_mcp_tools() -> list[ToolProtocol]:
    """Create MCP tools for the agent"""
    return [
        MCPStdioTool(
            name="zava_customer_sales_stdio",
            description="MCP server for Zava customer sales analysis",
            command="python",
            args=[
                "src/python/mcp_server/customer_sales/customer_sales.py",
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

# Global agent instance
agent_instance = None
credential_instance = None
async_exit_stack = None  # For managing async context

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
    global agent_instance, credential_instance, async_exit_stack
    if agent_instance is None:
        try:            # Remove problematic CA bundle environment variables that interfere with Azure CLI
            for var in ['REQUESTS_CA_BUNDLE', 'CURL_CA_BUNDLE']:
                if var in os.environ and os.environ[var] == '':
                    del os.environ[var]
                    logger.info(f"Removed empty {var} environment variable")
                        # Create async exit stack to manage the credential lifecycle
            if async_exit_stack is None:
                async_exit_stack = AsyncExitStack()

            # Create and manage the AzureCliCredential within the exit stack
            credential_instance = await async_exit_stack.enter_async_context(AzureCliCredential())

            # Create agent using AzureAIAgentClient.as_agent() for long-running apps
            agent_instance = await async_exit_stack.enter_async_context(
                AzureAIAgentClient(
                    project_endpoint=ENDPOINT,
                    model_deployment_name=MODEL_DEPLOYMENT_NAME,
                    credential=credential_instance,
                ).as_agent(
                    name=AGENT_NAME,
                    instructions=AGENT_INSTRUCTIONS,
                    tools=[
                        *create_mcp_tools(),
                    ],
                )
            )
            logger.info(
                "Agent Framework initialized successfully with AzureAIAgentClient")
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
        file_extension = file.filename.split(
            '.')[-1] if '.' in file.filename else 'jpg'
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
    global agent_instance

    # Initialize agent if not already done
    if agent_instance is None:
        await initialize_agent()

    # If agent is still None, fall back to simple responses
    if agent_instance is None:
        return "I'm sorry, I'm having trouble connecting to my tools right now. Please try again later."

    try:
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

                    logger.info(
                        f"Image loaded: {len(image_bytes)} bytes, MIME type: {mime_type}")

                    # Create a ChatMessage with multimodal content using DataContent
                    # Note: use 'contents' (plural) not 'content'
                    message_with_image = [
                        ChatMessage(
                            role="user",
                            contents=[
                                Content.from_text(user_message),
                                Content.from_data(image_bytes, mime_type)
                            ]
                        )
                    ]

                    logger.info(
                        f"Sending message with image to agent: {user_message}")

                    # Stream response from agent with image (no thread - each request is independent)
                    response_text = ""
                    async for chunk in agent_instance.run_stream(message_with_image):
                        if chunk.text:
                            response_text += chunk.text
                else:
                    logger.warning(f"Image file not found: {file_path}")
                    # Fall back to text-only processing
                    response_text = ""
                    async for chunk in agent_instance.run_stream(user_message):
                        if chunk.text:
                            response_text += chunk.text
            else:
                logger.warning(f"Invalid image URL format: {image_url}")
                # Fall back to text-only processing
                response_text = ""
                async for chunk in agent_instance.run_stream(user_message):
                    if chunk.text:
                        response_text += chunk.text
        else:
            # Stream response from agent (text only, no thread)
            response_text = ""
            async for chunk in agent_instance.run_stream(user_message):
                if chunk.text:
                    response_text += chunk.text

        return response_text if response_text else "I processed your request, but I'm having trouble generating a response. Please try rephrasing your question."

    except Exception as e:
        logger.error(f"Error in AI agent processing: {e}")
        import traceback
        traceback.print_exc()
        return f"I encountered an error while processing your request: {str(e)}. Please try again."


@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup"""
    await initialize_agent()


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    global agent_instance, credential_instance, async_exit_stack
    if agent_instance:
        try:
            # Agent cleanup if needed
            pass
        except Exception as e:
            logger.error(f"Error during agent cleanup: {e}")
        agent_instance = None

    if async_exit_stack:
        try:
            await async_exit_stack.aclose()
        except Exception as e:
            logger.error(f"Error during async exit stack cleanup: {e}")
        async_exit_stack = None

    credential_instance = None

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )

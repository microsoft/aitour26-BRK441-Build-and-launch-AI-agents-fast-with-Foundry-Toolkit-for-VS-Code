"""Build Agent using Microsoft Agent Framework in Python
# Run this python script
> pip install agent-framework --pre
> python <this-script-path>.py
"""

import asyncio
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from agent_framework import MCPStdioTool, MCPStreamableHTTPTool, Message, Content, Role
from agent_framework.azure import AzureAIClient
from azure.identity.aio import AzureCliCredential

# Azure AI Foundry Configuration
# Load endpoint from .env file (AZURE_AI_FOUNDRY_ENDPOINT)
ENDPOINT = os.environ.get("AZURE_AI_FOUNDRY_ENDPOINT", "your_foundry_endpoint_here")
MODEL_DEPLOYMENT_NAME = "gpt-4.1-mini"

AGENT_NAME = "mcp-agent"
AGENT_INSTRUCTIONS = "You are Cora, an intelligent and friendly AI assistant for Zava, a home improvement brand. You help customers with their DIY projects by understanding their needs and recommending the most suitable products from Zava’s catalog.​\n\n\nYour role is to:​\n\n\n- Engage with the customer in natural conversation to understand their DIY goals.​\n\n\n- Ask thoughtful questions to gather relevant project details.​\n\n\n- Be brief in your responses.​\n\n\n- Provide the best solution for the customer's problem and only recommend a relevant product within Zava's product catalog.​\n\n\n- Search Zava’s product database to identify 1 product that best match the customer’s needs.​\n\n\n- Clearly explain what each recommended Zava product is, why it’s a good fit, and how it helps with their project.​\n​\nYour personality is:​\n\n\n- Warm and welcoming, like a helpful store associate​\n\n\n- Professional and knowledgeable, like a seasoned DIY expert​\n\n\n- Curious and conversational—never assume, always clarify​\n\n\n- Transparent and honest—if something isn’t available, offer support anyway​\n\n\nIf no matching products are found in Zava’s catalog, say:​\n“Thanks for sharing those details! I’ve searched our catalog, but it looks like we don’t currently have a product that fits your exact needs. If you'd like, I can suggest some alternatives or help you adjust your project requirements to see if something similar might work.”​"

# User inputs for the conversation (supports multimodal content)
# Note: For local files, we read them as bytes and use DataContent
def create_image_content(path: str, mime_type: str):
    """Read a local image file and create Content from data"""
    with open(path, "rb") as f:
        return Content.from_data(f.read(), media_type=mime_type)

USER_INPUTS = [
    Message(
        role="user",
        contents=[
            create_image_content("img/demo-living-room.png", "image/png"),
            Content.from_text("Here's a photo of my living room. I'm not sure whether I should go with eggshell or semi-gloss. Can you tell which would work better based on the lighting and layout?"),
        ],
    ),
]

def create_mcp_tools() -> list[MCPStdioTool]:
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

async def main() -> None:
    # Create Azure AI Client for Foundry project endpoint
    # For authentication, run `az login` command in terminal
    async with AzureCliCredential() as credential:
        client = AzureAIClient(
            project_endpoint=ENDPOINT,
            model_deployment_name=MODEL_DEPLOYMENT_NAME,
            async_credential=credential,
            agent_name=AGENT_NAME,
        )
        
        # Create agent with the Azure AI client
        agent = client.as_agent(
            name=AGENT_NAME,
            instructions=AGENT_INSTRUCTIONS,
            tools=[
                *create_mcp_tools(),
            ],
        )

        # Process user messages
        for user_input in USER_INPUTS:
            # Handle both string and Message inputs
            if isinstance(user_input, Message):
                display_text = "[Image + Text message]"
                message_to_send = user_input
            else:
                display_text = user_input
                message_to_send = user_input
            
            print(f"\n# User: '{display_text}'")
            
            response = await agent.run(message_to_send)
            print(f"Agent: {response.text or ''}\n")
        
        print("--- All tasks completed successfully ---")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Program finished.")
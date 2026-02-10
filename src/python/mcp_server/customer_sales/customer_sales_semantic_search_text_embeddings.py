#!/usr/bin/env python3
"""
Customer Sales Semantic Search Tool

This module provides semantic search functionality for products using Azure OpenAI embeddings.
It generates embeddings for user queries and finds similar products using pgvector cosine similarity.

Usage:
    from customer_sales_semantic_search import SemanticSearchTool
    
    tool = SemanticSearchTool()
    embedding = tool.generate_query_embedding("waterproof electrical box")

Requirements:
    - Azure OpenAI configured
    - openai package
    - azure-identity package
"""

import os
from pathlib import Path
from typing import List, Optional

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import AzureOpenAI


class SemanticSearchTextEmbedding:
    """Handles semantic search operations using Azure OpenAI embeddings."""
    
    def __init__(self) -> None:
        """Initialize the semantic search tool with Azure OpenAI configuration."""
        # Load environment variables
        self._load_environment()
        
        # Azure OpenAI configuration
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "<ENDPOINT_URL>")
        self.model_name = "text-embedding-3-small"
        self.deployment = os.getenv("EMBEDDING_MODEL_DEPLOYMENT_NAME", "text-embedding-3-small")
        
        # Check if Azure OpenAI endpoint is configured
        if self.endpoint == "<ENDPOINT_URL>" or not self.endpoint:
            print("❌ Warning: AZURE_OPENAI_ENDPOINT not configured. Semantic search will not work.")
            print(f"   Current value: '{self.endpoint}'")
            print("   Please set AZURE_OPENAI_ENDPOINT in your .env file")
            self.openai_client = None
            return
        
        print(f"✓ Azure OpenAI Endpoint: {self.endpoint}")
        print(f"✓ Embedding Deployment: {self.deployment}")
        
        # Initialize Azure OpenAI client
        try:
            self.openai_client = self._setup_azure_openai_client()
            print("✓ Azure OpenAI client initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Azure OpenAI client: {e}")
            import traceback
            traceback.print_exc()
            self.openai_client = None
    
    def _load_environment(self) -> None:
        """Load environment variables from .env files."""
        script_dir = Path(__file__).parent
        # Try to load .env from script directory first, then parent directories
        env_paths = [
            script_dir / '.env',
            script_dir.parent.parent.parent / '.env',  # Up to workspace root
        ]

        env_loaded = False
        for env_path in env_paths:
            if env_path.exists():
                load_dotenv(env_path, override=False)
                print(f"✓ Loaded environment from: {env_path}")
                env_loaded = True
                break
        
        if not env_loaded:
            # Fallback to default behavior (searches current dir and parents)
            load_dotenv(override=False)
            print("✓ Loaded environment using default search path")
    
    def _setup_azure_openai_client(self) -> AzureOpenAI:
        """Setup and return Azure OpenAI client with token provider or API key."""
        api_version = "2024-02-01"
        
        # Check if API key is provided (fallback authentication method)
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        
        if api_key:
            print("ℹ️  Using API key authentication")
            return AzureOpenAI(
                api_version=api_version,
                azure_endpoint=self.endpoint,
                api_key=api_key,
            )
        else:
            print("ℹ️  Using Azure AD token authentication (DefaultAzureCredential)")
            token_provider = get_bearer_token_provider(
                DefaultAzureCredential(), 
                "https://cognitiveservices.azure.com/.default"
            )
            return AzureOpenAI(
                api_version=api_version,
                azure_endpoint=self.endpoint,
                azure_ad_token_provider=token_provider,
            )
    
    def generate_query_embedding(self, query_text: str) -> Optional[List[float]]:
        """
        Generate embedding for the user's query text.
        
        Args:
            query_text: The user's product description query
            
        Returns:
            List of float values representing the embedding, or None if failed
        """
        if not self.openai_client:
            print("❌ Azure OpenAI client not initialized. Cannot generate embeddings.")
            return None
            
        try:
            print(f"🔍 Generating embedding for query: '{query_text}'")
            print(f"   Using endpoint: {self.endpoint}")
            print(f"   Using deployment: {self.deployment}")
            
            # Generate embedding using Azure OpenAI
            response = self.openai_client.embeddings.create(
                input=[query_text],
                model=self.deployment
            )
            
            # Extract embedding from response
            embedding = response.data[0].embedding
            print(f"✓ Generated embedding successfully (dimension: {len(embedding)})")
            return embedding
            
        except Exception as e:
            print(f"❌ Error generating embedding: {type(e).__name__}: {e}")
            print(f"   Endpoint: {self.endpoint}")
            print(f"   Deployment: {self.deployment}")
            print(f"   Query: '{query_text}'")
            
            # Print detailed error info for common issues
            if "401" in str(e) or "unauthorized" in str(e).lower():
                print("   ⚠️  Authentication failed - check your Azure credentials")
            elif "404" in str(e) or "not found" in str(e).lower():
                print(f"   ⚠️  Deployment '{self.deployment}' not found - verify deployment name")
            elif "endpoint" in str(e).lower():
                print(f"   ⚠️  Invalid endpoint format - should be https://YOUR-RESOURCE.openai.azure.com/")
            
            import traceback
            traceback.print_exc()
            return None
    
    def is_available(self) -> bool:
        """Check if the semantic search functionality is available."""
        return self.openai_client is not None
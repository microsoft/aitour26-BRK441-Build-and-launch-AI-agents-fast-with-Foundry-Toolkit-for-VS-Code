# AI Agent Workshop - Copilot Instructions

## Project Overview

This is an **AI Tour 2026 workshop** demonstrating rapid AI agent development using **Microsoft Foundry**, **AI Toolkit**, and **Model Context Protocol (MCP)**. The project showcases "Cora" - an intelligent customer service agent for Zava (fictional home improvement retailer).

**Key Technologies**: Microsoft Agent Framework, FastAPI, PostgreSQL with pgvector, Azure OpenAI, FastMCP

## Architecture

### Core Components

1. **PostgreSQL Database** (`docker-compose.yml` → pgvector/pgvector:pg17)
   - Port: 15432 (external) → 5432 (internal)
   - Database: `zava`, Schema: `retail`
   - 400+ products, 50K+ customers, 200K+ orders (2020-2026)
   - **pgvector extension** for semantic search (512-dim image, 1536-dim text embeddings)
   - Default credentials: `postgres` / `P@ssw0rd!`

2. **MCP Servers** (`src/python/mcp_server/`)
   - **sales_analysis**: Multi-table queries, schema inspection, sales analytics
   - **customer_sales**: Name-based product search
   - **customer_sales_semantic_search**: AI-powered semantic product discovery (requires Azure OpenAI)
   - Support both **stdio** (VS Code integration) and **HTTP** modes
   - Configured in `.vscode/mcp.json` for AI Toolkit integration

3. **Web Application** (`src/python/web_app/web_app.py`)
   - FastAPI + WebSocket for real-time agent chat
   - Serves from `src/shared/static/index.html`
   - Uses Microsoft Agent Framework to orchestrate Cora agent
   - Multi-modal support (text + images)

4. **Standalone Agent** (`cora-agent-MAF.py`)
   - Reference implementation using Agent Framework directly
   - Demonstrates MCP tool integration and multi-modal prompts

## Row Level Security (RLS) Pattern

**Critical**: All MCP servers use RLS for multi-tenant data isolation.

- **RLS_USER_ID** controls which store's data is visible
- Global access: `00000000-0000-0000-0000-000000000000`
- Store-specific UUIDs in `.env` (Seattle: `f47ac10b-58cc-4372-a567-0e02b2c3d479`, etc.)
- **Two authentication methods**:
  - **Stdio mode**: `--RLS_USER_ID` CLI argument (see `.vscode/mcp.json`)
  - **HTTP mode**: `x-rls-user-id` header
- RLS applies to tables: `retail.customers`, `retail.orders`, `retail.order_items`, `retail.inventory`

When modifying MCP servers or queries, **always** verify RLS compliance.

## Development Workflows

### Running the Stack

```bash
# Start PostgreSQL (auto-initializes from data/zava_retail_2025_07_21_postgres_rls.backup)
docker-compose up -d

# Run web app (FastAPI + Agent Framework integration)
cd src/python/web_app && python web_app.py
# Access at http://localhost:8000

# Run standalone agent (console-based interaction)
python cora-agent-MAF.py

# Run MCP servers individually (HTTP mode for debugging)
cd src/python/mcp_server/customer_sales && python customer_sales.py
```

### AI Toolkit Workflow (VS Code Extension)

The intended development path (see `session-delivery-resources/demos-instructions/`):

1. **Model Catalog** → Compare models (e.g., gpt-4.1-mini vs gpt-4.1-nano)
2. **Agent Builder** → Define Cora's system prompt + attach MCP tools
3. **Evaluation Tab** → Test with CSV datasets, manual/AI-assisted evaluation
4. **Export to Code** → Generate production-ready Agent Framework code

### MCP Server Development

MCP servers use **FastMCP** (modern async MCP framework):

```python
# Pattern: Lifecycle management with AppContext
@dataclass
class AppContext:
    db: PostgreSQLCustomerSales  # Connection pool
    semantic_search: SemanticSearchTextEmbedding  # Optional for semantic servers

async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    # Initialize resources (db pool, Azure OpenAI client)
    yield AppContext(db=..., semantic_search=...)
    # Cleanup on shutdown

mcp = FastMCP("server-name", lifespan=app_lifespan, stateless_http=True)

@mcp.tool()
async def tool_function(
    ctx: Context[AppContext],
    param: Annotated[str, Field(description="...")],
) -> str:
    rls_user_id = get_rls_user_id(ctx)  # Extract from headers/args
    return await ctx.app_ctx.db.query(rls_user_id, param)
```

**Testing**: Each MCP file is runnable standalone (`if __name__ == "__main__"`) for local testing.

## Database Patterns

### Schema Structure

- **Hierarchy**: `categories` → `product_types` → `products`
- **Transactions**: `orders` (header) → `order_items` (line items)
- **Inventory**: Store-specific stock levels
- **Embeddings**: `product_image_embeddings` (512-dim), `product_description_embeddings` (1536-dim)

### Generating Test Data

```bash
cd data/database
pip install -r requirements.txt

# Full database generation
python generate_zava_postgres.py --num-customers 100000

# Utility scripts
python add_product.py              # Interactive product addition
python query_by_description.py     # Test semantic search
python generate_skus.py            # Generate missing SKUs
```

**Seasonal Patterns**: Products have Washington State seasonal multipliers (e.g., paint peaks in April at 2.2x, garden outdoor drops to 50% in winter). See `data/database/README.md` for details.

## Configuration

### Environment Variables (.env)

```bash
# Azure AI Foundry
AZURE_AI_FOUNDRY_ENDPOINT="https://<project>.eastus.api.azureml.ms"
MODEL_DEPLOYMENT_NAME="gpt-4.1-mini"

# Azure OpenAI (for semantic search servers)
AZURE_OPENAI_ENDPOINT="https://<resource>.openai.azure.com/"

# Database
POSTGRES_URL="postgresql://store_manager:StoreManager123!@db:5432/zava"

# Row Level Security
RLS_USER_ID="00000000-0000-0000-0000-000000000000"
```

### Python Dependencies

- **Agent Framework**: `agent-framework>=1.0.0b260130`
- **MCP**: `mcp>=1.10.0,<2.0.0`
- **Database**: `asyncpg>=0.30.0`
- **AI**: `azure-ai-agents`, `azure-ai-projects`, `openai>=1.97.0`
- **Linting**: Black + Ruff (line length: 120, see `pyproject.toml`)

Install: `pip install -r requirements-dev.txt` (includes `src/python/requirements.txt`)

## Code Conventions

1. **Async by default**: All agent/MCP code uses asyncio
2. **Type hints**: Use `Annotated[T, Field(...)]` for Pydantic validation in MCP tools
3. **Context management**: Use `async with` for Azure credentials and database pools
4. **Error handling**: MCP tools return user-friendly error messages as strings
5. **Import sorting**: Ruff/isort with "black" profile (`pyproject.toml`)

## Common Tasks

### Adding a New MCP Tool

1. Add `@mcp.tool()` decorated function to MCP server file
2. Use `ctx: Context[AppContext]` for app resources
3. Extract RLS user ID: `rls_user_id = get_rls_user_id(ctx)`
4. Add Pydantic `Field(description=...)` for clear tool descriptions
5. Reload VS Code MCP servers (Restart MCP servers from command palette)

### Modifying Agent System Prompt

**AI Toolkit Path**: Agent Builder → Instructions field
**Code Path**: Update `AGENT_INSTRUCTIONS` in `cora-agent-MAF.py` or `web_app.py`

**Key elements for Cora**:
- Role: Friendly home improvement assistant for Zava
- Behavior: Brief responses, ask clarifying questions, recommend 1 product
- Personality: Warm, professional, transparent
- Fallback: Graceful handling when no products match

### Adding Evaluation Datasets

File: `data/evals-data.csv` (if exists) or use AI Toolkit → Evaluation Tab → Generate Data

**Example queries**:
- "What type of organic compost does Zava have?"
- "Does Zava have a paint bucket? If so how much is it?"
- "How much tape measure is currently in stock?"

## Deployment (Azure)

### Infrastructure as Code

See `infra/main.bicep`:
- Deploys Azure AI Foundry project, Application Insights, model deployments
- Default models: gpt-4o-mini, text-embedding-3-small
- Run: `./infra/deploy.sh` or `./infra/deploy.ps1`

### Model Deployments

Configured in `infra/foundry-model-deployment.bicep`:
- GPT-4o-mini: 140 TPM capacity (GlobalStandard)
- text-embedding-3-small: 120 TPM capacity

## Troubleshooting

**Database connection fails**: Verify `docker-compose up -d` completed and healthcheck passed (check `docker ps`)

**MCP tools not appearing in AI Toolkit**: Reload window or restart MCP servers from VS Code command palette

**Semantic search errors**: Verify `AZURE_OPENAI_ENDPOINT` is set and text-embedding-3-small is deployed

**RLS returns wrong data**: Check `RLS_USER_ID` matches intended store UUID in `.env` or MCP config

**Import errors**: Ensure `pip install -r requirements-dev.txt` ran in dev container environment

## Resources

- Workshop demos: `session-delivery-resources/demos-instructions/`
- MCP server docs: `src/python/mcp_server/{sales_analysis,customer_sales}/README.md`
- Database design: `data/database/README.md`
- AI Toolkit: https://aka.ms/AIToolkit
- Microsoft Agent Framework: Uses `agent_framework` package (beta)

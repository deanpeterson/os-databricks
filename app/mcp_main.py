from .mcp_tools import mcp
from starlette.applications import Starlette
from starlette.routing import Mount
import uvicorn

# Create a Starlette application and mount the MCP SSE app
app = Starlette(
    routes=[
        # Root path "/" will serve SSE connections to the MCP server
        Mount('/', app=mcp.sse_app()),
    ]
)

if __name__ == "__main__":
    uvicorn.run("mcp_main:app", host="0.0.0.0", port=8000)

from .mcp_tools import mcp, upload_csv
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.requests import Request
from starlette.responses import JSONResponse
import uvicorn

async def upload_file_endpoint(request: Request):
    form = await request.form()
    uploaded_file = form.get("file")

    if uploaded_file is None:
        return JSONResponse({"error": "No file uploaded"}, status_code=400)

    file_name = uploaded_file.filename
    file_content = await uploaded_file.read()

    # Call your existing MCP tool directly
    upload_result = await upload_csv(file_name, file_content)

    if upload_result.startswith("Error"):
        return JSONResponse({"error": upload_result}, status_code=400)

    return JSONResponse({"message": upload_result})

# Extend your Starlette application:
app = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),  # MCP SSE endpoint remains the same
        Route('/upload', upload_file_endpoint, methods=['POST']),  # Add this new route
    ]
)

if __name__ == "__main__":
    uvicorn.run("mcp_main:app", host="0.0.0.0", port=8000)

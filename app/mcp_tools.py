from typing import Any, List, Dict, Union
import os
import shutil
from mcp.server.fastmcp import FastMCP

# If you also need httpx for other network calls (like in the weather tutorial), import it:
# import httpx

from app.spark_queries import filter_zipcodes

# Initialize FastMCP server (similar to the weather tutorial)
mcp = FastMCP("spark")

# Create our uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@mcp.tool()
async def upload_csv(file_name: str, file_content: bytes) -> str:
    """
    Upload a CSV file to the server.

    Args:
        file_name: Name of the file to upload.
        file_content: Raw bytes of the file.

    Returns:
        A confirmation message with file path or an error message.
    """
    if not file_name.lower().endswith('.csv'):
        return "Error: File must be a CSV."

    file_path = os.path.join(UPLOAD_DIR, file_name)
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        return f"File uploaded successfully: {file_path}"
    except Exception as e:
        return f"Error uploading file: {str(e)}"

@mcp.tool()
def query_zipcodes(filename: str, zipcode: int) -> Union[List[Dict[str, Any]], str]:
    """
    Query zip codes from an uploaded CSV using PySpark.

    Args:
        filename: Name of the CSV file previously uploaded.
        zipcode: Zip code to query.

    Returns:
        A list of matching rows as dictionaries, or an error message.
    """
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        return "Error: CSV file not found."

    try:
        results = filter_zipcodes(file_path, zipcode)
        if not results:
            return "No matching zip codes found."
        return results
    except Exception as e:
        return f"Error during query: {str(e)}"

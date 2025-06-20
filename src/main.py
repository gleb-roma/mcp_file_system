import os
import shutil
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("mcp-file-system")

# Base directory for file operations
BASE_DIR = Path(os.getenv("MCP_FILE_SYSTEM_BASE_DIR", "/tmp/mcp_file_system"))

# Ensure base directory exists
BASE_DIR.mkdir(parents=True, exist_ok=True)


def _resolve_path(file_path: str) -> Path:
    """
    Resolves a file path against the base directory and performs security checks.
    """
    if ".." in Path(file_path).parts:
        raise PermissionError("Path traversal is not allowed.")

    absolute_path = (BASE_DIR / file_path).resolve()

    if not absolute_path.is_relative_to(BASE_DIR.resolve()):
        raise PermissionError("Access denied: Path is outside the allowed base directory.")

    return absolute_path


@mcp.tool()
async def read_file(file_path: str) -> str:
    """
    Reads the contents of a file.

    Args:
        file_path: Path to the file relative to the base directory.
    """
    try:
        path = _resolve_path(file_path)
        if not path.is_file():
            return f"Error: '{file_path}' is not a file or does not exist."
        return path.read_text(encoding='utf-8')
    except Exception as e:
        return f"Error reading file '{file_path}': {e}"


@mcp.tool()
async def write_file(file_path: str, content: str) -> str:
    """
    Writes content to a file, creating directories if they don't exist and overwriting the file if it does.

    Args:
        file_path: Path to the file relative to the base directory.
        content: The content to write to the file.
    """
    try:
        path = _resolve_path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return f"Successfully wrote {len(content.encode('utf-8'))} bytes to '{file_path}'."
    except Exception as e:
        return f"Error writing to file '{file_path}': {e}"


@mcp.tool()
async def list_directory(directory_path: str = ".") -> str:
    """
    Lists the contents of a directory.

    Args:
        directory_path: Path to the directory relative to the base directory. Defaults to the base directory itself.
    """
    try:
        path = _resolve_path(directory_path)
        if not path.is_dir():
            return f"Error: '{directory_path}' is not a directory."

        items = []
        for item in sorted(path.iterdir()):
            item_type = "DIR" if item.is_dir() else "FILE"
            items.append(f"{item_type:4s} {item.name}")

        if not items:
            return f"Directory '{path.relative_to(BASE_DIR)}' is empty."

        return f"Contents of '{path.relative_to(BASE_DIR)}':\n" + "\n".join(items)
    except Exception as e:
        return f"Error listing directory '{directory_path}': {e}"


@mcp.tool()
async def delete_file(file_path: str) -> str:
    """
    Deletes a file. This cannot delete directories.

    Args:
        file_path: Path to the file to delete, relative to the base directory.
    """
    try:
        path = _resolve_path(file_path)
        if not path.exists():
            return f"Error: File '{file_path}' not found."
        if not path.is_file():
            return f"Error: Path '{file_path}' is a directory, not a file. Use a different tool to delete directories."
        
        path.unlink()
        return f"Successfully deleted file '{file_path}'."
    except Exception as e:
        return f"Error deleting file '{file_path}': {e}"


@mcp.tool()
async def move_file(source_path: str, destination_path: str) -> str:
    """
    Moves or renames a file.

    Args:
        source_path: The path of the file to move.
        destination_path: The new path for the file.
    """
    try:
        source = _resolve_path(source_path)
        destination = _resolve_path(destination_path)
        
        if not source.exists():
            return f"Error: Source path '{source_path}' does not exist."
        
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
        return f"Successfully moved '{source_path}' to '{destination_path}'."
    except Exception as e:
        return f"Error moving file: {e}"


@mcp.tool()
async def copy_file(source_path: str, destination_path: str) -> str:
    """
    Copies a file.

    Args:
        source_path: The path of the file to copy.
        destination_path: The path to copy the file to.
    """
    try:
        source = _resolve_path(source_path)
        destination = _resolve_path(destination_path)

        if not source.is_file():
            return f"Error: Source '{source_path}' is not a file."
            
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        return f"Successfully copied '{source_path}' to '{destination_path}'."
    except Exception as e:
        return f"Error copying file: {e}"


if __name__ == "__main__":
    mcp.run(transport='stdio')

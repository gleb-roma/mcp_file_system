from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
from pathlib import Path
import os

# Initialize FastAPI app
app = FastAPI(title="File System MCP Server")

# Initialize MCP server
mcp = FastApiMCP(app)

# Base directory for file operations
BASE_DIR = Path(os.getenv("MCP_FILE_SYSTEM_BASE_DIR", "/tmp/mcp_file_system"))

# Ensure base directory exists
BASE_DIR.mkdir(parents=True, exist_ok=True)

# Mount the MCP server to the FastAPI app
mcp.mount()

@app.post("/read")
async def read_file(file_path: str) -> dict:
    """
    Read the contents of a file.
    
    Args:
        file_path: Path to the file relative to the base directory
        
    Returns:
        dict: File contents and metadata
    """
    try:
        full_path = BASE_DIR / file_path
        if not str(full_path).startswith(str(BASE_DIR)):
            raise HTTPException(status_code=403, detail="Access denied: Path outside base directory")
            
        if not full_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
            
        with open(full_path, 'r') as f:
            content = f.read()
            
        return {
            "content": content,
            "path": str(full_path),
            "size": full_path.stat().st_size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/write")
async def write_file(file_path: str, content: str) -> dict:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file relative to the base directory
        content: Content to write to the file
        
    Returns:
        dict: Operation status and file metadata
    """
    try:
        full_path = BASE_DIR / file_path
        if not str(full_path).startswith(str(BASE_DIR)):
            raise HTTPException(status_code=403, detail="Access denied: Path outside base directory")
            
        # Create parent directories if they don't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w') as f:
            f.write(content)
            
        return {
            "status": "success",
            "path": str(full_path),
            "size": full_path.stat().st_size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list")
async def list_directory(dir_path: str = "") -> dict:
    """
    List contents of a directory.
    
    Args:
        dir_path: Path to the directory relative to the base directory
        
    Returns:
        dict: Directory contents and metadata
    """
    try:
        full_path = BASE_DIR / dir_path
        if not str(full_path).startswith(str(BASE_DIR)):
            raise HTTPException(status_code=403, detail="Access denied: Path outside base directory")
            
        if not full_path.exists():
            raise HTTPException(status_code=404, detail="Directory not found")
            
        if not full_path.is_dir():
            raise HTTPException(status_code=400, detail="Path is not a directory")
            
        contents = []
        for item in full_path.iterdir():
            contents.append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else None
            })
            
        return {
            "path": str(full_path),
            "contents": contents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete")
async def delete_file(file_path: str) -> dict:
    """
    Delete a file.
    
    Args:
        file_path: Path to the file relative to the base directory
        
    Returns:
        dict: Operation status
    """
    try:
        full_path = BASE_DIR / file_path
        if not str(full_path).startswith(str(BASE_DIR)):
            raise HTTPException(status_code=403, detail="Access denied: Path outside base directory")
            
        if not full_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
            
        if not full_path.is_file():
            raise HTTPException(status_code=400, detail="Path is not a file")
            
        full_path.unlink()
        return {
            "status": "success",
            "message": f"File {file_path} deleted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/move")
async def move_file(source_path: str, destination_path: str) -> dict:
    """
    Move or rename a file.
    
    Args:
        source_path: Path to the source file relative to the base directory
        destination_path: Path to the destination relative to the base directory
        
    Returns:
        dict: Operation status and new file metadata
    """
    try:
        source_full = BASE_DIR / source_path
        dest_full = BASE_DIR / destination_path
        
        if not str(source_full).startswith(str(BASE_DIR)) or not str(dest_full).startswith(str(BASE_DIR)):
            raise HTTPException(status_code=403, detail="Access denied: Path outside base directory")
            
        if not source_full.exists():
            raise HTTPException(status_code=404, detail="Source file not found")
            
        if not source_full.is_file():
            raise HTTPException(status_code=400, detail="Source path is not a file")
            
        # Create parent directories if they don't exist
        dest_full.parent.mkdir(parents=True, exist_ok=True)
        
        source_full.rename(dest_full)
        return {
            "status": "success",
            "source": str(source_full),
            "destination": str(dest_full),
            "size": dest_full.stat().st_size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/copy")
async def copy_file(source_path: str, destination_path: str) -> dict:
    """
    Copy a file.
    
    Args:
        source_path: Path to the source file relative to the base directory
        destination_path: Path to the destination relative to the base directory
        
    Returns:
        dict: Operation status and new file metadata
    """
    try:
        source_full = BASE_DIR / source_path
        dest_full = BASE_DIR / destination_path
        
        if not str(source_full).startswith(str(BASE_DIR)) or not str(dest_full).startswith(str(BASE_DIR)):
            raise HTTPException(status_code=403, detail="Access denied: Path outside base directory")
            
        if not source_full.exists():
            raise HTTPException(status_code=404, detail="Source file not found")
            
        if not source_full.is_file():
            raise HTTPException(status_code=400, detail="Source path is not a file")
            
        # Create parent directories if they don't exist
        dest_full.parent.mkdir(parents=True, exist_ok=True)
        
        import shutil
        shutil.copy2(source_full, dest_full)
        return {
            "status": "success",
            "source": str(source_full),
            "destination": str(dest_full),
            "size": dest_full.stat().st_size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

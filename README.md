# MCP File System Server

A Model Context Protocol (MCP) server for secure file system operations, built with FastAPI and Python. This server provides file operations (read, write, list, delete, move, copy) with security restrictions to limit access to a specific base directory.

## Features

- **Secure File Operations**: Read, write, list, delete, move, and copy files
- **Path Security**: All operations are restricted to a configurable base directory
- **FastAPI Integration**: Modern async web framework with automatic API documentation
- **MCP Protocol**: Designed to work with Claude Desktop and other MCP clients
- **Easy Testing**: Built-in Swagger UI for interactive API testing

## Installation

### Prerequisites

- Python 3.11 or higher
- `uv` package manager (recommended)

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd mcp_file_system
```

2. Install dependencies using `uv`:
```bash
uv sync
```

## Usage

### Starting the Server

Start the server in development mode with auto-reload:

```bash
make run
```

Or manually:
```bash
uv run uvicorn src.main:app --reload
```

The server will start on `http://127.0.0.1:8000`

### Testing the Server

#### 1. Check if the server is running

```bash
curl -X GET http://localhost:8000/docs
```

This should return the Swagger UI HTML page.

#### 2. View available endpoints

```bash
curl -X GET http://localhost:8000/openapi.json | jq '.paths | keys'
```

Expected output:
```json
[
  "/copy",
  "/delete", 
  "/list",
  "/move",
  "/read",
  "/write"
]
```

#### 3. Test the write endpoint

```bash
curl -X POST 'http://localhost:8000/write?file_path=test.txt&content=Hello%20MCP!'
```

Expected response:
```json
{
  "status": "success",
  "path": "/tmp/mcp_file_system/test.txt",
  "size": 10
}
```

**Note**: Use URL encoding for special characters in the content parameter. For example:
- Space: `%20`
- Exclamation mark: `%21`
- Quote: `%22`

## API Endpoints

### POST /write
Write content to a file.

**Parameters:**
- `file_path` (query): Path to the file relative to the base directory
- `content` (query): Content to write to the file

**Example:**
```bash
curl -X POST 'http://localhost:8000/write?file_path=example.txt&content=Hello%20World!'
```

### POST /read
Read the contents of a file.

**Parameters:**
- `file_path` (query): Path to the file relative to the base directory

**Example:**
```bash
curl -X POST 'http://localhost:8000/read?file_path=example.txt'
```

### GET /list
List contents of a directory.

**Parameters:**
- `dir_path` (query, optional): Path to the directory relative to the base directory

**Example:**
```bash
curl -X GET 'http://localhost:8000/list?dir_path='
```

### DELETE /delete
Delete a file.

**Parameters:**
- `file_path` (query): Path to the file relative to the base directory

**Example:**
```bash
curl -X DELETE 'http://localhost:8000/delete?file_path=example.txt'
```

### POST /move
Move or rename a file.

**Parameters:**
- `source_path` (query): Path to the source file relative to the base directory
- `destination_path` (query): Path to the destination relative to the base directory

**Example:**
```bash
curl -X POST 'http://localhost:8000/move?source_path=old.txt&destination_path=new.txt'
```

### POST /copy
Copy a file.

**Parameters:**
- `source_path` (query): Path to the source file relative to the base directory
- `destination_path` (query): Path to the destination relative to the base directory

**Example:**
```bash
curl -X POST 'http://localhost:8000/copy?source_path=original.txt&destination_path=backup.txt'
```

## Configuration

### Base Directory

The server restricts all file operations to a base directory for security. By default, this is set to `/tmp/mcp_file_system`.

You can change this by setting the `MCP_FILE_SYSTEM_BASE_DIR` environment variable:

```bash
export MCP_FILE_SYSTEM_BASE_DIR=/path/to/your/directory
make run
```

## Development

### Project Structure

```
mcp_file_system/
├── src/
│   ├── __init__.py
│   ├── main.py          # Main FastAPI application
│   ├── file_ops.py      # File operation utilities
│   └── security.py      # Security and validation functions
├── pyproject.toml       # Project dependencies and metadata
├── Makefile            # Development commands
├── TODO.md             # Development roadmap
└── README.md           # This file
```

### Available Make Commands

- `make run` - Start the server in development mode
- `make clean` - Clean up Python cache files
- `make help` - Show available commands

## Security Considerations

- All file operations are restricted to the configured base directory
- Path traversal attacks are prevented by validating all paths
- The server runs on localhost by default for development

## Testing with Claude Desktop

This MCP server is designed to work with Claude Desktop. To connect:

1. Ensure the server is running on `http://localhost:8000`
2. In Claude Desktop, add the MCP server with the appropriate configuration
3. The server will provide file system tools that Claude can use

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in the Makefile or use a different port
2. **Permission denied**: Ensure the base directory is writable
3. **Curl hangs**: Use proper URL encoding for special characters in parameters

### Debug Mode

For detailed logging, you can run the server with debug output:

```bash
uv run uvicorn src.main:app --reload --log-level debug
```

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

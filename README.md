# MCP File System Server

A Model Context Protocol (MCP) server that provides secure file system operations through a sandboxed environment.

## Features

- **Secure File Operations**: All operations are confined to a configurable base directory
- **Path Traversal Protection**: Prevents access to files outside the allowed directory
- **Comprehensive Tools**: Read, write, list, delete, move, and copy files
- **Error Handling**: Robust error handling with informative messages

## Installation

1. Install dependencies:
```bash
make install
```

2. Set the base directory (optional):
```bash
export MCP_FILE_SYSTEM_BASE_DIR="/path/to/your/sandbox"
```

## Usage

### Running the Server

```bash
make run
```

Or directly:
```bash
uv run src/main.py
```

### Available Tools

- `read_file(file_path: str)` - Read file contents
- `write_file(file_path: str, content: str)` - Write content to file
- `list_directory(directory_path: str)` - List directory contents
- `delete_file(file_path: str)` - Delete a file
- `move_file(source_path: str, destination_path: str)` - Move/rename a file
- `copy_file(source_path: str, destination_path: str)` - Copy a file

## Configuration

The server uses the `MCP_FILE_SYSTEM_BASE_DIR` environment variable to set the base directory for all file operations. If not set, it defaults to `/tmp/mcp_file_system`.

## Security

- All paths are resolved relative to the base directory
- Path traversal attacks (using `..`) are prevented
- Access outside the base directory is blocked
- File operations are sandboxed

## Testing

Test that the server imports correctly:
```bash
make test
```

## Development

Run in development mode with auto-reload:
```bash
make dev
```

## Integration with Claude Desktop

To use this server with Claude Desktop, add the following to your `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "file-system": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/mcp_file_system",
        "run",
        "src/main.py"
      ]
    }
  }
}
```

Replace `/ABSOLUTE/PATH/TO/mcp_file_system` with the actual absolute path to your project directory.

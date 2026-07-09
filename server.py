import asyncio
import json
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

from tools.file_system import (
    create_folder, write_file, read_file, delete_file, list_files, edit_file, edit_replace_file
)

server = Server("file_system-agent")

@server.list_tools()
async def list_tools() ->list[types.Tool]:
    return [
        types.Tool(
            name="create_folder",
            description ="Creates a folder at the specifed path",
            inputSchema={
                "type":"object",
                "properties":{
                    "path":{"type":"string", "description":"Relative Path of the folder to create"}
                },
                "required":["path"]
            }
        ),
        types.Tool(
            name = "write_file",
            description = "writes a file at the specified path with the given content",
            inputSchema={
                "type":"object",
                "properties":{
                    "path":{"type":"string", "description":"Relative Path of the file to write"},
                    "content":{"type":"string", "description":"Content to write to the file"}
                },
                "required":["path", "content"]
            }
        ),
        types.Tool(
            name = "read_file",
            description = "reads a file at the specified path and returns its content",
            inputSchema={
                "type":"object",
                "properties":{
                    "path":{"type":"string", "description":"Relative Path of the file to read"}
                },
                "required":["path"]
            }
        ),
        types.Tool(
            name = "delete_file",
            description = "deletes a file at the specified path",
            inputSchema={
                "type":"object",
                "properties":{
                    "path":{"type":"string", "description":"Relative Path of the file to delete"}
                },
                "required":["path"]
            }
        ),
        types.Tool(
            name = "list_files",
            description = "lists all files in the specified directory",
            inputSchema={
                "type":"object",
                "properties":{
                    "path":{"type":"string", "description":"Relative Path of the directory to list"}
                },
                "required":[] #will treate as current directory if not specified
            }
        ),
        types.Tool(
            name = "edit_file",
            description = "edits a file at the specified path with the given content",
            inputSchema={
                "type":"object",
                "properties":{
                    "path":{"type":"string", "description":"Relative Path of the file to edit"},
                    "content":{"type":"string", "description":"Content to write to the file"}
                },
                "required":["path", "content"]
            }
        ),
        types.Tool(
            name="edit_replace_file",
            description="Replaces the first occurrence of old_content with new_content in a file. Safer than edit_file for small targeted changes.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "old_content": {"type": "string"},
                    "new_content": {"type": "string"}
                },
                "required": ["path", "old_content", "new_content"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name:str, arguments:dict) -> list[types.TextContent]:
    tool_map = {
        "create_folder": lambda args: create_folder(args["path"]),
        "write_file": lambda args: write_file(args["path"], args["content"]),
        "read_file": lambda args: read_file(args["path"]),
        "delete_file": lambda args: delete_file(args["path"]),
        "list_files": lambda args: list_files(args.get("path", ".")),
        "edit_file": lambda args: edit_file(args["path"], args["content"]),
        "edit_replace_file": lambda args: edit_replace_file(args["path"], args["old_content"], args["new_content"])
    }

    if name not in tool_map:
        raise ValueError(f"Tool '{name}' not found")
    
    try:
        result = tool_map[name](arguments)
        
    except Exception as e:
        result = {"success": False, "error": str(e)}

    return [types.TextContent(type = "text", text=json.dumps(result))]


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="filesystem-agent",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
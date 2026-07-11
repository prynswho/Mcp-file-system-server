from mcp.server.fastmcp import FastMCP
import inspect
from .tools.file_system import (
    create_folder as create_folder_impl,
    write_file as write_file_impl,
    read_file as read_file_impl,
    delete_file as delete_file_impl,
    list_files as list_files_impl,
    edit_file as edit_file_impl,
    edit_replace_file as edit_replace_file_impl,
)

mcp = FastMCP("filesystem")

@mcp.tool()
def create_folder(path:str) -> dict:
    return create_folder_impl(path)

@mcp.tool()
def write_file(path:str, content:str) -> dict:
    return write_file_impl(path, content)

@mcp.tool()
def read_file(path:str) -> dict:
    return read_file_impl(path)

@mcp.tool()
def delete_file(path:str) -> dict:
    return delete_file_impl(path)

@mcp.tool()
def list_files(path:str = ".") -> dict:
    return list_files_impl(path)


@mcp.tool()
def edit_file(path:str, content:str) -> dict:
    return edit_file_impl(path, content)

@mcp.tool()
def edit_replace_file(path:str,new_content:str,old_content:str) -> dict:
    return edit_replace_file_impl(path,new_content,old_content)

if __name__ == "__main__":
    print("mcp server running .....")
    print(inspect.signature(FastMCP.run)) 
    # this will run on 8000
    mcp.run(transport="streamable-http", )
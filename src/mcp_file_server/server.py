from mcp.server import MCPServer

from .filesystem import (
    create_text_file,
    read_text_file,
    read_multiple_files,
    write_file,
    edit_file,
    str_replace,
    delete,
    create_directory,
    list_directory,
    list_directory_with_sizes,
    move_file,
    search_files,
    list_allowed_directories,
    get_file_info,
    git_status,
    git_diff,
    checkpoint,
    read_project_state,
)


mcp = MCPServer("MCP File Server")

mcp.tool()(create_text_file)

mcp.tool()(read_text_file)

mcp.tool()(read_multiple_files)

mcp.tool()(write_file)

mcp.tool()(edit_file)

mcp.tool()(str_replace)

mcp.tool()(delete)

mcp.tool()(create_directory)

mcp.tool()(list_directory)

mcp.tool()(list_directory_with_sizes)

mcp.tool()(move_file)

mcp.tool()(search_files)

mcp.tool()(list_allowed_directories)

mcp.tool()(get_file_info)

mcp.tool()(git_status)

mcp.tool()(git_diff)

mcp.tool()(checkpoint)

mcp.tool()(read_project_state)


if __name__ == "__main__":
    mcp.run()
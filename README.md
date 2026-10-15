# MCP File Server Connector

## 1. Project Information

- **Project Title:** Build Your Own MCP File Server Connector
- **Course and Section:** BSCS-3A
- **Document Reference:** CS3-WK06-MCP - Midterms PT. 1
- **Programming Language:** Python 3.11
- **Protocol:** Model Context Protocol (MCP)

## 2. Project Description

The MCP File Server Connector is a Python-based application that allows AI clients to manage files through the Model Context Protocol (MCP).

The system provides tools for creating, reading, writing, editing, moving, searching, and deleting files. It also supports directory management, file information, basic Git operations, and project checkpoints.

To protect files, the server restricts file operations to the designated workspace, `D:\Midterms`. It also supports local connections through STDIO and remote connections through Streamable HTTP over HTTPS using ngrok and Basic Authentication.

## 3. Project Objectives

The project aims to:

1. Develop an MCP server that allows AI clients to perform file-management operations.
2. Restrict file access to an approved workspace.
3. Validate tool inputs to reduce invalid requests.
4. Support local and remote MCP connections.
5. Test the server's functionality and security.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11 | Main programming language |
| MCP SDK | Connects AI clients to the server's tools |
| Pydantic | Validates selected tool inputs |
| pytest | Runs automated tests |
| Git | Tracks project changes |
| ngrok | Provides an HTTPS tunnel for remote access |
| Windows Task Scheduler | Starts the server and tunnel at user logon |

## 5. Main Features

- **File Management:** Create, read, write, edit, move, and delete files.
- **Directory Management:** Create directories and list their contents.
- **File Search:** Search for text within files.
- **File Information:** Retrieve file details, including size information.
- **Git Tools:** Check repository status and view changes.
- **Workspace Security:** Reject paths that point outside the approved directory.
- **Input Validation:** Check selected tool inputs before processing them.
- **Local Connection:** Connect through STDIO using an MCP-compatible client.
- **Remote Connection:** Connect through Streamable HTTP using an HTTPS tunnel.
- **Project Tracking:** Record checkpoints and read project-state information.

## 6. Available MCP Tools

The server registers 18 tools.

| No. | Tool Name | Description |
|---:|---|---|
| 1 | `create_text_file` | Creates a text file with the provided content. |
| 2 | `read_text_file` | Reads the contents of a text file. |
| 3 | `read_multiple_files` | Reads multiple files. |
| 4 | `write_file` | Writes content to a file. |
| 5 | `edit_file` | Replaces specified text in a file. |
| 6 | `str_replace` | Performs a string replacement in a file. |
| 7 | `delete` | Deletes a supported file or filesystem target. |
| 8 | `create_directory` | Creates a directory. |
| 9 | `list_directory` | Lists the contents of a directory. |
| 10 | `list_directory_with_sizes` | Lists directory contents with file sizes. |
| 11 | `move_file` | Moves a file to another location. |
| 12 | `search_files` | Searches files for a specified text query. |
| 13 | `list_allowed_directories` | Shows the allowed workspace directory. |
| 14 | `get_file_info` | Retrieves information about a file. |
| 15 | `git_status` | Shows the Git repository status. |
| 16 | `git_diff` | Shows changes tracked by Git. |
| 17 | `checkpoint` | Records a project checkpoint. |
| 18 | `read_project_state` | Reads the project's current state information. |

## 7. Project Structure

```text
MCP-File-Server/
├── mcp_launcher.py
├── mcp_http_launcher.py
├── pyproject.toml
├── uv.lock
├── scripts/
│   └── start-http.ps1
├── src/
│   └── mcp_file_server/
│       ├── __init__.py
│       ├── filesystem.py
│       ├── security.py
│       ├── server.py
│       └── validation.py
├── tests/
│   ├── test_security.py
│   └── test_validation.py
├── PROJECT_STATE.md
├── PLAN_LOG.md
├── CHECKPOINTS.md
├── DECISIONS.md
└── README.md
```

## 8. Installation and Setup

### Requirements

- Windows operating system
- Python 3.11
- Git
- Project dependencies listed in `pyproject.toml`
- ngrok for remote access

### Installation Steps

Open PowerShell and navigate to the project directory:

```powershell
cd D:\MCP-File-Server
```

Create a virtual environment if one does not already exist:

```powershell
py -3.11 -m venv .venv
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project and its dependencies:

```powershell
python -m pip install -e .
```

Create the approved workspace if necessary:

```powershell
New-Item -ItemType Directory -Force -Path D:\Midterms
```

## 9. Running the Server

### Local Connection Through STDIO

The STDIO launcher is intended for local MCP clients.

Run these commands from the project directory:

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) "src")
.\.venv\Scripts\python.exe .\mcp_launcher.py
```

Configure the MCP client to use the project's Python environment and `mcp_launcher.py`.

### HTTP Connection

The HTTP server uses Streamable HTTP and listens locally at:

`http://127.0.0.1:8000`

The MCP endpoint is:

`http://127.0.0.1:8000/mcp`

To start the HTTP server manually:

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) "src")
.\.venv\Scripts\python.exe .\mcp_http_launcher.py
```

Keep the terminal open while the server is running. Press `Ctrl+C` to stop it.

### Remote Connection Through HTTPS

The remote setup uses ngrok to provide an HTTPS address for the local server.

The endpoint follows this format:

`https://YOUR_NGROK_DOMAIN/mcp`

Replace `YOUR_NGROK_DOMAIN` with the domain configured for the deployment. Remote access uses Basic Authentication, so valid credentials are required.

Authentication credentials must be kept private and must not be included in the README or public repository.

## 10. Security Measures

The server uses `D:\Midterms` as its approved workspace.

The following measures help protect files:

1. Paths are checked before filesystem operations.
2. Requests that resolve outside the approved workspace are rejected.
3. Selected tool inputs are validated using Pydantic.
4. Remote connections use HTTPS through ngrok and require Basic Authentication.
5. Authentication credentials must remain private.

These measures help reduce unauthorized file access. The server should still be used with appropriate Windows permissions and secure credential management.

## 11. Automatic Startup

Windows Task Scheduler is configured to start the HTTP server and ngrok at user logon.

The configured tasks are:

- `MCP File Server HTTP`
- `MCP File Server ngrok`

The HTTP startup script is located at:

`scripts\start-http.ps1`

The HTTP server log is stored at:

`%LOCALAPPDATA%\MCP-File-Server\logs\http-server.log`

Automatic startup depends on the computer, network connection, task settings, and tunnel configuration.

## 12. Testing

Run the automated tests from the project directory:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

The tests cover workspace security and input validation.

The following checks are also used to verify the setup:

1. Create and read a file inside the approved workspace.
2. Attempt to access a path outside the workspace and confirm that the request is rejected.
3. Check that the local HTTP server is listening on port 8000.
4. Test authenticated access to the remote endpoint.
5. Connect through an MCP-compatible client and test the available tools.

## 13. Project Status

The project has been configured and tested for local file operations, sandbox path rejection, remote HTTP access, and automatic startup after Windows logon.

The automated tests cover sandbox security and input validation. Additional testing may be performed to verify each tool and the complete remote connection workflow.

## 14. Conclusion

The MCP File Server Connector demonstrates how an MCP server can provide file-management tools to AI clients. It combines filesystem operations, input validation, workspace restrictions, local and remote communication, and automated testing in one Python project.

The project provides a foundation for connecting AI clients to file operations while limiting access to an approved workspace.

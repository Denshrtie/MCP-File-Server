# PLAN_LOG.md

## Project Development Log

### 1. Project Setup

- Created the project directory at `D:\MCP-File-Server`.
- Set up a Python virtual environment.
- Installed the required Python MCP package and testing tools.
- Created the source code and test directories.
- Configured `D:\Midterms` as the allowed workspace.

### 2. File Access and Security

- Implemented path validation in `security.py`.
- Configured the server to reject paths outside the allowed workspace.
- Implemented file creation and reading tools.
- Tested successful file creation and reading.
- Tested a path outside the workspace and confirmed that the server rejected the request.

### 3. MCP Server Setup

- Configured the MCP server using the Python MCP package.
- Set up the local STDIO connection for Claude Desktop.
- Configured the HTTP server to use Streamable HTTP.
- Confirmed that the server could list its registered tools.
- Retained the existing STDIO configuration as a local alternative.

### 4. Remote Access Setup

- Configured ngrok to provide an HTTPS endpoint for the MCP server.
- Added Basic Authentication to protect remote access.
- Validated the ngrok configuration.
- Tested the remote endpoint and received a successful HTTP response.

### 5. Automatic Startup

- Created a Windows Task Scheduler task for the HTTP server.
- Created a separate task for ngrok.
- Updated the HTTP startup script to handle server output correctly.
- Restarted Windows and checked the HTTP server and ngrok task.
- Confirmed that the HTTP server was listening on port 8000 and the ngrok task was running after restart.

### 6. Client Testing

- Used Claude to create `mcp_test.txt` inside `D:\Midterms`.
- Checked the file contents to confirm that the write operation succeeded.
- Asked Claude to create a file outside the allowed workspace.
- Confirmed that the server returned a `sandbox_violation` error and rejected the request.
# CHECKPOINTS.md

## Project Testing Checkpoints

### Checkpoint 1: Sandbox Configuration

**Status:** Passed

- Configured `D:\Midterms` as the allowed workspace.
- Implemented path validation to prevent access outside the workspace.
- Confirmed that paths resolving outside the sandbox are rejected.

### Checkpoint 2: File Operations

**Status:** Passed for tested operations

- Tested file creation through an MCP tool.
- Tested reading an existing text file.
- Confirmed that a missing file returns a file-not-found error.
- Confirmed that file operations can access files inside the allowed workspace.

### Checkpoint 3: Security Testing

**Status:** Passed

- Attempted to create a file outside `D:\Midterms`.
- The server returned a `sandbox_violation` error.
- Confirmed that the requested file was not created outside the allowed workspace.

### Checkpoint 4: MCP Client Integration

**Status:** Passed

- Connected the MCP server to Claude Desktop using the existing local STDIO configuration.
- Used Claude to create `mcp_test.txt` inside the allowed workspace.
- Verified that the file was created successfully and contained the requested text.

### Checkpoint 5: Remote Access

**Status:** Passed for the tested endpoint

- Configured Streamable HTTP for remote MCP access.
- Configured ngrok to expose the local server through HTTPS.
- Enabled Basic Authentication for the remote endpoint.
- Confirmed that an authenticated request reached the server and returned HTTP 200.

### Checkpoint 6: Automatic Startup

**Status:** Passed in the restart test

- Created separate Windows Task Scheduler tasks for the HTTP server and ngrok.
- Restarted Windows.
- Confirmed that the HTTP server was listening on port 8000.
- Confirmed that the ngrok task was running after restart.
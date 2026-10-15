# DECISIONS.md

## Project Design Decisions

### 1. Runtime and SDK: Python with the Official MCP SDK

- Python was selected because it provides a straightforward environment for implementing file operations, input validation, and automated testing.
- The official Python MCP SDK was chosen to register tools and enable communication between the MCP server and compatible clients.
- The implementation uses `MCPServer` to define and manage the server's MCP tools.

### 2. Transport: Streamable HTTP with STDIO Support

- Streamable HTTP was selected as the primary transport because it allows remote MCP clients to communicate with the server through an HTTP endpoint.
- STDIO was retained as a local connection method for Claude Desktop, providing an alternative way to access the server without relying on the remote endpoint.
- Supporting both transports makes the server suitable for local development and remote access.

### 3. Input Validation and Sandbox Security

- File paths are validated before file operations are performed to ensure that requests remain within the designated workspace.
- The sandbox root is set to `D:\Midterms`, and paths that resolve outside this directory are rejected.
- Path validation helps prevent directory traversal and unauthorized access to files outside the permitted workspace.
- Invalid requests and file-related errors are handled with appropriate error responses, allowing clients to understand why an operation failed.
- Python's validation capabilities and the MCP SDK's tool input handling support structured tool requests and more predictable server behavior.

### 4. Remote Exposure: ngrok with HTTPS and Basic Authentication

- ngrok was selected to expose the locally hosted MCP server through a public HTTPS endpoint without requiring a separate cloud server.
- A static ngrok domain provides a consistent endpoint for remote MCP client configuration.
- Basic Authentication adds an access-control layer so that requests must provide valid credentials to reach the protected endpoint.
- HTTPS protects data in transit between the remote client and the ngrok endpoint.
- This approach provides a practical way to demonstrate remote MCP access while keeping the server hosted on the Windows machine.

### 5. Process Management: Windows Task Scheduler

- Windows Task Scheduler was selected to launch the HTTP server and ngrok automatically at user logon.
- Separate scheduled tasks allow the two components to start independently without requiring the user to launch each one manually.
- This approach uses Windows' built-in scheduling functionality and avoids introducing additional process-management software.
- The startup configuration was tested after restarting Windows to confirm that the HTTP server and ngrok could start automatically.
- Task Scheduler simplifies startup management, while process monitoring and automatic recovery remain separate considerations from launching applications at logon.

### 6. Version Control: Git

- Git was selected as the version control system for tracking changes to the source code and project documentation.
- Version control helps maintain a history of development, making it easier to review modifications and restore earlier versions when necessary.
- Git also supports collaboration by allowing project changes to be organized into commits and shared through a repository.

### 7. Testing: Automated Tests and Real MCP Client Testing

- Automated tests are used to check important security behavior and ensure that path validation works as intended.
- Manual testing of file operations helps confirm that the server can create and read files within the permitted workspace.
- Claude Desktop is used as a real MCP client to demonstrate tool invocation and verify that the server responds to client requests.
- Security testing includes attempting to create a file outside the sandbox and confirming that the server rejects the request.
- Remote endpoint testing checks connectivity, authentication, and the server's HTTP response.
- Testing through both automated checks and a real client provides evidence of the server's behavior under different conditions.

### 8. File Access and Operation Design

- File operations are restricted to the designated workspace to reduce the risk of unintended changes to other files on the host machine.
- The server provides tools for interacting with workspace files through MCP requests.
- File-related errors, such as missing files and rejected paths, are returned as structured responses to make failures easier to understand.
- Keeping file operations within the sandbox establishes a clear security boundary for clients using the server.

### 9. Project Handoff Documentation

- `PROJECT_STATE.md` records the project's purpose, configuration, current status, and important setup details.
- `PLAN_LOG.md` documents the major development steps and implementation progress.
- `CHECKPOINTS.md` records completed tests and their results.
- `DECISIONS.md` explains the technology choices and design reasoning behind the implementation.
- Maintaining these files helps preserve project information between development sessions and supports a consistent handoff to another agent or developer.

## Security Considerations

- The server restricts file operations to `D:\Midterms` through path validation.
- Requests that resolve outside the sandbox are rejected.
- Remote access is protected by HTTPS through ngrok and Basic Authentication.
- Authentication credentials are kept private and excluded from public project documentation.
- The existing Claude Desktop STDIO configuration is retained as a local alternative to remote access.

## Conclusion

The selected technology stack combines Python, the official MCP SDK, Streamable HTTP, ngrok, Windows Task Scheduler, Git, and automated testing. These choices support the development of a self-hosted MCP File Server that can provide controlled file access to compatible clients locally and remotely. The design emphasizes workspace isolation, authenticated remote connectivity, practical deployment on Windows, and documentation that supports continued development.
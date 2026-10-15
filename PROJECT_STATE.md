# PROJECT_STATE.md

## 1. Project Information

**Project Title:** Build Your Own MCP File Server Connector  
**Course & Section:** BSCS-3A  
**Document Reference:** CS3-WK06-MCP - Midterms PT. 1  

## 2. Project Overview

This project is a file server that allows AI agents to create, read, and manage files through the Model Context Protocol (MCP).

The server uses a restricted workspace to prevent access to files outside the allowed directory. It also supports remote connections through HTTPS and uses automatic startup settings in Windows Task Scheduler.

## 3. Project Setup

- **Operating System:** Windows
- **Programming Language:** Python 3.11.9
- **MCP Package:** `mcp` 2.3.0
- **Project Directory:** `D:\MCP-File-Server`
- **Python Virtual Environment:** `D:\MCP-File-Server\.venv`
- **Allowed Workspace:** `D:\Midterms`
- **HTTP Launcher:** `D:\MCP-File-Server\mcp_http_launcher.py`
- **HTTP Startup Script:** `D:\MCP-File-Server\scripts\start-http.ps1`
- **Local Server Address:** `http://127.0.0.1:8000`
- **Remote Server Address:** `https://appetizer-error-thank.ngrok-free.dev/mcp`
- **Remote Access:** HTTPS through ngrok with Basic Authentication
- **Automatic Startup:** Windows Task Scheduler

## 4. Completed Work and Test Results

The following tasks have been completed and tested:

1. Set `D:\Midterms` as the allowed workspace/sandbox root.
2. Added path validation to reject requests that point outside the workspace.
3. Used Claude to create `mcp_test.txt` inside `D:\Midterms`.
4. Tested an attempt to create a file outside the workspace. The server rejected it with a `sandbox_violation` error.
5. Configured the HTTP server to use Streamable HTTP.
6. Configured ngrok to provide an HTTPS address for remote access.
7. Tested the remote endpoint with Basic Authentication and received an HTTP `200 OK` response with `text/event-stream`.
8. Configured separate Task Scheduler tasks for the HTTP server and ngrok.
9. Restarted Windows and confirmed that the HTTP server was listening on port 8000 and the ngrok task was running.
10. Kept the existing Claude Desktop STDIO configuration as a local alternative.

## 5. Security Measures

- The server is restricted to `D:\Midterms`.
- Requests to access paths outside the workspace is rejected.
- Remote access is protected by Basic Authentication.
- The server uses HTTPS through ngrok for remote connections.
- Passwords and authentication tokens is not included in public documentation or committed to the repository.
- Security checks remains enabled during testing and normal use.
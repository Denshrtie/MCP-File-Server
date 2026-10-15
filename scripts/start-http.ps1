$ProjectRoot = "D:\MCP-File-Server"
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$LogDir = Join-Path $env:LOCALAPPDATA "MCP-File-Server\logs"
$LogFile = Join-Path $LogDir "http-server.log"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$env:PYTHONPATH = Join-Path $ProjectRoot "src"
Set-Location $ProjectRoot

& $Python (Join-Path $ProjectRoot "mcp_http_launcher.py") *>> $LogFile

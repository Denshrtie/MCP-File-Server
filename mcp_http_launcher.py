
from mcp_file_server.server import mcp
from mcp.server.transport_security import TransportSecuritySettings


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
        stateless_http=True,
        json_response=True,
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=[
                "127.0.0.1:*",
                "localhost:*",
                "appetizer-error-thank.ngrok-free.dev",
                "appetizer-error-thank.ngrok-free.dev:443",
            ],
        ),
    )

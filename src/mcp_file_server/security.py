from pathlib import Path


# The only directory the MCP server is allowed to access.
SANDBOX_ROOT = Path(r"D:\Midterms").resolve()


class SandboxViolation(Exception):
    """Raised when a requested path escapes the sandbox."""
    

def resolve_safe_path(user_path: str) -> Path:
    """
    Resolve a user-supplied path inside the configured sandbox.

    Relative paths are interpreted relative to SANDBOX_ROOT.
    Absolute paths are accepted only when they are already inside
    SANDBOX_ROOT.

    Any path that resolves outside the sandbox is rejected.
    """
    if not isinstance(user_path, str) or not user_path.strip():
        raise ValueError("Path must be a non-empty string.")

    requested = Path(user_path)

    if requested.is_absolute():
        candidate = requested
    else:
        candidate = SANDBOX_ROOT / requested

    try:
        resolved = candidate.resolve()
    except OSError as exc:
        raise SandboxViolation(
            f"Unable to resolve path: {user_path}"
        ) from exc

    try:
        resolved.relative_to(SANDBOX_ROOT)
    except ValueError as exc:
        raise SandboxViolation(
            f"Access denied: path escapes the sandbox root "
            f"'{SANDBOX_ROOT}'."
        ) from exc

    return resolved
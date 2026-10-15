
from pathlib import Path

from pydantic import ValidationError

from .validation import PathInput


# The only directory the MCP server is allowed to access.
SANDBOX_ROOT = Path(r"D:\Midterms").resolve()


class SandboxViolation(Exception):
    """Raised when a requested path escapes the sandbox."""


def resolve_safe_path(user_path: str) -> Path:
    """
    Validate and resolve a user-supplied path inside the sandbox.

    Relative paths are resolved against SANDBOX_ROOT.
    Absolute paths are accepted only when they remain inside
    SANDBOX_ROOT.

    Invalid paths are rejected through Pydantic validation.
    Paths outside the sandbox raise SandboxViolation.
    """
    try:
        user_path = PathInput(path=user_path).path
    except ValidationError as exc:
        raise ValueError(
            "Path must be a non-empty string no longer than 1024 characters."
        ) from exc

    requested = Path(user_path)

    if requested.is_absolute():
        candidate = requested
    else:
        candidate = SANDBOX_ROOT / requested

    try:
        resolved = candidate.resolve()
    except (OSError, RuntimeError) as exc:
        raise SandboxViolation(
            f"Unable to resolve path: {user_path}"
        ) from exc

    try:
        resolved.relative_to(SANDBOX_ROOT)
    except ValueError as exc:
        raise SandboxViolation(
            f"Access denied. Path is outside the sandbox root "
            f"'{SANDBOX_ROOT}'."
        ) from exc

    return resolved

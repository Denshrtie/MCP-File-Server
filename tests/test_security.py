import pytest

from mcp_file_server.security import (
    SANDBOX_ROOT,
    SandboxViolation,
    resolve_safe_path,
)


def test_relative_path_stays_inside_sandbox():
    result = resolve_safe_path("example.txt")

    assert result == SANDBOX_ROOT / "example.txt"


def test_nested_relative_path_stays_inside_sandbox():
    result = resolve_safe_path("notes/example.txt")

    assert result == SANDBOX_ROOT / "notes" / "example.txt"


def test_absolute_path_inside_sandbox_is_allowed():
    path = SANDBOX_ROOT / "example.txt"

    result = resolve_safe_path(str(path))

    assert result == path


def test_parent_directory_escape_is_rejected():
    with pytest.raises(SandboxViolation):
        resolve_safe_path("..\\outside.txt")


def test_absolute_path_outside_sandbox_is_rejected():
    with pytest.raises(SandboxViolation):
        resolve_safe_path(r"C:\Windows\System32\test.txt")


def test_empty_path_is_rejected():
    with pytest.raises(ValueError):
        resolve_safe_path("")
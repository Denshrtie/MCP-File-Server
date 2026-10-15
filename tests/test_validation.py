import pytest
from pydantic import ValidationError

from mcp_file_server.validation import (
    FileContentInput,
    PathInput,
    SearchInput,
)


def test_valid_path_is_accepted():
    result = PathInput(path="notes/example.txt")

    assert result.path == "notes/example.txt"


def test_empty_path_is_rejected():
    with pytest.raises(ValidationError):
        PathInput(path="")


def test_whitespace_only_path_is_rejected():
    with pytest.raises(ValidationError):
        PathInput(path="   ")


def test_path_over_1024_characters_is_rejected():
    with pytest.raises(ValidationError):
        PathInput(path="a" * 1025)


def test_file_content_input_accepts_valid_content():
    result = FileContentInput(
        path="example.txt",
        content="Hello, MCP!",
    )

    assert result.content == "Hello, MCP!"


def test_search_query_must_not_be_empty():
    with pytest.raises(ValidationError):
        SearchInput(query="")


def test_search_query_over_1000_characters_is_rejected():
    with pytest.raises(ValidationError):
        SearchInput(query="a" * 1001)


def test_search_path_defaults_to_current_directory():
    result = SearchInput(query="example")

    assert result.path == "."
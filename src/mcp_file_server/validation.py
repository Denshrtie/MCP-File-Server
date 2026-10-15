from pydantic import BaseModel, ConfigDict, Field, field_validator


class PathInput(BaseModel):
    """Validate a required file-system path."""

    model_config = ConfigDict(str_strip_whitespace=True)

    path: str = Field(min_length=1, max_length=1024)

    @field_validator("path")
    @classmethod
    def reject_blank_path(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Path must not be blank.")
        return value


class FileContentInput(PathInput):
    """Validate a path and text content."""

    content: str = Field(max_length=1_000_000)


class SearchInput(BaseModel):
    """Validate a text search request."""

    model_config = ConfigDict(str_strip_whitespace=True)

    query: str = Field(min_length=1, max_length=1000)
    path: str = Field(default=".", min_length=1, max_length=1024)
class TextReplacementInput(PathInput):
    """Validate text replacement input."""

    old_text: str = Field(min_length=1, max_length=1_000_000)
    new_text: str = Field(max_length=1_000_000)


class CheckpointInput(BaseModel):
    """Validate a checkpoint message."""

    model_config = ConfigDict(str_strip_whitespace=True)

    message: str = Field(min_length=1, max_length=10_000)

    @field_validator("message")
    @classmethod
    def reject_blank_message(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Checkpoint message must not be blank.")
        return value

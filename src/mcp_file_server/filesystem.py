from pathlib import Path
import shutil
import subprocess

from pydantic import ValidationError

from .security import SandboxViolation, resolve_safe_path
from .validation import (
    CheckpointInput,
    FileContentInput,
    SearchInput,
    TextReplacementInput,
)


# create_text_file
def create_text_file(
    path: str,
    content: str,
) -> dict:
    """Create a new UTF-8 text file inside the sandbox."""

    try:
        validated = FileContentInput(path=path, content=content)
        path, content = validated.path, validated.content
        target = resolve_safe_path(path)

        if target.exists():
            return {
                "success": False,
                "error": "file_exists",
                "message": f"File already exists: {path}",
            }

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "path": str(target),
            "message": "Text file created successfully.",
        }

    except ValidationError as exc:
        return {
            "success": False,
            "error": "validation_error",
            "message": "; ".join(
                f"{'.'.join(str(part) for part in item['loc'])}: {item['msg']}"
                for item in exc.errors()
            ),
        }

    except SandboxViolation as exc:
        return {
            "success": False,
            "error": "sandbox_violation",
            "message": str(exc),
        }

    except OSError as exc:
        return {
            "success": False,
            "error": "filesystem_error",
            "message": str(exc),
        }


# read_text_file
def read_text_file(
    path: str,
) -> dict:
    """Read a UTF-8 text file from inside the sandbox."""

    try:
        target = resolve_safe_path(path)

        if not target.exists():
            return {
                "success": False,
                "error": "file_not_found",
                "message": f"File does not exist: {path}",
            }

        if not target.is_file():
            return {
                "success": False,
                "error": "not_a_file",
                "message": f"Path is not a file: {path}",
            }

        content = target.read_text(encoding="utf-8")

        return {
            "success": True,
            "path": str(target),
            "content": content,
        }

    except SandboxViolation as exc:
        return {
            "success": False,
            "error": "sandbox_violation",
            "message": str(exc),
        }

    except UnicodeDecodeError:
        return {
            "success": False,
            "error": "invalid_text_encoding",
            "message": f"File is not valid UTF-8 text: {path}",
        }

    except OSError as exc:
        return {
            "success": False,
            "error": "filesystem_error",
            "message": str(exc),
        }


# read_multiple_files
def read_multiple_files(
    paths: list[str],
) -> dict:
    """Read multiple UTF-8 text files from inside the sandbox."""

    results = []

    for path in paths:
        try:
            target = resolve_safe_path(path)

            if not target.exists():
                results.append({
                    "success": False,
                    "path": path,
                    "error": "file_not_found",
                    "message": f"File does not exist: {path}",
                })
                continue

            if not target.is_file():
                results.append({
                    "success": False,
                    "path": path,
                    "error": "not_a_file",
                    "message": f"Path is not a file: {path}",
                })
                continue

            content = target.read_text(encoding="utf-8")

            results.append({
                "success": True,
                "path": str(target),
                "content": content,
            })

        except SandboxViolation as exc:
            results.append({
                "success": False,
                "path": path,
                "error": "sandbox_violation",
                "message": str(exc),
            })

        except UnicodeDecodeError:
            results.append({
                "success": False,
                "path": path,
                "error": "invalid_text_encoding",
                "message": f"File is not valid UTF-8 text: {path}",
            })

        except OSError as exc:
            results.append({
                "success": False,
                "path": path,
                "error": "filesystem_error",
                "message": str(exc),
            })

    return {
        "success": True,
        "count": len(results),
        "files": results,
    }


# write_file
def write_file(
    path: str,
    content: str,
) -> dict:
    """Create or overwrite a UTF-8 text file inside the sandbox."""

    try:
        validated = FileContentInput(path=path, content=content)
        path, content = validated.path, validated.content
        target = resolve_safe_path(path)

        if target.exists() and not target.is_file():
            return {
                "success": False,
                "error": "not_a_file",
                "message": f"Path is not a file: {path}",
            }

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "path": str(target),
            "message": "File written successfully.",
        }

    except ValidationError as exc:
        return {
            "success": False,
            "error": "validation_error",
            "message": "; ".join(
                f"{'.'.join(str(part) for part in item['loc'])}: {item['msg']}"
                for item in exc.errors()
            ),
        }

    except SandboxViolation as exc:
        return {
            "success": False,
            "error": "sandbox_violation",
            "message": str(exc),
        }

    except OSError as exc:
        return {
            "success": False,
            "error": "filesystem_error",
            "message": str(exc),
        }


# edit_file
def edit_file(
    path: str,
    old_text: str,
    new_text: str,
) -> dict:
    """Replace one exact section of a UTF-8 text file."""

    try:
        validated = TextReplacementInput(
            path=path, old_text=old_text, new_text=new_text
        )
        path, old_text, new_text = (
            validated.path, validated.old_text, validated.new_text
        )
        target = resolve_safe_path(path)

        if not target.exists():
            return {
                "success": False,
                "error": "file_not_found",
                "message": f"File does not exist: {path}",
            }

        if not target.is_file():
            return {
                "success": False,
                "error": "not_a_file",
                "message": f"Path is not a file: {path}",
            }

        content = target.read_text(encoding="utf-8")

        occurrences = content.count(old_text)

        if occurrences == 0:
            return {
                "success": False,
                "error": "text_not_found",
                "message": "The specified text was not found.",
            }

        if occurrences > 1:
            return {
                "success": False,
                "error": "multiple_matches",
                "message": "The specified text occurs more than once.",
            }

        updated = content.replace(old_text, new_text, 1)
        target.write_text(updated, encoding="utf-8")

        return {
            "success": True,
            "path": str(target),
            "message": "File edited successfully.",
        }

    except ValidationError as exc:
        return {
            "success": False,
            "error": "validation_error",
            "message": "; ".join(
                f"{'.'.join(str(part) for part in item['loc'])}: {item['msg']}"
                for item in exc.errors()
            ),
        }

    except SandboxViolation as exc:
        return {
            "success": False,
            "error": "sandbox_violation",
            "message": str(exc),
        }

    except UnicodeDecodeError:
        return {
            "success": False,
            "error": "invalid_text_encoding",
            "message": f"File is not valid UTF-8 text: {path}",
        }

    except OSError as exc:
        return {
            "success": False,
            "error": "filesystem_error",
            "message": str(exc),
        }


# str_replace
def str_replace(
    path: str,
    old_text: str,
    new_text: str,
) -> dict:
    """Replace an exact string in a UTF-8 text file."""

    return edit_file(path, old_text, new_text)


# delete
def delete(
    path: str,
) -> dict:
    """Delete a file or an empty directory inside the sandbox."""

    try:
        target = resolve_safe_path(path)

        if not target.exists():
            return {
                "success": False,
                "error": "not_found",
                "message": f"Path does not exist: {path}",
            }

        if target.is_file():
            target.unlink()

            return {
                "success": True,
                "path": str(target),
                "message": "File deleted successfully.",
            }

        if target.is_dir():
            try:
                target.rmdir()
            except OSError:
                return {
                    "success": False,
                    "error": "directory_not_empty",
                    "message": f"Directory is not empty: {path}",
                }

            return {
                "success": True,
                "path": str(target),
                "message": "Directory deleted successfully.",
            }

        return {
            "success": False,
            "error": "unsupported_path",
            "message": f"Unsupported path type: {path}",
        }

    except SandboxViolation as exc:
        return {
            "success": False,
            "error": "sandbox_violation",
            "message": str(exc),
        }

    except OSError as exc:
        return {
            "success": False,
            "error": "filesystem_error",
            "message": str(exc),
        }


# create_directory
def create_directory(
    path: str,
) -> dict:
    """Create a directory inside the sandbox."""

    try:
        target = resolve_safe_path(path)

        if target.exists():
            if target.is_dir():
                return {
                    "success": False,
                    "error": "directory_exists",
                    "message": f"Directory already exists: {path}",
                }

            return {
                "success": False,
                "error": "path_exists",
                "message": f"A file already exists at: {path}",
            }

        target.mkdir(parents=True)

        return {
            "success": True,
            "path": str(target),
            "message": "Directory created successfully.",
        }

    except SandboxViolation as exc:
        return {
            "success": False,
            "error": "sandbox_violation",
            "message": str(exc),
        }

    except OSError as exc:
        return {
            "success": False,
            "error": "filesystem_error",
            "message": str(exc),
        }


# list_directory
def list_directory(
    path: str = ".",
) -> dict:
    """List files and directories inside a sandbox directory."""

    try:
        target = resolve_safe_path(path)

        if not target.exists():
            return {
                "success": False,
                "error": "not_found",
                "message": f"Directory does not exist: {path}",
            }

        if not target.is_dir():
            return {
                "success": False,
                "error": "not_a_directory",
                "message": f"Path is not a directory: {path}",
            }

        entries = []

        for item in sorted(target.iterdir(), key=lambda p: p.name.lower()):
            entries.append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
            })

        return {
            "success": True,
            "path": str(target),
            "entries": entries,
        }

    except SandboxViolation as exc:
        return {
            "success": False,
            "error": "sandbox_violation",
            "message": str(exc),
        }

    except OSError as exc:
        return {
            "success": False,
            "error": "filesystem_error",
            "message": str(exc),
        }


# list_directory_with_sizes
def list_directory_with_sizes(
    path: str = ".",
) -> dict:
    """List directory contents and include file sizes."""

    try:
        target = resolve_safe_path(path)

        if not target.exists():
            return {
                "success": False,
                "error": "not_found",
                "message": f"Directory does not exist: {path}",
            }

        if not target.is_dir():
            return {
                "success": False,
                "error": "not_a_directory",
                "message": f"Path is not a directory: {path}",
            }

        entries = []

        for item in sorted(target.iterdir(), key=lambda p: p.name.lower()):
            if item.is_file():
                size = item.stat().st_size
                entry_type = "file"
            else:
                size = None
                entry_type = "directory"

            entries.append({
                "name": item.name,
                "type": entry_type,
                "size_bytes": size,
            })

        return {
            "success": True,
            "path": str(target),
            "entries": entries,
        }

    except SandboxViolation as exc:
        return {
            "success": False,
            "error": "sandbox_violation",
            "message": str(exc),
        }

    except OSError as exc:
        return {
            "success": False,
            "error": "filesystem_error",
            "message": str(exc),
        }


# move_file
def move_file(
    source: str,
    destination: str,
) -> dict:
    """Move or rename a file or directory within the sandbox."""

    try:
        source_path = resolve_safe_path(source)
        destination_path = resolve_safe_path(destination)

        if not source_path.exists():
            return {
                "success": False,
                "error": "source_not_found",
                "message": f"Source does not exist: {source}",
            }

        if destination_path.exists():
            return {
                "success": False,
                "error": "destination_exists",
                "message": f"Destination already exists: {destination}",
            }

        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source_path), str(destination_path))

        return {
            "success": True,
            "source": str(source_path),
            "destination": str(destination_path),
            "message": "Path moved successfully.",
        }

    except SandboxViolation as exc:
        return {
            "success": False,
            "error": "sandbox_violation",
            "message": str(exc),
        }

    except OSError as exc:
        return {
            "success": False,
            "error": "filesystem_error",
            "message": str(exc),
        }


# search_files
def search_files(
    query: str,
    path: str = ".",
) -> dict:
    """Search UTF-8 text files recursively for a string."""

    try:
        validated = SearchInput(query=query, path=path)
        query, path = validated.query, validated.path
        root = resolve_safe_path(path)

        if not root.exists():
            return {
                "success": False,
                "error": "not_found",
                "message": f"Search path does not exist: {path}",
            }

        if root.is_file():
            files = [root]
        else:
            files = [
                item
                for item in root.rglob("*")
                if item.is_file()
            ]

        matches = []

        for file_path in files:
            try:
                content = file_path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

            for line_number, line in enumerate(
                content.splitlines(),
                start=1,
            ):
                if query.lower() in line.lower():
                    matches.append({
                        "path": str(file_path),
                        "line": line_number,
                        "text": line,
                    })

        return {
            "success": True,
            "query": query,
            "count": len(matches),
            "matches": matches,
        }

    except ValidationError as exc:
        return {
            "success": False,
            "error": "validation_error",
            "message": "; ".join(
                f"{'.'.join(str(part) for part in item['loc'])}: {item['msg']}"
                for item in exc.errors()
            ),
        }

    except SandboxViolation as exc:
        return {
            "success": False,
            "error": "sandbox_violation",
            "message": str(exc),
        }

    except OSError as exc:
        return {
            "success": False,
            "error": "filesystem_error",
            "message": str(exc),
        }


# list_allowed_directories
def list_allowed_directories() -> dict:
    """Return the directory that the MCP server is allowed to access."""

    try:
        from .security import SANDBOX_ROOT

        return {
            "success": True,
            "directories": [str(SANDBOX_ROOT)],
        }

    except Exception as exc:
        return {
            "success": False,
            "error": "configuration_error",
            "message": str(exc),
        }


# get_file_info
def get_file_info(
    path: str,
) -> dict:
    """Return metadata for a file or directory."""

    try:
        target = resolve_safe_path(path)

        if not target.exists():
            return {
                "success": False,
                "error": "not_found",
                "message": f"Path does not exist: {path}",
            }

        stat = target.stat()

        return {
            "success": True,
            "path": str(target),
            "name": target.name,
            "type": "directory" if target.is_dir() else "file",
            "size_bytes": stat.st_size,
            "modified_timestamp": stat.st_mtime,
        }

    except SandboxViolation as exc:
        return {
            "success": False,
            "error": "sandbox_violation",
            "message": str(exc),
        }

    except OSError as exc:
        return {
            "success": False,
            "error": "filesystem_error",
            "message": str(exc),
        }


# git_status
def git_status() -> dict:
    """Return Git status for the MCP server repository."""

    try:
        repo_root = Path(__file__).resolve().parents[2]

        result = subprocess.run(
            ["git", "-C", str(repo_root), "status", "--short"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": "git_error",
                "message": result.stderr.strip() or "Git status failed.",
            }

        return {
            "success": True,
            "repository": str(repo_root),
            "status": result.stdout.strip(),
        }

    except OSError as exc:
        return {
            "success": False,
            "error": "git_unavailable",
            "message": str(exc),
        }


# git_diff
def git_diff() -> dict:
    """Return the current Git diff for the MCP server repository."""

    try:
        repo_root = Path(__file__).resolve().parents[2]

        result = subprocess.run(
            ["git", "-C", str(repo_root), "diff"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": "git_error",
                "message": result.stderr.strip() or "Git diff failed.",
            }

        return {
            "success": True,
            "repository": str(repo_root),
            "diff": result.stdout,
        }

    except OSError as exc:
        return {
            "success": False,
            "error": "git_unavailable",
            "message": str(exc),
        }


# checkpoint
def checkpoint(
    message: str,
) -> dict:
    """Append a timestamped checkpoint to CHECKPOINTS.md."""

    try:
        validated = CheckpointInput(message=message)
        message = validated.message
        from datetime import datetime
        from .security import SANDBOX_ROOT

        checkpoint_file = SANDBOX_ROOT / "CHECKPOINTS.md"

        timestamp = datetime.now().astimezone().isoformat(
            timespec="seconds"
        )

        entry = f"\n## Checkpoint — {timestamp}\n\n{message}\n"

        with checkpoint_file.open(
            "a",
            encoding="utf-8",
        ) as file:
            file.write(entry)

        return {
            "success": True,
            "path": str(checkpoint_file),
            "message": "Checkpoint recorded successfully.",
        }

    except ValidationError as exc:
        return {
            "success": False,
            "error": "validation_error",
            "message": "; ".join(
                f"{'.'.join(str(part) for part in item['loc'])}: {item['msg']}"
                for item in exc.errors()
            ),
        }

    except OSError as exc:
        return {
            "success": False,
            "error": "filesystem_error",
            "message": str(exc),
        }


# read_project_state
def read_project_state() -> dict:
    """Read PROJECT_STATE, PLAN_LOG, CHECKPOINTS, and DECISIONS."""

    try:
        from .security import SANDBOX_ROOT

        filenames = [
            "PROJECT_STATE.md",
            "PLAN_LOG.md",
            "CHECKPOINTS.md",
            "DECISIONS.md",
        ]

        documents = {}

        for filename in filenames:
            target = resolve_safe_path(filename)

            if target.exists() and target.is_file():
                documents[filename] = target.read_text(
                    encoding="utf-8"
                )
            else:
                documents[filename] = None

        return {
            "success": True,
            "sandbox": str(SANDBOX_ROOT),
            "documents": documents,
        }

    except SandboxViolation as exc:
        return {
            "success": False,
            "error": "sandbox_violation",
            "message": str(exc),
        }

    except UnicodeDecodeError as exc:
        return {
            "success": False,
            "error": "invalid_text_encoding",
            "message": str(exc),
        }

    except OSError as exc:
        return {
            "success": False,
            "error": "filesystem_error",
            "message": str(exc),
        }
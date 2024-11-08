# content/utils.py

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from .config import ALLOWED_FILE_TYPES, LANGUAGE_CONFIGS


def validate_content_structure(content: Dict[str, Any], required_fields: List[str]) -> bool:
    """Validate if content has all required fields."""
    return all(field in content for field in required_fields)


def sanitize_filename(filename: str) -> str:
    """Convert a string to a valid filename."""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    return filename.lower()


def is_valid_file_type(filename: str, category: str) -> bool:
    """Check if file type is allowed for the given category."""
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_FILE_TYPES.get(category, [])


def load_json_content(file_path: Path) -> Dict:
    """Load and validate JSON content file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {file_path}: {str(e)}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Content file not found: {file_path}")


def save_json_content(content: Dict, file_path: Path) -> None:
    """Save content to JSON file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)


def get_language_config(language: str) -> Optional[Dict]:
    """Get configuration for a specific language."""
    return LANGUAGE_CONFIGS.get(language.lower())


def format_code_sample(code: str, language: str) -> str:
    """Format code sample with proper indentation and comments."""
    config = get_language_config(language)
    if not config:
        return code

    # Basic formatting
    lines = code.split('\n')
    formatted_lines = []
    indent = 0

    for line in lines:
        # Handle indentation
        stripped = line.strip()
        if stripped.endswith('{'):
            formatted_lines.append('    ' * indent + stripped)
            indent += 1
        elif stripped.startswith('}'):
            indent = max(0, indent - 1)
            formatted_lines.append('    ' * indent + stripped)
        else:
            formatted_lines.append('    ' * indent + stripped)

    return '\n'.join(formatted_lines)


def create_content_metadata(
        title: str,
        author: str,
        version: str,
        last_updated: str,
        language: str
) -> Dict:
    """Create metadata for content files."""
    return {
        "title": title,
        "author": author,
        "version": version,
        "last_updated": last_updated,
        "language": language,
        "language_config": get_language_config(language)
    }


def validate_code_syntax(code: str, language: str) -> bool:
    """Basic syntax validation for code samples."""
    # This is a basic implementation - you might want to add more sophisticated validation
    try:
        if language.lower() == 'python':
            compile(code, '<string>', 'exec')
        # Add validation for other languages as needed
        return True
    except SyntaxError:
        return False


def generate_file_structure(base_path: Path, structure: Dict[str, Any]) -> None:
    """Generate directory and file structure from dictionary."""
    for name, content in structure.items():
        path = base_path / name
        if isinstance(content, dict):
            path.mkdir(parents=True, exist_ok=True)
            generate_file_structure(path, content)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, (str, bytes)):
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
            elif isinstance(content, dict):
                save_json_content(content, path)

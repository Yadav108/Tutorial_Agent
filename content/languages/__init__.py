# content/languages/__init__.py

import logging
from typing import Dict
from ..models import Language

# Import language content getters
from .python import get_python_content
from .javascript import get_javascript_content
from .csharp import get_csharp_content

logger = logging.getLogger('TutorialAgent')


def load_all_languages() -> Dict[str, Language]:
    """Load content for all supported languages.

    Returns:
        Dictionary mapping language IDs to Language objects
    """
    languages = {}

    try:
        # Load Python content
        try:
            python = get_python_content()
            languages['python'] = python
            logger.debug(f"Loaded Python content with {len(python.topics)} topics")
        except Exception as e:
            logger.error(f"Failed to load Python content: {str(e)}", exc_info=True)

        # Load JavaScript content
        try:
            javascript = get_javascript_content()
            languages['javascript'] = javascript
            logger.debug(f"Loaded JavaScript content with {len(javascript.topics)} topics")
        except Exception as e:
            logger.error(f"Failed to load JavaScript content: {str(e)}", exc_info=True)

        # Load C# content
        try:
            csharp = get_csharp_content()
            languages['csharp'] = csharp
            logger.debug(f"Loaded C# content with {len(csharp.topics)} topics")
        except Exception as e:
            logger.error(f"Failed to load C# content: {str(e)}", exc_info=True)

        # Add metadata to languages
        for lang_id, language in languages.items():
            language.id = lang_id
            # Set default icon if not specified
            if not language.icon:
                language.icon = f"{lang_id}.svg"
            # Set default color if not specified
            if not language.color:
                language.color = _get_default_color(lang_id)

        logger.info(f"Successfully loaded {len(languages)} languages")

    except Exception as e:
        logger.error(f"Error loading languages: {str(e)}", exc_info=True)

    return languages


def _get_default_color(lang_id: str) -> str:
    """Get default color for a language."""
    default_colors = {
        'python': '#3776AB',
        'javascript': '#F7DF1E',
        'csharp': '#178600'
    }
    return default_colors.get(lang_id, '#000000')


# Export functions
__all__ = [
    'load_all_languages',
    'get_python_content',
    'get_javascript_content',
    'get_csharp_content'
]

# Version info
__version__ = '1.0.0'

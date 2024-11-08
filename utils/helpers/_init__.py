"""
Helper utilities for Tutorial Agent
"""

from .file_helpers import FileHelper
from .string_helpers import StringHelper

# Import common utility functions
from .common import (
    sanitize_filename,
    format_time,
    format_size,
    format_date,
    generate_unique_id,
    validate_email,
    validate_password,
    calculate_hash,
    compare_versions,
    parse_duration,
    deep_merge,
    flatten_dict,
    unflatten_dict
)

# Error handling utilities
from .error_handling import (
    handle_exception,
    log_error,
    format_traceback,
    ErrorCode,
    ApplicationError,
    ValidationError,
    DatabaseError
)

# Decorators
from .decorators import (
    timer,
    retry,
    cache,
    validate_input,
    log_function,
    singleton,
    async_task,
    deprecated
)

# Type hints
from .types import (
    JsonDict,
    JsonList,
    PathLike,
    OptionalStr,
    CallbackType,
    ProgressCallback
)

# Constants
ENCODING = 'utf-8'
DEFAULT_CHUNK_SIZE = 8192
MAX_FILENAME_LENGTH = 255
VALID_FILE_EXTENSIONS = {
    'python': ['.py'],
    'cpp': ['.cpp', '.h', '.hpp'],
    'csharp': ['.cs'],
    'java': ['.java']
}

# Export helper components
__all__ = [
    # Classes
    'FileHelper',
    'StringHelper',
    'ErrorCode',
    'ApplicationError',
    'ValidationError',
    'DatabaseError',

    # Common utilities
    'sanitize_filename',
    'format_time',
    'format_size',
    'format_date',
    'generate_unique_id',
    'validate_email',
    'validate_password',
    'calculate_hash',
    'compare_versions',
    'parse_duration',
    'deep_merge',
    'flatten_dict',
    'unflatten_dict',

    # Error handling
    'handle_exception',
    'log_error',
    'format_traceback',

    # Decorators
    'timer',
    'retry',
    'cache',
    'validate_input',
    'log_function',
    'singleton',
    'async_task',
    'deprecated',

    # Type hints
    'JsonDict',
    'JsonList',
    'PathLike',
    'OptionalStr',
    'CallbackType',
    'ProgressCallback',

    # Constants
    'ENCODING',
    'DEFAULT_CHUNK_SIZE',
    'MAX_FILENAME_LENGTH',
    'VALID_FILE_EXTENSIONS'
]


# Initialize helper modules
def init_helpers():
    """Initialize helper modules"""
    pass


# Cleanup helper modules
def cleanup_helpers():
    """Cleanup helper modules"""
    FileHelper().cleanup_temp_files()
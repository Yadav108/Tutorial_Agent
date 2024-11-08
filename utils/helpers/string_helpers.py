import re
from typing import List, Optional
import difflib
import unicodedata
import html


class StringHelper:
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename by removing invalid characters"""
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '')

        # Replace spaces with underscores
        filename = filename.replace(' ', '_')

        # Remove any non-ASCII characters
        filename = ''.join(c for c in filename if ord(c) < 128)

        return filename.strip('._')

    @staticmethod
    def format_code(code: str, language: str) -> str:
        """Format code for display"""
        # Remove excess whitespace
        code = code.strip()

        # Add language-specific formatting
        if language == 'python':
            # Ensure proper indentation (4 spaces)
            lines = code.split('\n')
            formatted_lines = []
            indent_level = 0

            for line in lines:
                stripped = line.strip()

                # Adjust indent level based on content
                if stripped.endswith(':'):
                    formatted_lines.append('    ' * indent_level + stripped)
                    indent_level += 1
                elif stripped in ['break', 'continue', 'pass', 'return']:
                    formatted_lines.append('    ' * indent_level + stripped)
                    if indent_level > 0:
                        indent_level -= 1
                else:
                    formatted_lines.append('    ' * indent_level + stripped)

            code = '\n'.join(formatted_lines)

        return code

    @staticmethod
    def compare_code(code1: str, code2: str) -> float:
        """Compare similarity between two code snippets"""
        # Remove whitespace and convert to lowercase for comparison
        code1_clean = ' '.join(code1.lower().split())
        code2_clean = ' '.join(code2.lower().split())

        # Use difflib to calculate similarity ratio
        return difflib.SequenceMatcher(None, code1_clean, code2_clean).ratio()

    @staticmethod
    def extract_code_blocks(markdown: str) -> List[dict]:
        """Extract code blocks from markdown text"""
        pattern = r'```(\w+)?\n(.*?)\n```'
        matches = re.finditer(pattern, markdown, re.DOTALL)

        code_blocks = []
        for match in matches:
            language = match.group(1) or 'text'
            code = match.group(2).strip()
            code_blocks.append({
                'language': language,
                'code': code
            })

        return code_blocks

    @staticmethod
    def sanitize_html(content: str) -> str:
        """Sanitize HTML content"""
        # Convert special characters to HTML entities
        content = html.escape(content)

        # Remove potentially dangerous tags and attributes
        dangerous_tags = ['script', 'style', 'iframe', 'object', 'embed']
        for tag in dangerous_tags:
            content = re.sub(f'<{tag}.*?</{tag}>', '', content, flags=re.DOTALL)

        return content

    @staticmethod
    def truncate_text(text: str, max_length: int,
                      suffix: str = '...') -> str:
        """Truncate text to specified length"""
        if len(text) <= max_length:
            return text

        return text[:max_length - len(suffix)].strip() + suffix

    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text by removing special characters and extra whitespace"""
        # Convert to NFKD form and remove diacritics
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    @staticmethod
    def generate_slug(text: str) -> str:
        """Generate URL-friendly slug from text"""
        # Normalize text
        text = StringHelper.normalize_text(text.lower())

        # Replace spaces with hyphens
        text = text.replace(' ', '-')

        # Remove consecutive hyphens
        text = re.sub(r'-+', '-', text)

        return text.strip('-')

    @staticmethod
    def highlight_differences(text1: str, text2: str) -> tuple:
        """Highlight differences between two texts"""
        differ = difflib.Differ()
        diff = list(differ.compare(text1.splitlines(), text2.splitlines()))

        additions = []
        deletions = []

        for line in diff:
            if line.startswith('+'):
                additions.append(line[2:])
            elif line.startswith('-'):
                deletions.append(line[2:])

        return additions, deletions

    @staticmethod
    def extract_variables(code: str) -> List[str]:
        """Extract variable names from code"""
        # This is a simple implementation; might need adjustment based on language
        pattern = r'\b(?:var|let|const|int|float|string|bool|double)\s+(\w+)\b'
        matches = re.finditer(pattern, code)
        return [match.group(1) for match in matches]

    @staticmethod
    def format_error_message(error: Exception) -> str:
        """Format exception message for display"""
        error_type = type(error).__name__
        error_message = str(error)

        # Format traceback if available
        if hasattr(error, '__traceback__'):
            import traceback
            tb = ''.join(traceback.format_tb(error.__traceback__))
            return f"{error_type}: {error_message}\n\nTraceback:\n{tb}"

        return f"{error_type}: {error_message}"

    @staticmethod
    def is_valid_code_structure(code: str, language: str) -> bool:
        """Check if code has valid basic structure"""
        if language == 'python':
            # Check for basic Python syntax
            try:
                compile(code, '<string>', 'exec')
                return True
            except SyntaxError:
                return False
        elif language == 'java':
            # Check for basic Java class structure
            class_pattern = r'public\s+class\s+\w+\s*\{'
            method_pattern = r'public\s+static\s+void\s+main\s*\('
            return bool(re.search(class_pattern, code) and
                        re.search(method_pattern, code))

        return True  # Default to true for other languages

    @staticmethod
    def find_matching_bracket(text: str, pos: int) -> Optional[int]:
        """Find matching bracket position"""
        brackets = {'(': ')', '[': ']', '{': '}'}
        reverse_brackets = {v: k for k, v in brackets.items()}

        if pos >= len(text) or (text[pos] not in brackets and
                                text[pos] not in reverse_brackets):
            return None

        stack = []

        if text[pos] in brackets:
            # Forward search
            opening = text[pos]
            closing = brackets[opening]

            for i in range(pos, len(text)):
                if text[i] == opening:
                    stack.append(i)
                elif text[i] == closing:
                    if not stack:
                        return None
                    if stack.pop() == pos:
                        return i
        else:
            # Backward search
            closing = text[pos]
            opening = reverse_brackets[closing]

            for i in range(pos, -1, -1):
                if text[i] == closing:
                    stack.append(i)
                elif text[i] == opening:
                    if not stack:
                        return None
                    if stack.pop() == pos:
                        return i

        return None
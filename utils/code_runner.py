import subprocess
import os
import tempfile
import sys
import threading
import queue
import time
from typing import Dict, Tuple, Optional
from pathlib import Path


class CodeRunner:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.temp_dir = Path(tempfile.gettempdir()) / 'tutorial_agent'
        self.temp_dir.mkdir(exist_ok=True)

        self.language_configs = {
            'python': {
                'extension': '.py',
                'command': 'python',
                'compile_command': None
            },
            'cpp': {
                'extension': '.cpp',
                'command': './a.out',
                'compile_command': 'g++ {file_path}'
            },
            'csharp': {
                'extension': '.cs',
                'command': 'dotnet run',
                'compile_command': 'dotnet build'
            },
            'java': {
                'extension': '.java',
                'command': 'java',
                'compile_command': 'javac {file_path}'
            }
        }

    def run_code(self, code: str, language: str, input_data: str = '') -> Dict:
        """Run code and return result"""
        if language not in self.language_configs:
            return {
                'status': 'error',
                'error': f'Unsupported language: {language}'
            }

        try:
            # Create temporary file
            file_path = self._create_temp_file(code, language)

            # Compile if necessary
            if self.language_configs[language]['compile_command']:
                compile_result = self._compile_code(file_path, language)
                if compile_result.get('status') == 'error':
                    return compile_result

            # Run the code
            output, error = self._execute_code(file_path, language, input_data)

            # Clean up
            self._cleanup(file_path)

            if error:
                return {
                    'status': 'error',
                    'error': error
                }

            return {
                'status': 'success',
                'output': output
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def _create_temp_file(self, code: str, language: str) -> Path:
        """Create temporary file with the code"""
        config = self.language_configs[language]
        extension = config['extension']

        # Create unique file name
        timestamp = int(time.time() * 1000)
        file_name = f"code_{timestamp}{extension}"
        file_path = self.temp_dir / file_name

        # Handle Java class name
        if language == 'java':
            # Extract class name from code
            class_name = self._extract_java_class_name(code)
            if class_name:
                file_name = f"{class_name}{extension}"
                file_path = self.temp_dir / file_name

        # Write code to file
        with open(file_path, 'w') as f:
            f.write(code)

        return file_path

    def _compile_code(self, file_path: Path, language: str) -> Dict:
        """Compile code if needed"""
        config = self.language_configs[language]
        compile_command = config['compile_command']

        if not compile_command:
            return {'status': 'success'}

        try:
            compile_command = compile_command.format(file_path=file_path)
            process = subprocess.Popen(
                compile_command.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=file_path.parent
            )

            _, stderr = process.communicate(timeout=self.timeout)

            if process.returncode != 0:
                return {
                    'status': 'error',
                    'error': f"Compilation error:\n{stderr.decode()}"
                }

            return {'status': 'success'}

        except subprocess.TimeoutExpired:
            process.kill()
            return {
                'status': 'error',
                'error': 'Compilation timeout'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': f'Compilation error: {str(e)}'
            }

    def _execute_code(self, file_path: Path, language: str,
                      input_data: str) -> Tuple[str, Optional[str]]:
        """Execute the code and return output"""
        config = self.language_configs[language]
        command = config['command']

        if language == 'python':
            command = f"{command} {file_path}"
        elif language == 'java':
            command = f"{command} {file_path.stem}"

        # Create queue for output
        output_queue = queue.Queue()
        error_queue = queue.Queue()

        def target():
            try:
                process = subprocess.Popen(
                    command.split(),
                    stdin=subprocess.PIPE if input_data else None,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=file_path.parent
                )

                stdout, stderr = process.communicate(
                    input=input_data.encode() if input_data else None,
                    timeout=self.timeout
                )

                output_queue.put(stdout.decode())
                if stderr:
                    error_queue.put(stderr.decode())

            except Exception as e:
                error_queue.put(str(e))

        # Run execution in separate thread
        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout=self.timeout)

        if thread.is_alive():
            thread.join()
            return '', 'Execution timeout'

        # Get results
        output = output_queue.get() if not output_queue.empty() else ''
        error = error_queue.get() if not error_queue.empty() else None

        return output, error

    def _cleanup(self, file_path: Path):
        """Clean up temporary files"""
        try:
            if file_path.exists():
                file_path.unlink()

            # Clean up compiled files
            if file_path.suffix == '.cpp':
                (file_path.parent / 'a.out').unlink(missing_ok=True)
            elif file_path.suffix == '.class':
                (file_path.parent / f"{file_path.stem}.class").unlink(missing_ok=True)

        except Exception:
            pass  # Ignore cleanup errors

    def _extract_java_class_name(self, code: str) -> Optional[str]:
        """Extract Java class name from code"""
        import re
        pattern = r'public\s+class\s+(\w+)'
        match = re.search(pattern, code)
        return match.group(1) if match else None

    def validate_code(self, code: str, language: str) -> Dict:
        """Validate code before execution"""
        validation_result = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }

        # Check code length
        if len(code.strip()) == 0:
            validation_result['is_valid'] = False
            validation_result['errors'].append('Code cannot be empty')
            return validation_result

        if len(code) > 50000:  # 50KB limit
            validation_result['warnings'].append('Code is quite long, execution might be slow')

        # Language-specific validation
        if language == 'python':
            validation_result.update(self._validate_python_code(code))
        elif language == 'java':
            validation_result.update(self._validate_java_code(code))
        elif language == 'cpp':
            validation_result.update(self._validate_cpp_code(code))

        return validation_result

    def _validate_python_code(self, code: str) -> Dict:
        """Validate Python code"""
        result = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }

        # Check for syntax errors
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            result['is_valid'] = False
            result['errors'].append(f'Syntax error: {str(e)}')
            return result

        # Check for potentially dangerous operations
        dangerous_modules = ['os', 'subprocess', 'sys', 'shutil']
        for module in dangerous_modules:
            if f'import {module}' in code or f'from {module}' in code:
                result['warnings'].append(
                    f'Code contains potentially dangerous module: {module}'
                )

        return result

    def _validate_java_code(self, code: str) -> Dict:
        """Validate Java code"""
        result = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }

        # Check for public class
        if 'public class' not in code:
            result['is_valid'] = False
            result['errors'].append('Java code must contain a public class')

        # Check for main method
        if 'public static void main' not in code:
            result['is_valid'] = False
            result['errors'].append('Java code must contain a main method')

        return result

    def _validate_cpp_code(self, code: str) -> Dict:
        """Validate C++ code"""
        result = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }

        # Check for main function
        if 'main' not in code:
            result['is_valid'] = False
            result['errors'].append('C++ code must contain a main function')

        # Check for includes
        dangerous_headers = ['<fstream>', '<filesystem>']
        for header in dangerous_headers:
            if header in code:
                result['warnings'].append(
                    f'Code contains potentially dangerous header: {header}'
                )

        return result
import os
import shutil
import json
import yaml
import csv
from pathlib import Path
from typing import Dict, List, Union, Optional
from datetime import datetime


class FileHelper:
    def __init__(self, base_path: str = '.'):
        self.base_path = Path(base_path)
        self.temp_dir = self.base_path / 'temp'
        self.temp_dir.mkdir(exist_ok=True)

    def read_file(self, file_path: Union[str, Path], encoding: str = 'utf-8') -> str:
        """Read content from a file"""
        try:
            file_path = Path(file_path)
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            raise FileNotFoundError(f"Error reading file {file_path}: {str(e)}")

    def write_file(self, file_path: Union[str, Path],
                   content: str, encoding: str = 'utf-8') -> bool:
        """Write content to a file"""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing file {file_path}: {str(e)}")
            return False

    def read_json(self, file_path: Union[str, Path]) -> Dict:
        """Read JSON file"""
        try:
            content = self.read_file(file_path)
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {str(e)}")

    def write_json(self, file_path: Union[str, Path],
                   data: Dict, pretty: bool = True) -> bool:
        """Write JSON file"""
        try:
            content = json.dumps(data, indent=4 if pretty else None)
            return self.write_file(file_path, content)
        except Exception as e:
            print(f"Error writing JSON to {file_path}: {str(e)}")
            return False

    def read_yaml(self, file_path: Union[str, Path]) -> Dict:
        """Read YAML file"""
        try:
            content = self.read_file(file_path)
            return yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {file_path}: {str(e)}")

    def write_yaml(self, file_path: Union[str, Path], data: Dict) -> bool:
        """Write YAML file"""
        try:
            content = yaml.dump(data, default_flow_style=False)
            return self.write_file(file_path, content)
        except Exception as e:
            print(f"Error writing YAML to {file_path}: {str(e)}")
            return False

    def read_csv(self, file_path: Union[str, Path],
                 has_header: bool = True) -> List[Dict]:
        """Read CSV file"""
        try:
            with open(file_path, 'r', newline='') as f:
                if has_header:
                    reader = csv.DictReader(f)
                    return list(reader)
                else:
                    reader = csv.reader(f)
                    return [row for row in reader]
        except Exception as e:
            raise ValueError(f"Error reading CSV {file_path}: {str(e)}")

    def write_csv(self, file_path: Union[str, Path],
                  data: List[Dict], fieldnames: Optional[List[str]] = None) -> bool:
        """Write CSV file"""
        try:
            if not fieldnames and data:
                fieldnames = list(data[0].keys())

            with open(file_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            print(f"Error writing CSV to {file_path}: {str(e)}")
            return False

    def create_temp_file(self, content: str,
                         prefix: str = '', suffix: str = '') -> Path:
        """Create a temporary file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f"{prefix}_{timestamp}{suffix}" if prefix else f"temp_{timestamp}{suffix}"
        temp_file = self.temp_dir / file_name

        self.write_file(temp_file, content)
        return temp_file

    def cleanup_temp_files(self, max_age_days: int = 1):
        """Clean up old temporary files"""
        try:
            current_time = datetime.now()
            for file_path in self.temp_dir.glob('*'):
                if file_path.is_file():
                    file_age = datetime.fromtimestamp(file_path.stat().st_mtime)
                    age_days = (current_time - file_age).days

                    if age_days >= max_age_days:
                        file_path.unlink()
        except Exception as e:
            print(f"Error cleaning up temp files: {str(e)}")

    def copy_file(self, source: Union[str, Path],
                  destination: Union[str, Path]) -> bool:
        """Copy a file"""
        try:
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            print(f"Error copying file from {source} to {destination}: {str(e)}")
            return False

    def move_file(self, source: Union[str, Path],
                  destination: Union[str, Path]) -> bool:
        """Move a file"""
        try:
            shutil.move(source, destination)
            return True
        except Exception as e:
            print(f"Error moving file from {source} to {destination}: {str(e)}")
            return False

    def delete_file(self, file_path: Union[str, Path]) -> bool:
        """Delete a file"""
        try:
            Path(file_path).unlink()
            return True
        except Exception as e:
            print(f"Error deleting file {file_path}: {str(e)}")
            return False

    def ensure_directory(self, directory: Union[str, Path]) -> bool:
        """Ensure a directory exists"""
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directory {directory}: {str(e)}")
            return False

    def list_files(self, directory: Union[str, Path],
                   pattern: str = '*', recursive: bool = False) -> List[Path]:
        """List files in a directory"""
        try:
            path = Path(directory)
            if recursive:
                return list(path.rglob(pattern))
            return list(path.glob(pattern))
        except Exception as e:
            print(f"Error listing files in {directory}: {str(e)}")
            return []

    def get_file_info(self, file_path: Union[str, Path]) -> Dict:
        """Get file information"""
        try:
            path = Path(file_path)
            stat = path.stat()
            return {
                'name': path.name,
                'extension': path.suffix,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'is_file': path.is_file(),
                'is_directory': path.is_directory()
            }
        except Exception as e:
            print(f"Error getting file info for {file_path}: {str(e)}")
            return {}
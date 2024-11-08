"""DotNet SDK setup and management for the Tutorial Agent."""

import os
import sys
import subprocess
import platform
import urllib.request
import json
import tempfile
import shutil
import logging
from pathlib import Path
from PyQt6.QtWidgets import QMessageBox, QProgressDialog
from PyQt6.QtCore import Qt

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DotNetSetup:
    """Manages .NET SDK setup and verification."""

    def __init__(self):
        self.sdk_version = "6.0"  # LTS version
        self.base_path = self._get_base_path()
        self.dotnet_path = self._get_dotnet_path()
        self._installation_attempted = False  # Track if we've already tried installing

    def _get_base_path(self) -> Path:
        """Get the base path for .NET SDK installation."""
        if platform.system() == "Windows":
            return Path(os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))) / "TutorialAgent" / "dotnet"
        else:
            return Path.home() / ".tutorialagent" / "dotnet"

    def _get_dotnet_path(self) -> Path:
        """Get the path to the dotnet executable."""
        if platform.system() == "Windows":
            return self.base_path / "dotnet.exe"
        else:
            return self.base_path / "dotnet"

    def check_global_dotnet(self) -> bool:
        """Check if .NET SDK is installed globally."""
        try:
            result = subprocess.run(
                ['dotnet', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info(f"Global .NET SDK found: {result.stdout.strip()}")
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            logger.info(f"Global .NET SDK not found: {str(e)}")
        except Exception as e:
            logger.error(f"Error checking global .NET SDK: {str(e)}")
        return False

    def check_local_dotnet(self) -> bool:
        """Check if .NET SDK is installed locally."""
        try:
            if not self.dotnet_path.exists():
                logger.info("Local .NET SDK not found")
                return False

            result = subprocess.run(
                [str(self.dotnet_path), '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info(f"Local .NET SDK found: {result.stdout.strip()}")
                return True
        except Exception as e:
            logger.error(f"Error checking local .NET SDK: {str(e)}")
        return False

    def is_installed(self) -> bool:
        """Check if .NET SDK is installed either globally or locally."""
        return self.check_global_dotnet() or self.check_local_dotnet()

    def get_download_url(self) -> str:
        """Get the appropriate .NET SDK download URL for the current platform."""
        system = platform.system().lower()
        machine = platform.machine().lower()

        # Map architecture names
        arch_map = {
            'amd64': 'x64',
            'x86_64': 'x64',
            'aarch64': 'arm64'
        }

        arch = arch_map.get(machine, machine)

        # Base URLs for different platforms
        urls = {
            'windows': {
                'x64': f"https://dotnet.microsoft.com/download/dotnet/{self.sdk_version}",
                'x86': f"https://dotnet.microsoft.com/download/dotnet/{self.sdk_version}",
                'arm64': f"https://dotnet.microsoft.com/download/dotnet/{self.sdk_version}"
            },
            'linux': {
                'x64': f"https://dotnet.microsoft.com/download/dotnet/{self.sdk_version}",
                'arm64': f"https://dotnet.microsoft.com/download/dotnet/{self.sdk_version}"
            },
            'darwin': {
                'x64': f"https://dotnet.microsoft.com/download/dotnet/{self.sdk_version}",
                'arm64': f"https://dotnet.microsoft.com/download/dotnet/{self.sdk_version}"
            }
        }

        if system not in urls or arch not in urls[system]:
            msg = f"Unsupported platform: {system} {arch}"
            logger.error(msg)
            raise RuntimeError(msg)

        return urls[system][arch]

    def download_and_install(self, parent_widget=None) -> bool:
        """Download and install .NET SDK."""
        if self._installation_attempted:
            logger.info("Installation already attempted, skipping")
            return False

        self._installation_attempted = True
        try:
            # Show information about manual installation
            QMessageBox.information(
                parent_widget,
                "Manual .NET SDK Installation Required",
                "Please install the .NET SDK manually:\n\n"
                "1. Visit: https://dotnet.microsoft.com/download\n"
                "2. Download the .NET SDK for your platform\n"
                "3. Follow the installation instructions\n"
                "4. Restart the application after installation\n\n"
                "The C# compiler will be available after installing the SDK."
            )
            return False

        except Exception as e:
            logger.error(f"Error during installation: {str(e)}")
            if parent_widget:
                QMessageBox.critical(
                    parent_widget,
                    "Installation Error",
                    f"Failed to install .NET SDK:\n{str(e)}"
                )
            return False
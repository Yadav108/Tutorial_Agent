#!/usr/bin/env python3
"""
Tutorial Agent - Main Entry Point

This module provides the main entry point for the Tutorial Agent application.
It can be run using: python -m tutorial_agent
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run the application
from run import main

if __name__ == "__main__":
    sys.exit(main())
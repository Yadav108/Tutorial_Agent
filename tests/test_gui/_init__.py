"""
GUI test suite for Tutorial Agent
"""

import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt


# GUI test utilities
class GUITestCase:
    """Base class for GUI tests"""

    @pytest.fixture(autouse=True)
    def setup_qt(self, qtbot):
        """Setup Qt application and bot"""
        self.app = QApplication.instance() or QApplication([])
        self.qtbot = qtbot

    def capture_widget_screenshot(self, widget, name):
        """Capture widget screenshot"""
        if not hasattr(self, '_screenshot_dir'):
            import tempfile
            from pathlib import Path
            self._screenshot_dir = Path(tempfile.gettempdir()) / 'tutorial_agent_screenshots'
            self._screenshot_dir.mkdir(exist_ok=True)

        screenshot_path = self._screenshot_dir / f"{name}.png"
        widget.grab().save(str(screenshot_path))
        return screenshot_path

    def simulate_click(self, widget, button=Qt.MouseButton.LeftButton):
        """Simulate mouse click on widget"""
        QTest.mouseClick(widget, button)

    def simulate_double_click(self, widget, button=Qt.MouseButton.LeftButton):
        """Simulate mouse double click on widget"""
        QTest.mouseDClick(widget, button)

    def simulate_key_click(self, widget, key, modifier=Qt.KeyboardModifier.NoModifier):
        """Simulate keyboard key click"""
        QTest.keyClick(widget, key, modifier)

    def simulate_key_clicks(self, widget, text):
        """Simulate keyboard text input"""
        QTest.keyClicks(widget, text)

    def wait_until(self, callback, timeout=1000):
        """Wait until callback returns True or timeout"""
        return self.qtbot.waitUntil(callback, timeout=timeout)

    def wait_for_window(self, window_class, timeout=1000):
        """Wait for window of specific class to appear"""

        def check():
            for widget in self.app.topLevelWidgets():
                if isinstance(widget, window_class):
                    return True
            return False

        return self.wait_until(check, timeout=timeout)


# Test utilities
def requires_gui(func):
    """Decorator to mark test as requiring GUI"""
    return pytest.mark.gui(func)


def requires_display(func):
    """Decorator to mark test as requiring display"""

    def wrapper(*args, **kwargs):
        import os
        if not os.environ.get('DISPLAY'):
            pytest.skip('Test requires display')
        return func(*args, **kwargs)

    return wrapper


# Mouse button constants
MOUSE_BUTTONS = {
    'left': Qt.MouseButton.LeftButton,
    'right': Qt.MouseButton.RightButton,
    'middle': Qt.MouseButton.MiddleButton
}

# Keyboard modifier constants
KEY_MODIFIERS = {
    'shift': Qt.KeyboardModifier.ShiftModifier,
    'ctrl': Qt.KeyboardModifier.ControlModifier,
    'alt': Qt.KeyboardModifier.AltModifier,
    'meta': Qt.KeyboardModifier.MetaModifier
}

# Export test components
__all__ = [
    'GUITestCase',
    'requires_gui',
    'requires_display',
    'MOUSE_BUTTONS',
    'KEY_MODIFIERS'
]
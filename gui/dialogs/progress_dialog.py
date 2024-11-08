from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QProgressBar, QPushButton, QFrame, QScrollArea,
    QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QIcon, QFont


class ProgressWorker(QThread):
    """Worker thread for handling long operations"""
    progress_updated = pyqtSignal(int, str)
    task_completed = pyqtSignal(bool, str)
    log_message = pyqtSignal(str)

    def __init__(self, task_function, *args, **kwargs):
        super().__init__()
        self.task_function = task_function
        self.args = args
        self.kwargs = kwargs
        self.is_cancelled = False

    def run(self):
        """Execute the task"""
        try:
            # Pass the progress callback to the task function
            self.kwargs['progress_callback'] = self.update_progress
            self.kwargs['log_callback'] = self.log

            result = self.task_function(*self.args, **self.kwargs)
            if not self.is_cancelled:
                self.task_completed.emit(True, "Task completed successfully")
            else:
                self.task_completed.emit(False, "Task cancelled by user")

        except Exception as e:
            self.task_completed.emit(False, str(e))

    def update_progress(self, progress: int, message: str = ""):
        """Update progress from the task"""
        if not self.is_cancelled:
            self.progress_updated.emit(progress, message)

    def log(self, message: str):
        """Log a message from the task"""
        if not self.is_cancelled:
            self.log_message.emit(message)

    def cancel(self):
        """Cancel the task"""
        self.is_cancelled = True


class ProgressDialog(QDialog):
    cancelled = pyqtSignal()

    def __init__(self, title: str, task_function, *args, parent=None, **kwargs):
        super().__init__(parent)
        self.title = title
        self.worker = ProgressWorker(task_function, *args, **kwargs)
        self.show_log = kwargs.get('show_log', True)
        self.can_cancel = kwargs.get('can_cancel', True)
        self.auto_close = kwargs.get('auto_close', True)

        self.init_ui()
        self.setup_worker_connections()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(self.title)
        self.setMinimumWidth(400)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QFrame {
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 4px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Progress section
        progress_frame = QFrame()
        progress_layout = QVBoxLayout(progress_frame)

        # Status message
        self.status_label = QLabel("Initializing...")
        self.status_label.setFont(QFont("Arial", 11))
        self.status_label.setStyleSheet("color: #2c3e50;")
        progress_layout.addWidget(self.status_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 4px;
                text-align: center;
                background-color: #e9ecef;
                height: 12px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 4px;
            }
        """)
        progress_layout.addWidget(self.progress_bar)

        layout.addWidget(progress_frame)

        # Log section
        if self.show_log:
            log_frame = QFrame()
            log_layout = QVBoxLayout(log_frame)

            log_label = QLabel("Operation Log:")
            log_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            log_layout.addWidget(log_label)

            # Log text area
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("""
                QScrollArea {
                    border: none;
                }
            """)

            log_content = QWidget()
            self.log_layout = QVBoxLayout(log_content)
            self.log_layout.addStretch()

            scroll.setWidget(log_content)
            log_layout.addWidget(scroll)

            layout.addWidget(log_frame)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        if self.can_cancel:
            self.cancel_button = QPushButton("Cancel")
            self.cancel_button.setIcon(QIcon("assets/images/cancel.png"))
            self.cancel_button.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            self.cancel_button.clicked.connect(self.cancel_operation)
            button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def setup_worker_connections(self):
        """Setup worker thread connections"""
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.task_completed.connect(self.on_task_completed)
        self.worker.log_message.connect(self.add_log_message)

    def start(self):
        """Start the operation"""
        self.worker.start()
        self.exec()

    def update_progress(self, progress: int, message: str):
        """Update progress bar and status"""
        self.progress_bar.setValue(progress)
        if message:
            self.status_label.setText(message)

    def add_log_message(self, message: str):
        """Add message to log"""
        if self.show_log:
            log_entry = QLabel(message)
            log_entry.setWordWrap(True)
            log_entry.setStyleSheet("""
                QLabel {
                    color: #2c3e50;
                    padding: 2px 0;
                }
            """)
            self.log_layout.insertWidget(self.log_layout.count() - 1, log_entry)

    def on_task_completed(self, success: bool, message: str):
        """Handle task completion"""
        if success:
            self.progress_bar.setValue(100)
            self.status_label.setText("Operation completed successfully")
            self.status_label.setStyleSheet("color: #27ae60;")
        else:
            self.status_label.setText(f"Error: {message}")
            self.status_label.setStyleSheet("color: #e74c3c;")

        if self.can_cancel:
            self.cancel_button.setText("Close")
            self.cancel_button.setStyleSheet("""
                QPushButton {
                    background-color: #95a5a6;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 15px;
                }
                QPushButton:hover {
                    background-color: #7f8c8d;
                }
            """)

        if self.auto_close and success:
            QTimer.singleShot(1000, self.accept)

    def cancel_operation(self):
        """Cancel the operation"""
        if self.worker.isRunning():
            self.worker.cancel()
            self.cancelled.emit()
            self.status_label.setText("Operation cancelled")
            self.status_label.setStyleSheet("color: #e74c3c;")
            self.add_log_message("Operation cancelled by user")
        self.reject()

    def closeEvent(self, event):
        """Handle dialog close event"""
        if self.worker.isRunning():
            self.cancel_operation()
        event.accept()

    @staticmethod
    def example_task(progress_callback, log_callback):
        """Example task function showing how to use the progress dialog"""
        import time
        total_steps = 5

        for i in range(total_steps):
            if QThread.currentThread().is_cancelled:
                return False

            progress = ((i + 1) / total_steps) * 100
            progress_callback(progress, f"Processing step {i + 1} of {total_steps}")
            log_callback(f"Completed step {i + 1}")
            time.sleep(1)  # Simulate work

        return True
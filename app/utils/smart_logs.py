import logging
import os
from datetime import datetime

class SmartLogs:
    def __init__(self):
        # Create logs directory if it doesn't exist
        self.logs_dir = 'logs'
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

        # Set up logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Create handlers
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        
        # File handler - create new log file each day
        today = datetime.now().strftime('%Y-%m-%d')
        file_handler = logging.FileHandler(f'{self.logs_dir}/{today}.log')
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        # Add handlers to logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def info(self, message):
        """Log info level message"""
        self.logger.info(message)

    def error(self, message, exc_info=True):
        """Log error level message with exception info"""
        self.logger.error(message, exc_info=exc_info)

    def warning(self, message):
        """Log warning level message"""
        self.logger.warning(message)

    def debug(self, message):
        """Log debug level message"""
        self.logger.debug(message)

    def critical(self, message):
        """Log critical level message"""
        self.logger.critical(message)

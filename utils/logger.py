"""Logger utility for test framework."""

import logging
import colorlog
from pathlib import Path
from typing import Optional
from utils.config_manager import config


class Logger:
    """Custom logger with colored console output and file logging."""
    def __init__(self, name: str, log_file: Optional[str] = None):
        """Initialize logger.
        
        Args:
            name: Logger name
            log_file: Path to log file. If None, uses config default
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Remove existing handlers
        self.logger.handlers = []

        # Get logging config
        log_config = config.get_logging_config()
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        log_format = log_config.get(
            'format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Console handler with colors
        console_handler = colorlog.StreamHandler()
        console_handler.setLevel(log_level)

        console_format = colorlog.ColoredFormatter(
            '%(log_color)s' + log_format,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            })
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)

        # File handler
        if log_file is None:
            log_file = log_config.get('file_path', 'reports/test_log.log')

        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message: str, *args, **kwargs):
        """Log debug message."""
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """Log info message."""
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """Log warning message."""
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """Log error message."""
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """Log critical message."""
        self.logger.critical(message, *args, **kwargs)

    def log_request(self,
                    method: str,
                    url: str,
                    headers: dict = None,
                    body: dict = None,
                    params: dict = None):
        """Log HTTP request details.
        
        Args:
            method: HTTP method
            url: Request URL
            headers: Request headers
            body: Request body
            params: Query parameters
        """
        self.info(f"Request: {method} {url}")
        if params:
            self.debug(f"Query Parameters: {params}")
        if headers:
            self.debug(f"Headers: {headers}")
        if body:
            self.debug(f"Body: {body}")

    def log_response(self,
                     status_code: int,
                     headers: dict = None,
                     body: dict = None,
                     elapsed_time: float = None):
        """Log HTTP response details.
        
        Args:
            status_code: Response status code
            headers: Response headers
            body: Response body
            elapsed_time: Request elapsed time in seconds
        """
        if elapsed_time:
            self.info(f"Response: {status_code} ({elapsed_time:.2f}s)")
        else:
            self.info(f"Response: {status_code}")

        if headers:
            self.debug(f"Response Headers: {headers}")
        if body:
            self.debug(f"Response Body: {body}")


def get_logger(name: str, log_file: Optional[str] = None) -> Logger:
    """Get logger instance.
    
    Args:
        name: Logger name
        log_file: Optional log file path
        
    Returns:
        Logger instance
    """
    return Logger(name, log_file)

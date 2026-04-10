"""
Logging utility for Stauto
"""

import logging
import logging.handlers
from pathlib import Path
from config.settings import SETTINGS


def setup_logger(name: str) -> logging.Logger:
    """
    Setup logger with both file and console handlers
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    # Set log level
    log_level = SETTINGS.get("log_level", "INFO")
    logger.setLevel(getattr(logging, log_level))
    
    # Create logs directory if it doesn't exist
    log_dir = Path(SETTINGS.get("log_file", "logs/stauto.log")).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler with rotation
    log_file = SETTINGS.get("log_file", "logs/stauto.log")
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

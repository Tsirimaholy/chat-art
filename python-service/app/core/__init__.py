"""
Core Package for FAQ Finance Chatbot

This package contains core functionality including configuration,
logging utilities, and other shared components.
"""

from .config import settings
from .logging import setup_logging, log_interaction

__all__ = ["settings", "setup_logging", "log_interaction"]
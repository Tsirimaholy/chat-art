"""
Models Package for FAQ Finance Chatbot

This package contains all Pydantic models and data schemas
used for request/response validation and data structures.
"""

from .schemas import ChatRequest, ChatResponse

__all__ = ["ChatRequest", "ChatResponse"]
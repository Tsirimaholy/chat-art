"""
Pydantic schemas for FAQ Finance Chatbot

This module contains all request and response models used for API validation
and data serialization/deserialization.
"""

from pydantic import BaseModel, Field
from typing import List


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User question to be processed by the chatbot"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What is EBITDA?"
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str = Field(
        ...,
        description="Bot's answer to the user question"
    )
    sources: List[str] = Field(
        default_factory=list,
        description="List of source IDs used to generate the answer"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "EBITDA (Earnings Before Interest, Taxes, Depreciation and Amortization) is an operational performance indicator...",
                "sources": ["faq#ebitda"]
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str = Field(
        ...,
        description="Service health status"
    )
    faq_entries: int = Field(
        ...,
        description="Number of FAQ entries loaded"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "faq_entries": 15
            }
        }


class ServiceInfoResponse(BaseModel):
    """Response model for service info endpoint"""
    service: str = Field(
        ...,
        description="Service name"
    )
    status: str = Field(
        ...,
        description="Service status"
    )
    endpoints: List[str] = Field(
        ...,
        description="Available API endpoints"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "service": "FAQ Finance Chatbot",
                "status": "running",
                "endpoints": ["/chat"]
            }
        }
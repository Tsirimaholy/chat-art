"""
Knowledge base management for FAQ Finance Chatbot

This module handles loading and managing the FAQ knowledge base data.
It provides a clean interface for accessing FAQ entries and handles
file loading with proper error handling.
"""

import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path

from ..core.config import settings
from ..core.logging import get_logger

logger = get_logger(__name__)


class KnowledgeBaseError(Exception):
    """Custom exception for knowledge base related errors"""
    pass


class KnowledgeBase:
    """
    Knowledge base manager for FAQ data

    This class handles loading, caching, and providing access to the FAQ
    knowledge base. It ensures the data is properly loaded and validated.
    """

    def __init__(self, faq_file_path: Optional[str] = None):
        """
        Initialize the knowledge base

        Args:
            faq_file_path (Optional[str]): Path to FAQ JSON file.
                                         If None, uses settings default.
        """
        self.faq_file_path = faq_file_path or settings.faq_file_path
        self._faq_data = []
        self._loaded = False
        
    def load_faq_data(self) -> None:
        """
        Load FAQ data from JSON file
        
        Raises:
            KnowledgeBaseError: If file cannot be loaded or data is invalid
        """
        try:
            # Handle both absolute and relative paths
            if not os.path.isabs(self.faq_file_path):
                # Convert to absolute path relative to project root
                project_root = Path(__file__).parent.parent.parent
                file_path = project_root / self.faq_file_path
            else:
                file_path = Path(self.faq_file_path)
            
            if not file_path.exists():
                raise KnowledgeBaseError(f"FAQ file not found: {file_path}")
            
            with open(file_path, "r", encoding="utf-8") as f:
                self._faq_data = json.load(f)
            
            # Validate the loaded data
            self._validate_faq_data()
            self._loaded = True
            
            logger.info(f"Loaded {len(self._faq_data)} FAQ entries from {file_path}")
            
        except json.JSONDecodeError as e:
            raise KnowledgeBaseError(f"Invalid JSON in FAQ file: {e}")
        except Exception as e:
            raise KnowledgeBaseError(f"Failed to load FAQ data: {e}")
    
    def _validate_faq_data(self) -> None:
        """
        Validate the structure of loaded FAQ data
        
        Raises:
            KnowledgeBaseError: If data structure is invalid
        """
        if not isinstance(self._faq_data, list):
            raise KnowledgeBaseError("FAQ data must be a list of entries")
        
        if not self._faq_data:
            raise KnowledgeBaseError("FAQ data cannot be empty")
        
        required_fields = {"id", "q", "a"}
        
        for i, entry in enumerate(self._faq_data):
            if not isinstance(entry, dict):
                raise KnowledgeBaseError(f"FAQ entry {i} must be a dictionary")
            
            missing_fields = required_fields - set(entry.keys())
            if missing_fields:
                raise KnowledgeBaseError(
                    f"FAQ entry {i} missing required fields: {missing_fields}"
                )
            
            # Validate field types and content
            if not isinstance(entry["id"], str) or not entry["id"].strip():
                raise KnowledgeBaseError(f"FAQ entry {i} has invalid 'id' field")
            
            if not isinstance(entry["q"], str) or not entry["q"].strip():
                raise KnowledgeBaseError(f"FAQ entry {i} has invalid 'q' field")
            
            if not isinstance(entry["a"], str) or not entry["a"].strip():
                raise KnowledgeBaseError(f"FAQ entry {i} has invalid 'a' field")
    
    @property
    def faq_data(self) -> List[Dict[str, Any]]:
        """
        Get the FAQ data, loading it if necessary
        
        Returns:
            List[Dict[str, Any]]: List of FAQ entries
            
        Raises:
            KnowledgeBaseError: If data cannot be loaded
        """
        if not self._loaded:
            self.load_faq_data()
        return self._faq_data
    
    @property
    def questions(self) -> List[str]:
        """
        Get all questions from the FAQ data
        
        Returns:
            List[str]: List of FAQ questions
        """
        return [entry["q"] for entry in self.faq_data]
    
    def get_entry_by_id(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific FAQ entry by its ID
        
        Args:
            entry_id (str): The ID of the FAQ entry
            
        Returns:
            Optional[Dict[str, Any]]: FAQ entry if found, None otherwise
        """
        for entry in self.faq_data:
            if entry["id"] == entry_id:
                return entry
        return None
    
    def get_entry_by_index(self, index: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific FAQ entry by its index
        
        Args:
            index (int): The index of the FAQ entry
            
        Returns:
            Optional[Dict[str, Any]]: FAQ entry if index is valid, None otherwise
        """
        try:
            return self.faq_data[index]
        except IndexError:
            return None
    
    def search_questions(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Search for FAQ entries containing a keyword in the question
        
        Args:
            keyword (str): Keyword to search for
            
        Returns:
            List[Dict[str, Any]]: List of matching FAQ entries
        """
        keyword_lower = keyword.lower()
        matches = []
        
        for entry in self.faq_data:
            if keyword_lower in entry["q"].lower():
                matches.append(entry)
                
        return matches
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the knowledge base
        
        Returns:
            Dict[str, Any]: Dictionary containing knowledge base statistics
        """
        if not self._loaded:
            self.load_faq_data()
            
        return {
            "total_entries": len(self._faq_data),
            "avg_question_length": sum(len(entry["q"]) for entry in self._faq_data) / len(self._faq_data),
            "avg_answer_length": sum(len(entry["a"]) for entry in self._faq_data) / len(self._faq_data),
            "unique_ids": len(set(entry["id"] for entry in self._faq_data)),
            "loaded": self._loaded,
            "file_path": str(self.faq_file_path)
        }
    
    def reload(self) -> None:
        """
        Reload the FAQ data from file
        
        This method forces a reload of the data from the file,
        useful for development or when the file has been updated.
        """
        self._loaded = False
        self._faq_data = []
        self.load_faq_data()
        logger.info("Knowledge base reloaded")


# Global knowledge base instance
knowledge_base = KnowledgeBase()
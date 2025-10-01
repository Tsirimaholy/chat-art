"""
Tests for service modules (FAQ service and knowledge base)

This module contains unit tests for the core business logic services
including FAQ matching and knowledge base management.
"""

import pytest
import tempfile
import json
import os
from unittest.mock import patch, MagicMock

from app.services.knowledge_base import KnowledgeBase, KnowledgeBaseError
from app.services.faq_service import FAQService, FAQServiceError
from app.core.config import settings


class TestKnowledgeBase:
    """Test cases for KnowledgeBase class"""

    def create_temp_faq_file(self, data):
        """Helper to create temporary FAQ file"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(data, temp_file, ensure_ascii=False, indent=2)
        temp_file.close()
        return temp_file.name

    def test_load_valid_faq_data(self):
        """Test loading valid FAQ data"""
        test_data = [
            {"id": "test1", "q": "Test question?", "a": "Test answer."},
            {"id": "test2", "q": "Another question?", "a": "Another answer."}
        ]

        temp_file = self.create_temp_faq_file(test_data)

        try:
            kb = KnowledgeBase(temp_file)
            kb.load_faq_data()

            assert kb.faq_data == test_data
            assert len(kb.questions) == 2
            assert kb.questions[0] == "Test question?"
        finally:
            os.unlink(temp_file)

    def test_load_missing_file(self):
        """Test loading from non-existent file"""
        kb = KnowledgeBase("non_existent_file.json")

        with pytest.raises(KnowledgeBaseError, match="FAQ file not found"):
            kb.load_faq_data()

    def test_load_invalid_json(self):
        """Test loading invalid JSON file"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        temp_file.write("invalid json content")
        temp_file.close()

        try:
            kb = KnowledgeBase(temp_file.name)
            with pytest.raises(KnowledgeBaseError, match="Invalid JSON"):
                kb.load_faq_data()
        finally:
            os.unlink(temp_file.name)

    def test_validate_missing_fields(self):
        """Test validation of FAQ entries with missing fields"""
        invalid_data = [
            {"id": "test1", "q": "Test question?"},  # Missing 'a' field
        ]

        temp_file = self.create_temp_faq_file(invalid_data)

        try:
            kb = KnowledgeBase(temp_file)
            with pytest.raises(KnowledgeBaseError, match="missing required fields"):
                kb.load_faq_data()
        finally:
            os.unlink(temp_file)

    def test_validate_empty_data(self):
        """Test validation of empty FAQ data"""
        empty_data = []

        temp_file = self.create_temp_faq_file(empty_data)

        try:
            kb = KnowledgeBase(temp_file)
            with pytest.raises(KnowledgeBaseError, match="FAQ data cannot be empty"):
                kb.load_faq_data()
        finally:
            os.unlink(temp_file)

    def test_get_entry_by_id(self):
        """Test retrieving FAQ entry by ID"""
        test_data = [
            {"id": "test1", "q": "Test question?", "a": "Test answer."},
            {"id": "test2", "q": "Another question?", "a": "Another answer."}
        ]

        temp_file = self.create_temp_faq_file(test_data)

        try:
            kb = KnowledgeBase(temp_file)
            kb.load_faq_data()

            entry = kb.get_entry_by_id("test1")
            assert entry is not None
            assert entry["q"] == "Test question?"

            not_found = kb.get_entry_by_id("nonexistent")
            assert not_found is None
        finally:
            os.unlink(temp_file)

    def test_search_questions(self):
        """Test searching questions by keyword"""
        test_data = [
            {"id": "test1", "q": "What is EBITDA?", "a": "EBITDA explanation."},
            {"id": "test2", "q": "How to calculate ROE?", "a": "ROE calculation."},
            {"id": "test3", "q": "What is cash flow?", "a": "Cash flow definition."}
        ]

        temp_file = self.create_temp_faq_file(test_data)

        try:
            kb = KnowledgeBase(temp_file)
            kb.load_faq_data()

            results = kb.search_questions("EBITDA")
            assert len(results) == 1
            assert results[0]["id"] == "test1"

            results = kb.search_questions("what")
            assert len(results) == 2  # "What is EBITDA?" and "What is cash flow?"
        finally:
            os.unlink(temp_file)

    def test_get_stats(self):
        """Test knowledge base statistics"""
        test_data = [
            {"id": "test1", "q": "Short?", "a": "Short answer."},
            {"id": "test2", "q": "Longer question here?", "a": "Much longer answer with more details."}
        ]

        temp_file = self.create_temp_faq_file(test_data)

        try:
            kb = KnowledgeBase(temp_file)
            kb.load_faq_data()

            stats = kb.get_stats()
            assert stats["total_entries"] == 2
            assert stats["loaded"] == True
            assert stats["unique_ids"] == 2
            assert "avg_question_length" in stats
            assert "avg_answer_length" in stats
        finally:
            os.unlink(temp_file)


class TestFAQService:
    """Test cases for FAQService class"""

    @pytest.fixture
    def sample_kb(self):
        """Create a sample knowledge base for testing"""
        test
_data = [
            {"id": "faq1", "q": "What is EBITDA?", "a": "EBITDA is a financial metric."},
            {"id": "faq2", "q": "How to calculate ROE?", "a": "ROE is calculated by dividing net income by equity."},
            {"id": "faq3", "q": "What is cash flow?", "a": "Cash flow is the movement of money."}
        ]

        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(test_data, temp_file, ensure_ascii=False, indent=2)
        temp_file.close()

        kb = KnowledgeBase(temp_file.name)
        kb.load_faq_data()

        yield kb

        os.unlink(temp_file.name)

    def test_service_initialization(self, sample_kb):
        """Test FAQ service initialization"""
        service = FAQService(kb=sample_kb, threshold=0.3)
        assert not service._initialized

        service.initialize()
        assert service._initialized
        assert service._vectorizer is not None
        assert service._faq_vectors is not None

    def test_find_exact_match(self, sample_kb):
        """Test finding exact matches"""
        service = FAQService(kb=sample_kb, threshold=0.1)
        service.initialize()

        result = service.find_best_match("What is EBITDA?")
        assert result is not None
        assert result["id"] == "faq1"
        assert "_similarity_score" in result
        assert result["_similarity_score"] > 0.9  # Should be very high for exact match

    def test_find_partial_match(self, sample_kb):
        """Test finding partial matches"""
        service = FAQService(kb=sample_kb, threshold=0.1)
        service.initialize()

        result = service.find_best_match("EBITDA definition")
        assert result is not None
        assert result["id"] == "faq1"
        assert result["_similarity_score"] > 0.1

    def test_no_match_below_threshold(self, sample_kb):
        """Test when no match exceeds threshold"""
        service = FAQService(kb=sample_kb, threshold=0.9)  # Very high threshold
        service.initialize()

        result = service.find_best_match("How to cook pasta?")
        assert result is None

    def test_process_query_with_match(self, sample_kb):
        """Test processing query that finds a match"""
        service = FAQService(kb=sample_kb, threshold=0.1)
        service.initialize()

        result = service.process_query("What is EBITDA?")
        assert result["matched"] == True
        assert result["answer"] == "EBITDA is a financial metric."
        assert result["sources"] == ["faq1"]
        assert result["similarity_score"] > 0.9

    def test_process_query_no_match(self, sample_kb):
        """Test processing query that finds no match"""
        service = FAQService(kb=sample_kb, threshold=0.9)  # Very high threshold
        service.initialize()

        result = service.process_query("How to cook pasta?")
        assert result["matched"] == False
        assert "désolé" in result["answer"].lower()
        assert result["sources"] == []
        assert result["similarity_score"] == 0.0

    def test_get_multiple_matches(self, sample_kb):
        """Test getting multiple matches"""
        service = FAQService(kb=sample_kb, threshold=0.01)
        service.initialize()

        matches = service.get_multiple_matches("financial metric", top_k=3)
        assert isinstance(matches, list)
        assert len(matches) >= 1  # Should find at least EBITDA

        for match in matches:
            assert "_similarity_score" in match
            assert match["_similarity_score"] > 0.01

    def test_update_threshold(self, sample_kb):
        """Test updating similarity threshold"""
        service = FAQService(kb=sample_kb, threshold=0.3)

        service.update_threshold(0.5)
        assert service.threshold == 0.5

        with pytest.raises(ValueError):
            service.update_threshold(-0.1)  # Invalid threshold

        with pytest.raises(ValueError):
            service.update_threshold(1.1)  # Invalid threshold

    def test_service_not_initialized_error(self, sample_kb):
        """Test error when service is not initialized"""
        service = FAQService(kb=sample_kb)

        with pytest.raises(FAQServiceError, match="not initialized"):
            service.find_best_match("test query")

        with pytest.raises(FAQServiceError, match="not initialized"):
            service.get
_multiple_matches("test query")
    
    def test_empty_query_handling(self, sample_kb):
        """Test handling of empty queries"""
        service = FAQService(kb=sample_kb)
        service.initialize()
        
        assert service.find_best_match("") is None
        assert service.find_best_match("   ") is None
        assert service.get_multiple_matches("") == []
    
    def test_get_service_stats(self, sample_kb):
        """Test getting service statistics"""
        service = FAQService(kb=sample_kb)
        service.initialize()
        
        stats = service.get_service_stats()
        assert stats["initialized"] == True
        assert stats["threshold"] > 0
        assert stats["vectorizer_vocab_size"] > 0
        assert stats["total_entries"] == 3
        assert "faq_vectors_shape" in stats


class TestServiceIntegration:
    """Integration tests for services working together"""
    
    def test_end_to_end_query_processing(self):
        """Test complete query processing flow"""
        # This would use the actual FAQ data if available
        with patch('app.services.knowledge_base.settings') as mock_settings:
            # Mock the settings to use test data
            test_data = [
                {"id": "integration1", "q": "What is working capital?", "a": "Working capital is current assets minus current liabilities."}
            ]
            
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
            json.dump(test_data, temp_file, ensure_ascii=False, indent=2)
            temp_file.close()
            
            mock_settings.faq_file_path = temp_file.name
            
            try:
                kb = KnowledgeBase()
                service = FAQService(kb=kb)
                service.initialize()
                
                # Test successful query
                result = service.process_query("working capital definition")
                assert result["matched"] == True
                assert "working capital" in result["answer"].lower()
                
                # Test unsuccessful query
                result = service.process_query("random unrelated query")
                assert result["matched"] == False
                assert result["sources"] == []
                
            finally:
                os.unlink(temp_file.name)
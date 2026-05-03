import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.vqa_service import VQAService

class TestVQAService:
    def setup_method(self):
        self.vqa_service = VQAService()
    
    def test_single_question_qa(self):
        result = self.vqa_service.visual_question_answer("test.txt", "这是什么？")
        assert result.get("success") == False
        assert result.get("error") == "不支持的图片格式"
    
    def test_multi_turn_qa_empty(self):
        result = self.vqa_service.multi_turn_qa("test.txt", [])
        assert result.get("success") == False
    
    def test_reasoning_qa_invalid_format(self):
        result = self.vqa_service.reasoning_qa("test.txt", "分析一下")
        assert result.get("success") == False
        assert result.get("error") == "不支持的图片格式"
    
    def test_conversation_history(self):
        assert len(self.vqa_service.conversation_history) == 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

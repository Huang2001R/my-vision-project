import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.vision_service import VisionService
from app.utils.image_utils import validate_image_format

class TestVisionService:
    def setup_method(self):
        self.vision_service = VisionService()
    
    def test_validate_image_format(self):
        assert validate_image_format("test.jpg") == True
        assert validate_image_format("test.png") == True
        assert validate_image_format("test.gif") == True
        assert validate_image_format("test.bmp") == True
        assert validate_image_format("test.txt") == False
        assert validate_image_format("test.pdf") == False
    
    def test_describe_image_invalid_format(self):
        result = self.vision_service.describe_image("test.txt")
        assert result.get("error") == "不支持的图片格式"
    
    def test_detect_objects_invalid_format(self):
        result = self.vision_service.detect_objects("test.txt")
        assert result.get("error") == "不支持的图片格式"
    
    def test_analyze_scene_invalid_format(self):
        result = self.vision_service.analyze_scene("test.txt")
        assert result.get("error") == "不支持的图片格式"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

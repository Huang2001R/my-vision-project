import requests
import base64
from PIL import Image
from io import BytesIO

from app.config.settings import settings
from app.utils.logger import logger

class VisionClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def initialize(self):
        if self._initialized:
            return
        
        self.api_key = settings.vision_api_key
        self.api_base_url = settings.vision_api_base_url
        
        if not self.api_key:
            raise ValueError("Vision API Key not configured")
        
        self._initialized = True
    
    def image_to_base64(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    
    def describe_image(self, image_path: str) -> str:
        if not self._initialized:
            self.initialize()
        
        base64_image = self.image_to_base64(image_path)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llava-1.5-7b",
            "prompt": "请详细描述这张图片的内容，包括物体、场景、颜色、动作等信息。",
            "image": base64_image,
            "max_tokens": settings.max_new_tokens,
            "temperature": settings.temperature
        }
        
        try:
            response = requests.post(
                f"{self.api_base_url}/vision/describe",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result.get("description", "")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Vision API调用失败: {str(e)}")
            raise
    
    def visual_qa(self, image_path: str, question: str) -> str:
        if not self._initialized:
            self.initialize()
        
        base64_image = self.image_to_base64(image_path)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llava-1.5-7b",
            "question": question,
            "image": base64_image,
            "max_tokens": settings.max_new_tokens,
            "temperature": settings.temperature
        }
        
        try:
            response = requests.post(
                f"{self.api_base_url}/vision/qa",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result.get("answer", "")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Vision QA API调用失败: {str(e)}")
            raise
    
    def detect_objects(self, image_path: str) -> str:
        if not self._initialized:
            self.initialize()
        
        base64_image = self.image_to_base64(image_path)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llava-1.5-7b",
            "prompt": "请识别图片中的所有物体，并列出它们的名称和位置。",
            "image": base64_image,
            "max_tokens": settings.max_new_tokens,
            "temperature": settings.temperature
        }
        
        try:
            response = requests.post(
                f"{self.api_base_url}/vision/detect",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result.get("objects", "")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Object Detection API调用失败: {str(e)}")
            raise

vision_client = VisionClient()

import requests
import json

from app.config.settings import settings
from app.utils.logger import logger

class QwenClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def initialize(self):
        if self._initialized:
            return
        
        self.api_key = settings.qwen_api_key
        self.api_base_url = settings.qwen_api_base_url
        self.default_model = settings.qwen_model_name
        
        if not self.api_key:
            raise ValueError("Qwen API Key not configured")
        
        self._initialized = True
    
    def generate(self, prompt: str, max_new_tokens: int = None) -> str:
        if not self._initialized:
            self.initialize()
        
        max_tokens = max_new_tokens or settings.max_new_tokens
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.default_model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": settings.temperature,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.api_base_url}/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result.get("choices", [{}])[0].get("text", "")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Qwen API调用失败: {str(e)}")
            raise
    
    def chat(self, messages: list) -> str:
        if not self._initialized:
            self.initialize()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.default_model,
            "messages": messages,
            "max_tokens": settings.max_new_tokens,
            "temperature": settings.temperature,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.api_base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Qwen Chat API调用失败: {str(e)}")
            raise

qwen_client = QwenClient()

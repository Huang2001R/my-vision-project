from typing import Dict, Any

from app.clients.vision_client import vision_client
from app.utils.image_utils import load_image, resize_image, get_image_metadata, validate_image_format
from app.utils.logger import logger
from app.config.settings import settings

class VisionService:
    @staticmethod
    def describe_image(image_path: str) -> Dict[str, Any]:
        try:
            if not validate_image_format(image_path):
                return {"success": False, "error": "不支持的图片格式"}
            
            image = load_image(image_path)
            image = resize_image(image)
            
            temp_path = str(settings.upload_dir / "temp_describe.jpg")
            image.save(temp_path)
            
            description = vision_client.describe_image(temp_path)
            
            metadata = get_image_metadata(image_path)
            
            return {
                "success": True,
                "description": description,
                "metadata": metadata
            }
        
        except Exception as e:
            logger.error(f"图像描述失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def detect_objects(image_path: str) -> Dict[str, Any]:
        try:
            if not validate_image_format(image_path):
                return {"success": False, "error": "不支持的图片格式"}
            
            image = load_image(image_path)
            image = resize_image(image)
            
            temp_path = str(settings.upload_dir / "temp_detect.jpg")
            image.save(temp_path)
            
            objects = vision_client.detect_objects(temp_path)
            
            metadata = get_image_metadata(image_path)
            
            return {
                "success": True,
                "objects": objects,
                "metadata": metadata
            }
        
        except Exception as e:
            logger.error(f"物体检测失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def analyze_scene(image_path: str) -> Dict[str, Any]:
        try:
            if not validate_image_format(image_path):
                return {"success": False, "error": "不支持的图片格式"}
            
            image = load_image(image_path)
            image = resize_image(image)
            
            temp_path = str(settings.upload_dir / "temp_scene.jpg")
            image.save(temp_path)
            
            analysis = vision_client.visual_qa(
                temp_path,
                "请分析这张图片的场景类型、环境氛围、光线条件和主要元素。"
            )
            
            metadata = get_image_metadata(image_path)
            
            return {
                "success": True,
                "analysis": analysis,
                "metadata": metadata
            }
        
        except Exception as e:
            logger.error(f"场景分析失败: {str(e)}")
            return {"success": False, "error": str(e)}

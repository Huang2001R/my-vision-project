from typing import Dict, Any, List
from pathlib import Path

from app.clients.vision_client import vision_client
from app.clients.qwen_client import qwen_client
from app.utils.image_utils import load_image, resize_image, validate_image_format
from app.utils.logger import logger
from app.config.settings import settings

class VQAService:
    def __init__(self):
        self.conversation_history = []
    
    def visual_question_answer(self, image_path: str, question: str) -> Dict[str, Any]:
        try:
            if not validate_image_format(image_path):
                return {"success": False, "error": "不支持的图片格式"}
            
            image = load_image(image_path)
            image = resize_image(image)
            
            temp_path = str(settings.upload_dir / "temp_vqa.jpg")
            image.save(temp_path)
            
            answer = vision_client.visual_qa(temp_path, question)
            
            self.conversation_history.append({
                "question": question,
                "answer": answer,
                "image_path": image_path
            })
            
            return {
                "success": True,
                "answer": answer,
                "question": question
            }
        
        except Exception as e:
            logger.error(f"视觉问答失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def multi_turn_qa(self, image_path: str, questions: List[str]) -> Dict[str, Any]:
        results = []
        
        try:
            if not validate_image_format(image_path):
                return {"success": False, "error": "不支持的图片格式"}
            
            image = load_image(image_path)
            image = resize_image(image)
            
            temp_path = str(settings.upload_dir / "temp_multi.jpg")
            image.save(temp_path)
            
            for question in questions:
                answer = vision_client.visual_qa(temp_path, question)
                
                results.append({
                    "question": question,
                    "answer": answer
                })
            
            return {
                "success": True,
                "results": results,
                "count": len(results)
            }
        
        except Exception as e:
            logger.error(f"多轮问答失败: {str(e)}")
            return {"success": False, "error": str(e), "results": results}
    
    def reasoning_qa(self, image_path: str, question: str) -> Dict[str, Any]:
        try:
            if not validate_image_format(image_path):
                return {"success": False, "error": "不支持的图片格式"}
            
            image = load_image(image_path)
            image = resize_image(image)
            
            temp_path = str(settings.upload_dir / "temp_reasoning.jpg")
            image.save(temp_path)
            
            initial_answer = vision_client.visual_qa(temp_path, question)
            
            reasoning_prompt = f"""
            基于以下视觉问答结果，请进行深度推理分析：
            
            问题：{question}
            初步答案：{initial_answer}
            
            请分析：
            1. 答案的合理性
            2. 可能的推理过程
            3. 是否存在歧义或需要进一步确认的信息
            """
            
            deep_analysis = qwen_client.generate(reasoning_prompt)
            
            return {
                "success": True,
                "question": question,
                "initial_answer": initial_answer,
                "deep_analysis": deep_analysis
            }
        
        except Exception as e:
            logger.error(f"推理问答失败: {str(e)}")
            return {"success": False, "error": str(e)}

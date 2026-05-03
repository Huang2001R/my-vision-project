from typing import Dict, Any
import pytesseract
from PIL import Image
import cv2
import numpy as np

from app.clients.qwen_client import qwen_client
from app.utils.image_utils import load_image, resize_image, validate_image_format
from app.utils.logger import logger

class DocumentService:
    @staticmethod
    def ocr_recognition(image_path: str) -> Dict[str, Any]:
        try:
            if not validate_image_format(image_path):
                return {"success": False, "error": "不支持的图片格式"}
            
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            thresh = cv2.threshold(
                gray, 0, 255, 
                cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
            )[1]
            
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(thresh, config=custom_config)
            
            return {
                "success": True,
                "text": text,
                "length": len(text)
            }
        
        except Exception as e:
            logger.error(f"OCR识别失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def extract_table(image_path: str) -> Dict[str, Any]:
        try:
            if not validate_image_format(image_path):
                return {"success": False, "error": "不支持的图片格式"}
            
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            thresh = cv2.threshold(
                gray, 0, 255, 
                cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
            )[1]
            
            horizontal_lines = cv2.HoughLinesP(
                thresh, 1, np.pi/180, threshold=100, 
                minLineLength=100, maxLineGap=5
            )
            
            vertical_lines = cv2.HoughLinesP(
                thresh, 1, np.pi/180, threshold=100, 
                minLineLength=100, maxLineGap=5
            )
            
            has_table = horizontal_lines is not None or vertical_lines is not None
            
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(gray, config=custom_config)
            
            return {
                "success": True,
                "has_table": has_table,
                "text": text,
                "horizontal_lines_count": len(horizontal_lines) if horizontal_lines is not None else 0,
                "vertical_lines_count": len(vertical_lines) if vertical_lines is not None else 0
            }
        
        except Exception as e:
            logger.error(f"表格提取失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def analyze_document(image_path: str) -> Dict[str, Any]:
        try:
            if not validate_image_format(image_path):
                return {"success": False, "error": "不支持的图片格式"}
            
            ocr_result = DocumentService.ocr_recognition(image_path)
            if not ocr_result["success"]:
                return ocr_result
            
            table_result = DocumentService.extract_table(image_path)
            
            analysis_prompt = f"""
            请分析以下文档内容：
            
            文档文本：{ocr_result["text"]}
            是否包含表格：{"是" if table_result["has_table"] else "否"}
            
            请提供：
            1. 文档类型判断（如合同、报告、简历等）
            2. 主要内容摘要
            3. 关键信息提取
            4. 建议的后续处理
            """
            
            analysis = qwen_client.generate(analysis_prompt)
            
            return {
                "success": True,
                "ocr_text": ocr_result["text"],
                "has_table": table_result["has_table"],
                "analysis": analysis
            }
        
        except Exception as e:
            logger.error(f"文档分析失败: {str(e)}")
            return {"success": False, "error": str(e)}

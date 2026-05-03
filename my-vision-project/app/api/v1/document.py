from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Dict, Any
import shutil

from app.services.document_service import DocumentService
from app.config.settings import settings

router = APIRouter()
document_service = DocumentService()

@router.post("/ocr", summary="OCR文字识别")
async def ocr_recognition(file: UploadFile = File(...)) -> Dict[str, Any]:
    try:
        file_path = settings.upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        result = document_service.ocr_recognition(str(file_path))
        
        if not result.get("success", False):
            raise HTTPException(status_code=500, detail=result.get("error", "处理失败"))
        
        return {
            "status": "success",
            "text": result["text"],
            "length": result["length"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/table", summary="表格提取")
async def extract_table(file: UploadFile = File(...)) -> Dict[str, Any]:
    try:
        file_path = settings.upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        result = document_service.extract_table(str(file_path))
        
        if not result.get("success", False):
            raise HTTPException(status_code=500, detail=result.get("error", "处理失败"))
        
        return {
            "status": "success",
            "has_table": result["has_table"],
            "text": result["text"],
            "horizontal_lines": result["horizontal_lines_count"],
            "vertical_lines": result["vertical_lines_count"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze", summary="文档分析")
async def analyze_document(file: UploadFile = File(...)) -> Dict[str, Any]:
    try:
        file_path = settings.upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        result = document_service.analyze_document(str(file_path))
        
        if not result.get("success", False):
            raise HTTPException(status_code=500, detail=result.get("error", "处理失败"))
        
        return {
            "status": "success",
            "ocr_text": result["ocr_text"],
            "has_table": result["has_table"],
            "analysis": result["analysis"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

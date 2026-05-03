from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Dict, Any
import shutil
from pathlib import Path

from app.services.vision_service import VisionService
from app.config.settings import settings

router = APIRouter()
vision_service = VisionService()

@router.post("/describe", summary="图像内容描述")
async def describe_image(file: UploadFile = File(...)) -> Dict[str, Any]:
    try:
        file_path = settings.upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        result = vision_service.describe_image(str(file_path))
        
        if not result.get("success", False):
            raise HTTPException(status_code=500, detail=result.get("error", "处理失败"))
        
        return {
            "status": "success",
            "description": result["description"],
            "metadata": result["metadata"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/detect", summary="物体检测")
async def detect_objects(file: UploadFile = File(...)) -> Dict[str, Any]:
    try:
        file_path = settings.upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        result = vision_service.detect_objects(str(file_path))
        
        if not result.get("success", False):
            raise HTTPException(status_code=500, detail=result.get("error", "处理失败"))
        
        return {
            "status": "success",
            "objects": result["objects"],
            "metadata": result["metadata"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze", summary="场景分析")
async def analyze_scene(file: UploadFile = File(...)) -> Dict[str, Any]:
    try:
        file_path = settings.upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        result = vision_service.analyze_scene(str(file_path))
        
        if not result.get("success", False):
            raise HTTPException(status_code=500, detail=result.get("error", "处理失败"))
        
        return {
            "status": "success",
            "analysis": result["analysis"],
            "metadata": result["metadata"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

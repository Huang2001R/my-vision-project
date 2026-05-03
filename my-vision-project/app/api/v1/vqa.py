from fastapi import APIRouter, File, UploadFile, HTTPException, Body
from typing import Dict, Any, List
import shutil

from app.services.vqa_service import VQAService
from app.config.settings import settings

router = APIRouter()
vqa_service = VQAService()

@router.post("/query", summary="视觉问答")
async def visual_qa(
    file: UploadFile = File(...),
    question: str = Body(..., embed=True)
) -> Dict[str, Any]:
    try:
        file_path = settings.upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        result = vqa_service.visual_question_answer(str(file_path), question)
        
        if not result.get("success", False):
            raise HTTPException(status_code=500, detail=result.get("error", "处理失败"))
        
        return {
            "status": "success",
            "question": result["question"],
            "answer": result["answer"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/multi-turn", summary="多轮视觉问答")
async def multi_turn_vqa(
    file: UploadFile = File(...),
    questions: List[str] = Body(..., embed=True)
) -> Dict[str, Any]:
    try:
        file_path = settings.upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        result = vqa_service.multi_turn_qa(str(file_path), questions)
        
        if not result.get("success", False):
            raise HTTPException(status_code=500, detail=result.get("error", "处理失败"))
        
        return {
            "status": "success",
            "count": result["count"],
            "results": result["results"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reasoning", summary="推理问答")
async def reasoning_vqa(
    file: UploadFile = File(...),
    question: str = Body(..., embed=True)
) -> Dict[str, Any]:
    try:
        file_path = settings.upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        result = vqa_service.reasoning_qa(str(file_path), question)
        
        if not result.get("success", False):
            raise HTTPException(status_code=500, detail=result.get("error", "处理失败"))
        
        return {
            "status": "success",
            "question": result["question"],
            "initial_answer": result["initial_answer"],
            "deep_analysis": result["deep_analysis"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1 import vision, vqa, document
from app.config.settings import Settings

settings = Settings()

app = FastAPI(
    title="Qwen-Vision API",
    description="基于Qwen-3.5的本地多模态视觉理解系统",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vision.router, prefix="/api/v1/vision", tags=["视觉分析"])
app.include_router(vqa.router, prefix="/api/v1/vqa", tags=["视觉问答"])
app.include_router(document.router, prefix="/api/v1/document", tags=["文档分析"])

@app.get("/api/v1/health", tags=["健康检查"])
async def health_check():
    return {
        "status": "healthy",
        "service": "Qwen-Vision",
        "version": "1.0.0",
        "models": {
            "llm": "Qwen-3.5",
            "vision": "LLaVA-1.5"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True
    )

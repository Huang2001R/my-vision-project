from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # 服务配置
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # Qwen API配置
    qwen_api_key: str = ""
    qwen_api_base_url: str = "https://api.qwenlm.cn/v1"
    qwen_model_name: str = "Qwen-3.5-7B-Instruct"
    
    # Vision API配置
    vision_api_key: str = ""
    vision_api_base_url: str = "https://api.vision.example.com/v1"
    
    # 模型配置（保留用于本地回退）
    model_dir: Path = Path(__file__).parent.parent.parent / "models"
    device: str = "cuda"
    load_in_4bit: bool = True
    max_new_tokens: int = 1024
    temperature: float = 0.2
    
    # 文件配置
    upload_dir: Path = Path(__file__).parent.parent.parent / "uploads"
    allowed_extensions: list = ["jpg", "jpeg", "png", "gif", "bmp", "pdf"]
    
    # 日志配置
    log_level: str = "INFO"
    log_file: Path = Path(__file__).parent.parent.parent / "logs" / "app.log"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

if not settings.upload_dir.exists():
    settings.upload_dir.mkdir(parents=True, exist_ok=True)

if not settings.log_file.parent.exists():
    settings.log_file.parent.mkdir(parents=True, exist_ok=True)

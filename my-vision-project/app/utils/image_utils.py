from PIL import Image
import cv2
import numpy as np
from pathlib import Path

def load_image(image_path: str) -> Image.Image:
    return Image.open(image_path).convert("RGB")

def save_image(image: Image.Image, save_path: str) -> None:
    image.save(save_path)

def resize_image(image: Image.Image, max_size: int = 1024) -> Image.Image:
    width, height = image.size
    
    if width > max_size or height > max_size:
        ratio = min(max_size / width, max_size / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        return image.resize((new_width, new_height), Image.LANCZOS)
    
    return image

def image_to_base64(image: Image.Image) -> str:
    import base64
    from io import BytesIO
    
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def base64_to_image(base64_str: str) -> Image.Image:
    import base64
    from io import BytesIO
    
    image_data = base64.b64decode(base64_str)
    return Image.open(BytesIO(image_data))

def detect_image_quality(image: Image.Image) -> dict:
    width, height = image.size
    mode = image.mode
    format_info = image.format
    
    np_image = np.array(image)
    
    brightness = np.mean(np_image)
    contrast = np.std(np_image)
    
    return {
        "width": width,
        "height": height,
        "mode": mode,
        "format": format_info,
        "brightness": brightness,
        "contrast": contrast
    }

def get_image_metadata(image_path: str) -> dict:
    image = Image.open(image_path)
    
    return {
        "filename": Path(image_path).name,
        "size": image.size,
        "mode": image.mode,
        "format": image.format,
        "info": image.info
    }

def validate_image_format(image_path: str, allowed_extensions: list = None) -> bool:
    if allowed_extensions is None:
        allowed_extensions = ["jpg", "jpeg", "png", "gif", "bmp"]
    
    ext = Path(image_path).suffix.lower()[1:]
    return ext in allowed_extensions

def preprocess_image_for_model(image_path: str) -> np.ndarray:
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    target_size = (224, 224)
    image = cv2.resize(image, target_size)
    
    image = image / 255.0
    image = np.transpose(image, (2, 0, 1))
    image = np.expand_dims(image, axis=0)
    
    return image

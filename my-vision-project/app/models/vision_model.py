from llava.constants import IMAGE_TOKEN_INDEX
from llava.conversation import conv_templates
from llava.model.builder import load_pretrained_model
from llava.utils import disable_torch_init
from PIL import Image
import torch

from app.config.settings import settings

class VisionModel:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def initialize(self):
        if self._initialized:
            return
        
        disable_torch_init()
        
        self.model, self.vis_processor, self.text_processor = load_pretrained_model(
            str(settings.model_dir / "llava-1.5"),
            settings.device,
            str(settings.model_dir / "llava-1.5"),
            load_in_4bit=settings.load_in_4bit
        )
        
        self.conv_template = conv_templates["llava_v1"].copy()
        self._initialized = True
    
    def describe_image(self, image_path: str) -> str:
        if not self._initialized:
            self.initialize()
        
        image = self.vis_processor(Image.open(image_path)).unsqueeze(0).to(settings.device)
        
        self.conv_template.clear_messages()
        self.conv_template.append_message(
            self.conv_template.roles[0],
            "请详细描述这张图片的内容，包括物体、场景、颜色、动作等信息。"
        )
        self.conv_template.append_message(self.conv_template.roles[1], None)
        prompt = self.conv_template.get_prompt()
        
        input_ids = self.text_processor([prompt]).input_ids.to(settings.device)
        
        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids,
                images=image,
                max_new_tokens=settings.max_new_tokens,
                temperature=settings.temperature,
                use_cache=True
            )
        
        response = self.text_processor.decode(output_ids[0], skip_special_tokens=True)
        return response
    
    def visual_qa(self, image_path: str, question: str) -> str:
        if not self._initialized:
            self.initialize()
        
        image = self.vis_processor(Image.open(image_path)).unsqueeze(0).to(settings.device)
        
        self.conv_template.clear_messages()
        self.conv_template.append_message(
            self.conv_template.roles[0],
            f"
{question}"
        )
        self.conv_template.append_message(self.conv_template.roles[1], None)
        prompt = self.conv_template.get_prompt()
        
        input_ids = self.text_processor([prompt]).input_ids.to(settings.device)
        
        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids,
                images=image,
                max_new_tokens=settings.max_new_tokens,
                temperature=settings.temperature,
                use_cache=True
            )
        
        response = self.text_processor.decode(output_ids[0], skip_special_tokens=True)
        return response
    
    def detect_objects(self, image_path: str) -> str:
        if not self._initialized:
            self.initialize()
        
        image = self.vis_processor(Image.open(image_path)).unsqueeze(0).to(settings.device)
        
        self.conv_template.clear_messages()
        self.conv_template.append_message(
            self.conv_template.roles[0],
            "请识别图片中的所有物体，并列出它们的名称和位置。"
        )
        self.conv_template.append_message(self.conv_template.roles[1], None)
        prompt = self.conv_template.get_prompt()
        
        input_ids = self.text_processor([prompt]).input_ids.to(settings.device)
        
        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids,
                images=image,
                max_new_tokens=settings.max_new_tokens,
                temperature=settings.temperature,
                use_cache=True
            )
        
        response = self.text_processor.decode(output_ids[0], skip_special_tokens=True)
        return response

vision_model = VisionModel()

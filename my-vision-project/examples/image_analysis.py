import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.vision_service import VisionService
from app.services.document_service import DocumentService

def main():
    if len(sys.argv) < 2:
        print("用法: python image_analysis.py <图片路径>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    vision_service = VisionService()
    document_service = DocumentService()
    
    print("=" * 60)
    print("GLM-Vision 图像分析演示")
    print("=" * 60)
    
    print("\n1. 图像内容描述:")
    print("-" * 40)
    result = vision_service.describe_image(image_path)
    if result["success"]:
        print(result["description"])
    else:
        print(f"错误: {result['error']}")
    
    print("\n2. 物体检测:")
    print("-" * 40)
    result = vision_service.detect_objects(image_path)
    if result["success"]:
        print(result["objects"])
    else:
        print(f"错误: {result['error']}")
    
    print("\n3. 场景分析:")
    print("-" * 40)
    result = vision_service.analyze_scene(image_path)
    if result["success"]:
        print(result["analysis"])
    else:
        print(f"错误: {result['error']}")
    
    print("\n4. OCR文字识别:")
    print("-" * 40)
    result = document_service.ocr_recognition(image_path)
    if result["success"]:
        print(result["text"])
    else:
        print(f"错误: {result['error']}")
    
    print("\n" + "=" * 60)
    print("分析完成!")

if __name__ == "__main__":
    main()

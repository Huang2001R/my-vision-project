import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.vqa_service import VQAService

def main():
    if len(sys.argv) < 2:
        print("用法: python vqa_demo.py <图片路径>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    vqa_service = VQAService()
    
    print("=" * 60)
    print("GLM-Vision 视觉问答演示")
    print("=" * 60)
    print("输入问题进行问答，输入 'exit' 结束")
    print("-" * 60)
    
    while True:
        question = input("请输入问题: ")
        
        if question.lower() == "exit":
            print("感谢使用 GLM-Vision!")
            break
        
        if not question.strip():
            print("请输入有效的问题")
            continue
        
        result = vqa_service.visual_question_answer(image_path, question)
        
        if result["success"]:
            print(f"答案: {result['answer']}")
        else:
            print(f"错误: {result['error']}")
        
        print("-" * 60)

if __name__ == "__main__":
    main()

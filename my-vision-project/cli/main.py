import click
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.vision_service import VisionService
from app.services.vqa_service import VQAService
from app.services.document_service import DocumentService

vision_service = VisionService()
vqa_service = VQAService()
document_service = DocumentService()

@click.group()
def cli():
    pass

@cli.command("describe")
@click.argument("image_path")
def describe_image(image_path):
    result = vision_service.describe_image(image_path)
    
    if result["success"]:
        click.echo("=== 图像描述 ===")
        click.echo(result["description"])
    else:
        click.echo(f"错误: {result['error']}", err=True)

@cli.command("detect")
@click.argument("image_path")
def detect_objects(image_path):
    result = vision_service.detect_objects(image_path)
    
    if result["success"]:
        click.echo("=== 物体检测 ===")
        click.echo(result["objects"])
    else:
        click.echo(f"错误: {result['error']}", err=True)

@cli.command("vqa")
@click.argument("image_path")
@click.argument("question")
def visual_qa(image_path, question):
    result = vqa_service.visual_question_answer(image_path, question)
    
    if result["success"]:
        click.echo("=== 视觉问答 ===")
        click.echo(f"问题: {result['question']}")
        click.echo(f"答案: {result['answer']}")
    else:
        click.echo(f"错误: {result['error']}", err=True)

@cli.command("ocr")
@click.argument("image_path")
def ocr_recognition(image_path):
    result = document_service.ocr_recognition(image_path)
    
    if result["success"]:
        click.echo("=== OCR识别 ===")
        click.echo(result["text"])
    else:
        click.echo(f"错误: {result['error']}", err=True)

@cli.command("analyze-document")
@click.argument("image_path")
def analyze_document(image_path):
    result = document_service.analyze_document(image_path)
    
    if result["success"]:
        click.echo("=== 文档分析 ===")
        click.echo(f"是否包含表格: {'是' if result['has_table'] else '否'}")
        click.echo("--- 识别文本 ---")
        click.echo(result["ocr_text"])
        click.echo("--- 分析结果 ---")
        click.echo(result["analysis"])
    else:
        click.echo(f"错误: {result['error']}", err=True)

if __name__ == "__main__":
    cli()

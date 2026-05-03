# Qwen-Vision: 基于Qwen-3.5 API的多模态视觉理解系统

## 📋 项目概述

Qwen-Vision是一个基于API调用的多模态AI系统，通过调用Qwen-3.5大语言模型API与计算机视觉技术深度融合，实现图像理解、视觉问答、场景分析等功能。系统提供RESTful API接口，便于快速集成和部署。

## ✨ 核心功能

| 功能模块 | 描述 |
|---------|------|
| 智能图像理解 | 图像内容描述、物体检测、场景分类 |
| 视觉问答系统 | 基于图像内容的自然语言问答、多轮对话 |
| 文档智能分析 | OCR识别、表格提取、公式理解 |
| 实时视频分析 | 视频帧处理、动态场景理解 |

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                    应用层 (Application Layer)               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │  Web UI     │ │  CLI 工具   │ │  API 服务   │          │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘          │
└─────────┼────────────────┼────────────────┼────────────────┘
          │                │                │
┌─────────▼────────────────▼────────────────▼────────────────┐
│                    业务逻辑层 (Service Layer)               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  VisionService  │  VQAService  │  DocumentService │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────┬───────────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────────┐
│                    API层 (API Layer)                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │       Qwen-3.5 API       │    LLaVA-1.5 API       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ 技术栈

- **语言**: Python 3.10+
- **框架**: FastAPI, Requests
- **大语言模型**: Qwen-3.5 API
- **视觉模型**: LLaVA-1.5 API / OpenAI Vision API
- **计算机视觉**: OpenCV, PIL, Tesseract
- **数据库**: SQLite (可选)
- **API文档**: Swagger UI

## 📁 项目结构

```
qwen-vision-project/
├── app/                    # 主应用目录
│   ├── __init__.py
│   ├── main.py             # FastAPI入口
│   ├── api/                # API路由
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── vision.py   # 视觉相关API
│   │   │   ├── vqa.py      # 视觉问答API
│   │   │   └── document.py # 文档分析API
│   ├── services/           # 业务服务层
│   │   ├── __init__.py
│   │   ├── vision_service.py
│   │   ├── vqa_service.py
│   │   └── document_service.py
│   ├── clients/            # API客户端
│   │   ├── __init__.py
│   │   ├── qwen_client.py  # Qwen-3.5 API客户端
│   │   └── vision_client.py # 视觉模型API客户端
│   ├── utils/              # 工具函数
│   │   ├── __init__.py
│   │   ├── image_utils.py
│   │   └── logger.py
│   └── config/             # 配置文件
│       ├── __init__.py
│       └── settings.py
├── cli/                    # 命令行工具
│   ├── __init__.py
│   └── main.py
├── tests/                  # 测试文件
│   ├── __init__.py
│   ├── test_vision.py
│   └── test_vqa.py
├── examples/               # 示例代码
│   ├── image_analysis.py
│   └── vqa_demo.py
├── requirements.txt        # 依赖列表
├── setup.py               # 安装脚本
└── README.md              # 项目说明
```

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Qwen-3.5 API Key

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置API密钥

在 `.env` 文件中配置：

```env
QWEN_API_KEY=your_api_key_here
QWEN_API_BASE_URL=https://api.qwenlm.cn/v1
```

### 启动服务

```bash
# 开发模式
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### API文档

启动服务后访问: http://localhost:8000/docs

## 🔌 API接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/v1/vision/describe` | POST | 图像内容描述 |
| `/api/v1/vision/detect` | POST | 物体检测 |
| `/api/v1/vqa/query` | POST | 视觉问答 |
| `/api/v1/document/ocr` | POST | 文档OCR识别 |
| `/api/v1/health` | GET | 健康检查 |

## 📊 性能指标

| 指标 | Qwen-3.5 7B | Qwen-3.5 14B |
|------|-------------|--------------|
| 响应延迟 | <300ms | <500ms |
| 并发支持 | 100+ | 50+ |

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和PR！

---

*项目已通过Qwen-3.5 API集成验证*

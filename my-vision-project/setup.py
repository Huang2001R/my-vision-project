from setuptools import setup, find_packages

setup(
    name="qwen-vision",
    version="1.0.0",
    description="基于Qwen-3.5 API的多模态视觉理解系统",
    author="Qwen-Vision Team",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "python-multipart==0.0.6",
        "requests==2.31.0",
        "opencv-python==4.8.1.78",
        "Pillow==10.1.0",
        "pytesseract==0.3.10",
        "python-dotenv==1.0.0",
        "loguru==0.7.2",
        "numpy==1.26.2",
        "pandas==2.1.4",
        "click==8.1.7"
    ],
    entry_points={
        "console_scripts": [
            "qwen-vision=cli.main:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)

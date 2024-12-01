# Virtual Environments Guide

## Overview
Virtual environments are essential for managing Python dependencies and ensuring consistent behavior across different projects using LMStudio.

## Environment Setup

### Basic Setup
```bash
# Create new virtual environment
python -m venv lmstudio-env

# Activate environment
# On Windows
lmstudio-env\Scripts\activate
# On macOS/Linux
source lmstudio-env/bin/activate

# Install basic requirements
pip install -r requirements.txt
```

### Advanced Setup
```bash
# Using conda
conda create -n lmstudio python=3.10
conda activate lmstudio

# Install GPU support
conda install -c conda-forge cudatoolkit=11.8
conda install -c conda-forge cudnn=8.4.1
```

## Package Management

### Basic Requirements
```txt
# requirements.txt
openai==0.28.0
requests==2.31.0
python-dotenv==1.0.0
tenacity==8.2.3
```

### Development Requirements
```txt
# requirements-dev.txt
-r requirements.txt
pytest==7.4.0
black==23.7.0
flake8==6.1.0
mypy==1.5.1
```

### Installation Scripts
```python
# install.py
import subprocess
import sys

def install_requirements():
    subprocess.check_call([
        sys.executable, 
        "-m", 
        "pip", 
        "install", 
        "-r", 
        "requirements.txt"
    ])

def install_dev_requirements():
    subprocess.check_call([
        sys.executable, 
        "-m", 
        "pip", 
        "install", 
        "-r", 
        "requirements-dev.txt"
    ])

if __name__ == "__main__":
    install_requirements()
```

## Environment Management

### Project Structure
```
project/
├── .env
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── setup.py
├── venv/
└── src/
    └── __init__.py
```

### Environment Variables
```bash
# .env
LMSTUDIO_API_BASE=http://localhost:1234/v1
LMSTUDIO_MODEL_PATH=/path/to/models
PYTHONPATH=${PYTHONPATH}:${PWD}/src
```

### Loading Environment
```python
# config.py
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    API_BASE = os.getenv("LMSTUDIO_API_BASE")
    MODEL_PATH = os.getenv("LMSTUDIO_MODEL_PATH")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
```

## Dependency Management

### Package Version Control
```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="lmstudio-project",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=0.28.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.7.0",
            "flake8>=6.1.0"
        ]
    }
)
```

### Version Locking
```bash
# Generate requirements.txt
pip freeze > requirements.txt

# Install specific versions
pip install -r requirements.txt
```

## Integration with LMStudio

### API Client Setup
```python
# client.py
import os
import openai
from dotenv import load_dotenv

load_dotenv()

class LMStudioClient:
    def __init__(self):
        openai.api_key = "not-needed"
        openai.api_base = os.getenv("LMSTUDIO_API_BASE")
    
    def chat_completion(self, messages):
        return openai.ChatCompletion.create(
            model="any-model-name",
            messages=messages
        )
```

### Model Management
```python
# models.py
import os
from pathlib import Path

class ModelManager:
    def __init__(self):
        self.model_path = Path(os.getenv("LMSTUDIO_MODEL_PATH"))
    
    def get_model_path(self, model_name):
        return self.model_path / f"{model_name}.gguf"
    
    def list_models(self):
        return [p.stem for p in self.model_path.glob("*.gguf")]
```

## Development Tools

### Testing Setup
```python
# conftest.py
import pytest
from dotenv import load_dotenv

@pytest.fixture(autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture
def lmstudio_client():
    from client import LMStudioClient
    return LMStudioClient()
```

### Code Quality Tools
```python
# setup.cfg
[flake8]
max-line-length = 88
extend-ignore = E203

[mypy]
python_version = 3.10
warn_return_any = True
warn_unused_configs = True

[tool:pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
```

## Best Practices

### Environment Management
1. **Isolation**
   - One environment per project
   - Clear dependency documentation
   - Version control for requirements

2. **Maintenance**
   - Regular updates
   - Dependency audits
   - Clean unused packages

### Development Workflow
1. **Setup**
   - Create new environment
   - Install dependencies
   - Configure tools

2. **Maintenance**
   - Update dependencies
   - Run tests
   - Check code quality

## Troubleshooting

### Common Issues
1. **Dependency Conflicts**
   - Check versions
   - Update requirements
   - Clean install

2. **Environment Problems**
   - Verify activation
   - Check paths
   - Rebuild if needed

### Solutions
1. **Clean Environment**
   ```bash
   deactivate
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Update Dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

## Next Steps
1. Set up virtual environment
2. Install dependencies
3. Configure development tools
4. Test integration
5. Document setup process

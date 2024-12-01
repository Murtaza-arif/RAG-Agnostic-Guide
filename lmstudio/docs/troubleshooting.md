# Troubleshooting Guide

## Common Issues and Solutions

### Installation Problems

#### Application Won't Start
1. **Symptoms**
   - Application crashes on launch
   - Blank screen
   - Error messages

2. **Solutions**
   - Verify system requirements
   - Run as administrator
   - Clear temporary files
   - Reinstall application

#### GPU Not Detected
1. **Symptoms**
   - CPU-only operation
   - Slow performance
   - GPU-related errors

2. **Solutions**
   ```bash
   # Check CUDA installation
   nvidia-smi
   
   # Verify GPU drivers
   nvidia-smi -L
   
   # Update CUDA toolkit
   conda install -c conda-forge cudatoolkit
   ```

### Model Management

#### Download Issues
1. **Symptoms**
   - Failed downloads
   - Incomplete files
   - Verification errors

2. **Solutions**
   ```python
   # Verify model file
   import hashlib
   
   def verify_model(file_path, expected_hash):
       with open(file_path, 'rb') as f:
           file_hash = hashlib.sha256(f.read()).hexdigest()
       return file_hash == expected_hash
   ```

#### Loading Problems
1. **Symptoms**
   - Model load failures
   - Memory errors
   - Initialization issues

2. **Solutions**
   ```python
   # Memory management
   import gc
   import torch
   
   def clean_memory():
       gc.collect()
       torch.cuda.empty_cache()
   ```

### API Server Issues

#### Connection Problems
1. **Symptoms**
   - Server won't start
   - Connection timeouts
   - API errors

2. **Solutions**
   ```python
   # Test server connection
   import requests
   
   def test_server():
       try:
           response = requests.get("http://localhost:1234/v1/models")
           return response.status_code == 200
       except:
           return False
   ```

#### Performance Issues
1. **Symptoms**
   - Slow responses
   - High latency
   - Timeouts

2. **Solutions**
   ```python
   # Monitor response times
   import time
   
   class PerformanceMonitor:
       def __init__(self):
           self.times = []
       
       def record_time(self, duration):
           self.times.append(duration)
           if len(self.times) > 100:
               self.times.pop(0)
       
       def get_average(self):
           return sum(self.times) / len(self.times)
   ```

## Resource Management

### Memory Issues

#### RAM Management
```python
import psutil

def check_memory():
    memory = psutil.virtual_memory()
    return {
        "total": memory.total,
        "available": memory.available,
        "percent": memory.percent,
        "used": memory.used,
        "free": memory.free
    }

def memory_warning():
    memory = check_memory()
    if memory["percent"] > 90:
        return "Warning: High memory usage"
    return "Memory usage normal"
```

#### GPU Memory
```python
import torch

def check_gpu_memory():
    if torch.cuda.is_available():
        return {
            "allocated": torch.cuda.memory_allocated(),
            "cached": torch.cuda.memory_reserved(),
            "max_allocated": torch.cuda.max_memory_allocated()
        }
    return None
```

### Performance Optimization

#### CPU Usage
```python
def optimize_threads():
    cpu_count = psutil.cpu_count()
    return max(1, cpu_count - 1)  # Leave one core free

def monitor_cpu():
    return psutil.cpu_percent(interval=1, percpu=True)
```

#### GPU Usage
```python
def optimize_gpu_layers(total_layers):
    if not torch.cuda.is_available():
        return 0
    
    vram = torch.cuda.get_device_properties(0).total_memory
    return min(total_layers, int(vram / (1024 * 1024 * 1024)))  # VRAM in GB
```

## Error Handling

### Logging Setup
```python
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('lmstudio.log'),
            logging.StreamHandler()
        ]
    )

def log_error(error, context=None):
    logger = logging.getLogger('lmstudio')
    if context:
        logger.error(f"Error in {context}: {str(error)}")
    else:
        logger.error(str(error))
```

### Error Recovery
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def robust_api_call(func):
    try:
        return func()
    except Exception as e:
        log_error(e, context=func.__name__)
        raise
```

## Diagnostics

### System Check
```python
def system_diagnostics():
    return {
        "cpu": {
            "usage": psutil.cpu_percent(),
            "cores": psutil.cpu_count(),
            "frequency": psutil.cpu_freq()
        },
        "memory": check_memory(),
        "gpu": check_gpu_memory(),
        "disk": {
            "usage": psutil.disk_usage('/'),
            "io": psutil.disk_io_counters()
        }
    }
```

### Network Diagnostics
```python
def check_network():
    try:
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        return {
            "status": "online" if response.status_code == 200 else "error",
            "latency": response.elapsed.total_seconds(),
            "status_code": response.status_code
        }
    except:
        return {"status": "offline"}
```

## Best Practices

### Preventive Measures
1. **Regular Maintenance**
   - Clean cache regularly
   - Update dependencies
   - Monitor resource usage

2. **Backup Strategy**
   - Save configurations
   - Backup model files
   - Document settings

### Recovery Procedures
1. **Emergency Shutdown**
   - Save state
   - Close connections
   - Clean resources

2. **Restart Protocol**
   - Check requirements
   - Verify resources
   - Test functionality

## Next Steps
1. Implement logging
2. Set up monitoring
3. Create backup plan
4. Document procedures
5. Test recovery steps

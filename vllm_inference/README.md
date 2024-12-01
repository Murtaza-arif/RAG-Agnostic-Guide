# vLLM Batch Inference Example

This example demonstrates how to use vLLM for efficient batch inference with large language models.

## Setup

### Option 1: Using Conda (Recommended)
1. Create and activate the conda environment:
```bash
conda env create -f environment.yml
conda activate vllm-env
```

### Option 2: Using pip
1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you have enough GPU memory to load the model. The default example uses Llama-2-7b-chat-hf.

## Usage

Run the batch inference script:
```bash
python batch_inference.py
```

## Features

- Efficient batch processing of multiple prompts
- Configurable sampling parameters (temperature, top_p, max_tokens)
- Performance timing for batch inference
- Easy-to-modify prompt list
- Structured output display

## Customization

You can modify the following in `batch_inference.py`:
- Change the model by updating the `model_name` in `initialize_model()`
- Modify sampling parameters in `run_batch_inference()`
- Add or modify prompts in `prepare_prompts()`

## Performance Notes

vLLM uses PagedAttention for efficient memory management and continuous batching for optimal throughput. The batch inference implementation automatically handles memory management and scheduling.

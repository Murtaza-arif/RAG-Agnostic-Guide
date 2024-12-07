# RAG Metrics Evaluator

## Overview
A comprehensive utility for evaluating Retrieval-Augmented Generation (RAG) systems using RAGAS metrics.

## Features
- Evaluate multiple RAG performance metrics
- Generate visualizations and reports
- Supports various evaluation metrics

## Supported Metrics
1. Context Precision
2. Context Recall
3. Context Entities Recall
4. Noise Sensitivity
5. Response Relevancy
6. Faithfulness

## Prerequisites
- Python 3.8+
- OpenAI API Key

## Installation

### Conda Environment Setup

1. **Create Conda Environment**
```bash
# Using the provided setup script
chmod +x setup.sh
./setup.sh

# Or manually
conda env create -f environment.yml
conda activate rag-metrics-eval
```

2. **Manual Installation**
```bash
# If you prefer pip
pip install -r requirements.txt
```

### Environment Management

- Activate environment: `conda activate rag-metrics-eval`
- Deactivate environment: `conda deactivate`
- Update environment: `conda env update -f environment.yml`
- Export current environment: `conda env export > environment.yml`

## Environment Setup
Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage
```python
from rag_metrics_evaluator import RAGMetricsEvaluator

# Initialize evaluator
evaluator = RAGMetricsEvaluator()

# Prepare your RAG system data
questions = [...]
contexts = [...]
ground_truth = [...]
answers = [...]

# Create dataset
dataset = evaluator.prepare_dataset(questions, contexts, ground_truth, answers)

# Evaluate metrics
metrics_results = evaluator.evaluate_rag_metrics(dataset)

# Generate reports and visualizations
evaluator.visualize_metrics(metrics_results)
evaluator.generate_report(metrics_results)
```

## Output
- JSON report of metrics
- Markdown report with interpretations
- Bar plot and interactive HTML visualization

## Customization
- Choose specific metrics to evaluate
- Modify visualization styles
- Extend reporting capabilities

## Contributing
Contributions are welcome! Please submit pull requests or open issues.

# Deepeval RAG Evaluation Demo

This demo shows how to evaluate RAG (Retrieval-Augmented Generation) systems using the Deepeval library.

## Setup

1. Create and activate the conda environment:
```bash
conda env create -f environment.yml
conda activate deepeval-demo
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key'
```

## Running the Demo

Run the evaluation script:
```bash
python rag_evaluation.py
```

## Metrics Used

The demo implements several key metrics for RAG evaluation:

1. **Answer Relevancy**: Measures how relevant the generated answer is to the input question
2. **Contextual Relevancy**: Evaluates if the retrieved context is relevant to the question
3. **Faithfulness**: Checks if the generated answer is faithful to the provided context
4. **Contextual Precision/Recall**: Measures the precision and recall of the context retrieval

## Sample Output

The script will output evaluation results for each metric, showing:
- Whether the metric passed or failed
- The score achieved for each metric

## Customization

You can modify the test cases in `rag_evaluation.py` to evaluate your own questions, contexts, and responses.

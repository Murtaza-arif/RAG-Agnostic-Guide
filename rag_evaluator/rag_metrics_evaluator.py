import os
import json
import asyncio
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    context_precision,
    context_recall,
    answer_relevancy
)
from datasets import Dataset
from langchain_openai import ChatOpenAI
import numpy as np
class RAGMetricsEvaluator:
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 model: str = 'gpt-3.5-turbo'):
        """
        Initialize RAG Metrics Evaluator
        
        Args:
            api_key: Optional API key for evaluation model
            model: Evaluation model (default: 'gpt-3.5-turbo')
        """
        load_dotenv()
        
        # Set up API key
        if not api_key:
            api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise ValueError("No API key provided. Set OPENAI_API_KEY in .env")
        
        os.environ['OPENAI_API_KEY'] = api_key
        
        # Configure LLM for RAGAS metrics
        self.llm = ChatOpenAI(
            model_name=model, 
            temperature=0.1,  # Low temperature for more deterministic responses
            max_tokens=1000
        )
        
        # Initialize metrics
        self.faithfulness = faithfulness
        self.context_precision = context_precision
        self.context_recall = context_recall
        self.answer_relevance = answer_relevancy
    
    async def evaluate_single_sample(self, 
                                     user_input: str, 
                                     response: str, 
                                     retrieved_contexts: List[str]) -> Dict[str, float]:
        """
        Evaluate a single RAG sample asynchronously
        
        Args:
            user_input: Original user query
            response: Generated response
            retrieved_contexts: Retrieved context documents
        
        Returns:
            Dictionary of metric scores
        """
        # Create a dataset in the format expected by Ragas
        data = {
            "question": [user_input],
            "answer": [response],
            "contexts": [retrieved_contexts],
            "ground_truths": [""],  # Required by Ragas but not used for these metrics
            "reference": [""]  # Required by context_precision metric
        }
        dataset = Dataset.from_dict(data)
        
        results = evaluate(
            dataset=dataset,
            metrics=[
                self.faithfulness,
                self.context_precision,
                self.context_recall,
                self.answer_relevance
            ],
            llm=self.llm
        )
        
        # Convert results to dictionary format
        return {
            'faithfulness': float(np.mean(results['faithfulness'])),
            'context_precision': float(np.mean(results['context_precision'])),
            'context_recall': float(np.mean(results['context_recall'])),
            'answer_relevance': float(np.mean(results['answer_relevancy']))
        }
    async def evaluate_rag_metrics(self, 
                                   questions: List[str], 
                                   answers: List[str], 
                                   contexts: List[List[str]]) -> List[Dict[str, float]]:
        """
        Evaluate multiple RAG samples
        
        Args:
            questions: List of user queries
            answers: List of generated answers
            contexts: List of retrieved contexts for each query
        
        Returns:
            List of metric scores for each sample
        """
        tasks = [
            self.evaluate_single_sample(q, a, c) 
            for q, a, c in zip(questions, answers, contexts)
        ]
        
        return await asyncio.gather(*tasks)
    
    def run_evaluation(self, 
                       questions: List[str], 
                       answers: List[str], 
                       contexts: List[List[str]]) -> Dict[str, float]:
        """
        Synchronous wrapper for async evaluation
        
        Args:
            questions: List of user queries
            answers: List of generated answers
            contexts: List of retrieved contexts for each query
        
        Returns:
            Aggregated metric scores
        """
        results = asyncio.run(self.evaluate_rag_metrics(questions, answers, contexts))
        
        # Aggregate results
        aggregated_metrics = {}
        for metric in ['faithfulness', 'context_precision', 'context_recall', 'answer_relevance']:
            values = [result[metric] for result in results]  # Each value is already a float from evaluate_single_sample
            aggregated_metrics[metric] = sum(values) / len(values)
        
        return aggregated_metrics
    
    def visualize_metrics(self, metrics_results: Dict[str, float], output_dir: str = 'metrics_reports'):
        """
        Create visualizations of RAG evaluation metrics
        
        Args:
            metrics_results: Dictionary of metric scores
            output_dir: Directory to save visualization reports
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Bar Plot
        plt.figure(figsize=(12, 6))
        plt.bar(metrics_results.keys(), metrics_results.values())
        plt.title('RAG System Metrics Performance', fontsize=15)
        plt.xlabel('Metrics', fontsize=12)
        plt.ylabel('Score', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'metrics_bar_plot.png'))
        plt.close()
        
        # Interactive Plotly Plot
        df = pd.DataFrame.from_dict(metrics_results, orient='index', columns=['Score'])
        df.index.name = 'Metrics'
        df.reset_index(inplace=True)
        
        fig = px.bar(df, x='Metrics', y='Score', 
                     title='RAG System Metrics Performance',
                     labels={'Score': 'Metric Score'},
                     color='Score',
                     color_continuous_scale='viridis')
        fig.update_layout(
            xaxis_title='Metrics',
            yaxis_title='Score',
            height=500,
            width=800
        )
        fig.write_html(os.path.join(output_dir, 'metrics_interactive_plot.html'))
    
    def generate_report(self, 
                        metrics_results: Dict[str, float], 
                        output_dir: str = 'metrics_reports'):
        """
        Generate comprehensive metrics report
        
        Args:
            metrics_results: Dictionary of metric scores
            output_dir: Directory to save report
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # JSON Report
        with open(os.path.join(output_dir, 'metrics_report.json'), 'w') as f:
            json.dump(metrics_results, f, indent=4)
        
        # Markdown Report
        markdown_content = "# RAG System Metrics Evaluation\n\n"
        markdown_content += "## Metrics Scores\n\n"
        for metric, score in metrics_results.items():
            markdown_content += f"- **{metric}**: {score:.4f}\n"
        
        markdown_content += "\n## Metric Interpretations\n"
        metric_descriptions = {
            "faithfulness": "Determines if the answer is grounded in the provided context.",
            "context_precision": "Measures how relevant the retrieved context is to the question.",
            "context_recall": "Assesses the comprehensiveness of the retrieved context.",
            "answer_relevance": "Checks how well the answer addresses the original question."
        }
        
        for metric, description in metric_descriptions.items():
            if metric in metrics_results:
                markdown_content += f"### {metric.replace('_', ' ').title()}\n"
                markdown_content += f"- **Score**: {metrics_results[metric]:.4f}\n"
                markdown_content += f"- **Description**: {description}\n\n"
        
        markdown_content += "## Scoring Guidelines\n"
        markdown_content += "- Scores range from 0 to 1\n"
        markdown_content += "- Higher scores indicate better performance\n"
        
        with open(os.path.join(output_dir, 'metrics_report.md'), 'w') as f:
            f.write(markdown_content)

def main():
    # Example usage
    evaluator = RAGMetricsEvaluator()
    
    # Sample data (replace with your actual RAG system outputs)
    questions = [
        "When was the first Super Bowl?",
        "How do vector databases work?"
    ]
    answers = [
        "The first Super Bowl was held on Jan 15, 1967",
        "Vector databases use embeddings to quickly find similar data points."
    ]
    contexts = [
        ["The First AFL–NFL World Championship Game was an American football game played on January 15, 1967, at the Los Angeles Memorial Coliseum in Los Angeles."],
        ["Vector databases store high-dimensional embeddings", "Similarity search is key in vector databases"]
    ]
    
    # Evaluate metrics
    metrics_results = evaluator.run_evaluation(questions, answers, contexts)
    
    # Generate visualizations and reports
    evaluator.visualize_metrics(metrics_results)
    evaluator.generate_report(metrics_results)
    
    # Print results
    for metric, score in metrics_results.items():
        print(f"{metric}: {score}")

if __name__ == "__main__":
    main()
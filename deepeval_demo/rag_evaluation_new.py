from deepeval import evaluate
from deepeval.metrics import (
    FaithfulnessMetric,
    AnswerRelevancyMetric,
    ContextualRelevancyMetric,
    ContextualPrecisionMetric
)
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Example 1: Basic RAG evaluation
question1 = "What is the capital of France?"
context1 = ["France is a country in Western Europe. Paris is the capital and largest city of France. Located on the Seine River, Paris is known for its iconic landmarks like the Eiffel Tower and the Louvre Museum."]
actual_output1 = "The capital of France is Paris."

# Example 2: Product refund policy
question2 = "What if these shoes don't fit?"
context2 = ["All customers are eligible for a 30 day full refund at no extra cost."]
actual_output2 = "We offer a 30-day full refund at no extra cost."

# Create test cases
test_case1 = LLMTestCase(
    input=question1,
    actual_output=actual_output1,
    retrieval_context=context1
)

test_case2 = LLMTestCase(
    input=question2,
    actual_output=actual_output2,
    retrieval_context=context2
)

# Initialize metrics with GPT-4
metrics = [
    FaithfulnessMetric(threshold=0.7, model="gpt-4", include_reason=True),
    AnswerRelevancyMetric(threshold=0.7, model="gpt-4", include_reason=True),
    ContextualRelevancyMetric(threshold=0.7, model="gpt-4", include_reason=True),
    ContextualPrecisionMetric(threshold=0.7, model="gpt-4", include_reason=True)
]

def evaluate_single_case(test_case, metrics):
    print(f"\nEvaluating test case: {test_case.input}")
    print("-" * 50)
    for metric in metrics:
        metric.measure(test_case)
        print(f"\n{metric.__class__.__name__}:")
        print(f"Score: {metric.score}")
        print(f"Passed: {metric.score >= metric.threshold}")
        if hasattr(metric, 'reason'):
            print(f"Reason: {metric.reason}")
        print("-" * 30)

# Evaluate individual test cases
print("\nIndividual Evaluation Results:")
evaluate_single_case(test_case1, metrics)
evaluate_single_case(test_case2, metrics)

# Bulk evaluation
print("\nBulk Evaluation Results:")
print("-" * 50)
results = evaluate(
    test_cases=[test_case1, test_case2],
    metrics=metrics
)

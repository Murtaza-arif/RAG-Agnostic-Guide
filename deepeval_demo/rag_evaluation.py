from deepeval.metrics import (
    AnswerRelevancyMetric,
    ContextualRelevancyMetric,
    FaithfulnessMetric,
    ContextualPrecisionMetric,
)
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv

# Sample test case data
question = "What is the capital of France?"
context = """France is a country in Western Europe. Paris is the capital and largest city of France. 
Located on the Seine River, Paris is known for its iconic landmarks like the Eiffel Tower and the Louvre Museum."""
actual_output = "The capital of France is Paris."
expected_output = "Paris is the capital of France."
load_dotenv()

# Create a test case
test_case = LLMTestCase(
    input=question,
    actual_output=actual_output,
    expected_output=expected_output,
    retrieval_context=[context]
)

# Initialize metrics
metrics = [
    AnswerRelevancyMetric(threshold=0.5, model="gpt-4", include_reason=True),
    ContextualRelevancyMetric(threshold=0.5, model="gpt-4", include_reason=True),
    FaithfulnessMetric(threshold=0.5, model="gpt-4", include_reason=True),
    ContextualPrecisionMetric(threshold=0.5, model="gpt-4", include_reason=True)
]

# Run evaluation
print("\nEvaluation Results:")
print("------------------")
for metric in metrics:
    score = metric.measure(test_case)
    # print(f"{metric.__class__.__name__}: {'Passed' if score >= metric.threshold else 'Failed'}")
    print(f"Score: {metric.score}")
    print(f"Score: {metric.reason}")
    print("------------------")

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time

def initialize_model(model_name="facebook/opt-125m"):
    """Initialize the model and tokenizer."""
    print("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # Move model to MPS (Metal Performance Shaders) if available, else CPU
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model = model.to(device)
    
    return model, tokenizer, device

def prepare_prompts():
    """Prepare a batch of prompts for inference."""
    return [
        "Explain what is machine learning in one sentence.",
        "What is the capital of France?",
        "Write a simple Python function to add two numbers.",
        "Explain what is deep learning in one sentence.",
        "What is the meaning of RAG in AI context?"
    ]

def run_batch_inference(model, tokenizer, prompts, device, max_tokens=128):
    """Run batch inference on the given prompts."""
    print(f"Running batch inference on {len(prompts)} prompts...")
    start_time = time.time()
    
    # Tokenize all prompts
    inputs = tokenizer(prompts, padding=True, truncation=True, return_tensors="pt").to(device)
    
    # Generate responses
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_tokens,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.95,
            pad_token_id=tokenizer.pad_token_id
        )
    
    # Decode outputs
    responses = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    
    end_time = time.time()
    print(f"Batch inference completed in {end_time - start_time:.2f} seconds")
    
    return responses

def display_results(prompts, responses):
    """Display the results of batch inference."""
    print("\nResults:")
    print("-" * 50)
    for prompt, response in zip(prompts, responses):
        print(f"\nPrompt: {prompt}")
        print(f"Response: {response}")
        print("-" * 50)

def main():
    # Initialize model
    model, tokenizer, device = initialize_model()
    print(f"Using device: {device}")
    
    # Prepare prompts
    prompts = prepare_prompts()
    
    # Run inference
    responses = run_batch_inference(model, tokenizer, prompts, device)
    
    # Display results
    display_results(prompts, responses)

if __name__ == "__main__":
    main()

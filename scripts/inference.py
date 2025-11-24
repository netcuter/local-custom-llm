#!/usr/bin/env python3
"""
Test the fine-tuned pentesting model
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_model(model_path: str):
    """Load fine-tuned model"""
    logger.info(f"Loading model from {model_path}")

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

    # Load base model with LoRA weights
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=torch.float16,
    )

    logger.info("Model loaded successfully")
    return model, tokenizer


def generate_response(model, tokenizer, prompt: str, max_length: int = 1024):
    """Generate response for a given prompt"""

    # Format prompt
    formatted_prompt = f"""<|user|>
{prompt}
<|assistant|>
"""

    # Tokenize
    inputs = tokenizer(formatted_prompt, return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    # Generate
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_length,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    # Decode
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract assistant response
    if "<|assistant|>" in response:
        response = response.split("<|assistant|>")[-1].strip()

    return response


def interactive_mode(model, tokenizer):
    """Interactive chat mode"""
    print("\n" + "="*70)
    print("Pentesting Model - Interactive Mode")
    print("="*70)
    print("Type your questions. Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            prompt = input("\n🎯 You: ").strip()

            if prompt.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break

            if not prompt:
                continue

            print("\n🤖 Assistant: ", end="", flush=True)
            response = generate_response(model, tokenizer, prompt)
            print(response)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


def test_examples(model, tokenizer):
    """Run predefined test examples"""
    examples = [
        "Explain SQL injection attacks and how to prevent them.",
        "What is Cross-Site Scripting (XSS) and how does it work?",
        "How do you exploit a remote code execution vulnerability?",
        "Explain the OWASP Top 10 vulnerabilities.",
        "What tools are commonly used for web application penetration testing?",
    ]

    print("\n" + "="*70)
    print("Testing with example prompts")
    print("="*70)

    for i, prompt in enumerate(examples, 1):
        print(f"\n[Example {i}/{len(examples)}]")
        print(f"Prompt: {prompt}")
        print(f"\nResponse:")
        print("-" * 70)

        response = generate_response(model, tokenizer, prompt, max_length=512)
        print(response)
        print("-" * 70)


def main():
    parser = argparse.ArgumentParser(description="Test pentesting model")
    parser.add_argument(
        "--model_path",
        type=str,
        default="models/granite-pentesting",
        help="Path to fine-tuned model"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["interactive", "test", "both"],
        default="interactive",
        help="Mode: interactive chat or test examples"
    )

    args = parser.parse_args()

    # Load model
    model, tokenizer = load_model(args.model_path)

    # Run selected mode
    if args.mode == "test":
        test_examples(model, tokenizer)
    elif args.mode == "interactive":
        interactive_mode(model, tokenizer)
    else:  # both
        test_examples(model, tokenizer)
        interactive_mode(model, tokenizer)


if __name__ == '__main__':
    main()

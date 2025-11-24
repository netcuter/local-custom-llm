#!/usr/bin/env python3
"""
Export trained model to GGUF format (Q4_K_M)
Requires: llama.cpp compiled with quantize tool
"""

import subprocess
import shutil
from pathlib import Path
import sys
import argparse

def check_llama_cpp():
    """Check if llama.cpp tools are available"""
    # Check for convert.py (new llama.cpp)
    convert_py = Path('llama.cpp/convert-hf-to-gguf.py')
    quantize = Path('llama.cpp/quantize') or shutil.which('quantize')

    if not convert_py.exists() and not shutil.which('convert-hf-to-gguf.py'):
        print("❌ llama.cpp not found")
        print("\nInstall llama.cpp:")
        print("  git clone https://github.com/ggerganov/llama.cpp")
        print("  cd llama.cpp && make")
        return False

    return True


def merge_lora_adapter(model_path: str, output_path: str):
    """Merge LoRA adapter with base model"""
    print(f"\n🔀 Merging LoRA adapter...")
    print(f"  Input: {model_path}")
    print(f"  Output: {output_path}")

    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import PeftModel

        # Load base model
        print("  Loading base model...")
        base_model_name = "ibm-granite/granite-3.0-2b-instruct"
        model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            trust_remote_code=True,
            torch_dtype="auto"
        )

        # Load LoRA adapter
        print("  Loading LoRA adapter...")
        model = PeftModel.from_pretrained(model, model_path)

        # Merge
        print("  Merging...")
        model = model.merge_and_unload()

        # Save merged model
        print(f"  Saving to {output_path}...")
        model.save_pretrained(output_path)

        # Save tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        tokenizer.save_pretrained(output_path)

        print("  ✅ Merge complete")
        return True

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def convert_to_gguf(input_path: str, output_path: str):
    """Convert to GGUF f16"""
    print(f"\n📦 Converting to GGUF...")
    print(f"  Input: {input_path}")
    print(f"  Output: {output_path}")

    try:
        # Try new convert script
        cmd = [
            'python3', 'llama.cpp/convert-hf-to-gguf.py',
            input_path,
            '--outfile', output_path,
            '--outtype', 'f16'
        ]

        subprocess.run(cmd, check=True)
        print("  ✅ Conversion complete")
        return True

    except subprocess.CalledProcessError as e:
        print(f"  ❌ Error: {e}")
        return False


def quantize_gguf(input_path: str, output_path: str, quant_type: str = "Q4_K_M"):
    """Quantize GGUF to Q4_K_M"""
    print(f"\n⚙️  Quantizing to {quant_type}...")
    print(f"  Input: {input_path}")
    print(f"  Output: {output_path}")

    try:
        cmd = [
            'llama.cpp/quantize',
            input_path,
            output_path,
            quant_type
        ]

        subprocess.run(cmd, check=True)
        print(f"  ✅ Quantization complete")
        return True

    except subprocess.CalledProcessError as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Export model to GGUF Q4_K_M")
    parser.add_argument(
        '--model_path',
        type=str,
        default='models/granite-pentesting',
        help='Path to trained model with LoRA adapter'
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        default='models/gguf',
        help='Output directory for GGUF files'
    )

    args = parser.parse_args()

    print("="*70)
    print("Export to GGUF Q4_K_M")
    print("="*70)

    # Create output dir
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Paths
    merged_path = output_dir / 'merged'
    gguf_f16_path = output_dir / 'model-f16.gguf'
    gguf_q4_path = output_dir / 'granite-pentesting-q4_k_m.gguf'

    # Step 1: Merge LoRA
    print("\n[Step 1/3] Merge LoRA adapter")
    if not merge_lora_adapter(args.model_path, str(merged_path)):
        print("\n❌ Failed to merge LoRA adapter")
        return 1

    # Step 2: Convert to GGUF F16
    print("\n[Step 2/3] Convert to GGUF F16")
    if not convert_to_gguf(str(merged_path), str(gguf_f16_path)):
        print("\n❌ Failed to convert to GGUF")
        return 1

    # Step 3: Quantize to Q4_K_M
    print("\n[Step 3/3] Quantize to Q4_K_M")
    if not quantize_gguf(str(gguf_f16_path), str(gguf_q4_path)):
        print("\n❌ Failed to quantize")
        return 1

    print("\n" + "="*70)
    print("✅ Export complete!")
    print("="*70)
    print(f"\n📁 Output file: {gguf_q4_path}")
    print(f"   Size: {gguf_q4_path.stat().st_size / (1024**3):.2f} GB")
    print("\nTest with llama.cpp:")
    print(f"  ./llama.cpp/main -m {gguf_q4_path} -p 'Explain SQL injection' -n 256")

    return 0


if __name__ == '__main__':
    sys.exit(main())

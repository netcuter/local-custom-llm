# Training Guide - Pentesting LLM

## Overview
This guide explains how to fine-tune a language model on pentesting data using LoRA/QLoRA.

## Dataset
- **Location**: `data/raw/final_dataset.jsonl`
- **Size**: 307 examples
- **Sources**:
  - 126 HTB writeups (xct.github.io)
  - 100 PayloadsAllTheThings files
  - 50 HTB writeups (0xdf.gitlab.io)
  - 20 HTB writeups (various)
  - 9 PortSwigger articles
  - 2 OWASP articles
- **Average length**: ~7797 characters per example

## Model Architecture
- **Base model**: IBM Granite 3.0 2B Instruct
- **Fine-tuning method**: LoRA (Low-Rank Adaptation)
- **Quantization**: 4-bit (QLoRA) for memory efficiency

## Training Configuration

### LoRA Settings
- **Rank (r)**: 16
- **Alpha**: 32
- **Dropout**: 0.05
- **Target modules**: q_proj, v_proj, k_proj, o_proj

### Training Hyperparameters
- **Epochs**: 3
- **Batch size**: 1 (per device)
- **Gradient accumulation**: 8 steps (effective batch size = 8)
- **Learning rate**: 2e-4
- **Max sequence length**: 2048 tokens
- **Warmup steps**: 100
- **Optimizer**: AdamW
- **Scheduler**: Cosine

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify Data
```bash
# Check dataset exists
ls -lh data/raw/final_dataset.jsonl

# Count examples
wc -l data/raw/final_dataset.jsonl
```

### 3. Start Training
```bash
# Full training
python scripts/train.py

# With custom settings (edit train.py Config class)
```

### 4. Monitor Training
```bash
# View logs in real-time
tail -f logs/training_summary.txt

# TensorBoard (if available)
tensorboard --logdir logs/
```

## Expected Training Time
- **CPU (8-12 cores)**: 8-12 hours
- **GPU (RTX 3090)**: 2-3 hours
- **GPU (A100)**: 1-2 hours

## Memory Requirements
- **With 4-bit quantization**: ~6-8 GB RAM
- **Without quantization**: ~16 GB RAM
- **GPU VRAM**: ~8 GB (if using GPU)

## Testing the Model

### Interactive Mode
```bash
python scripts/inference.py --mode interactive
```

### Test with Examples
```bash
python scripts/inference.py --mode test
```

### Both
```bash
python scripts/inference.py --mode both
```

## Output Files
After training, you'll find:
- **Model**: `models/granite-pentesting/`
  - `adapter_model.bin` - LoRA weights
  - `adapter_config.json` - LoRA config
  - `tokenizer files` - Tokenizer
- **Logs**: `logs/`
  - `training_summary.txt` - Training summary
  - TensorBoard logs

## Tips for Better Results

### 1. Increase Data Quality
- Add more recent CVE writeups
- Include PortSwigger lab solutions
- Add HackerOne disclosed reports

### 2. Adjust Hyperparameters
- **More epochs** (5-10): Better convergence
- **Larger LoRA rank** (32-64): More capacity
- **Lower learning rate** (1e-4): More stable

### 3. Use Better Base Model
- **Granite 8B**: Better performance, more memory
- **Mistral 7B**: Strong general capabilities
- **CodeLlama 13B**: Good for technical content

### 4. Advanced Techniques
- **DPO/RLHF**: Align with preferences
- **Continued pre-training**: More domain knowledge
- **Multi-task learning**: Train on related tasks

## Troubleshooting

### Out of Memory
- Reduce batch size to 1
- Increase gradient accumulation steps
- Enable gradient checkpointing
- Use smaller max_seq_length (1024)

### Poor Performance
- Train for more epochs
- Check data quality
- Increase LoRA rank
- Try different learning rate

### Slow Training
- Use GPU if available
- Reduce max_seq_length
- Use smaller model
- Enable mixed precision (fp16/bf16)

## Next Steps
1. Evaluate model on test set
2. Deploy as API service
3. Create web interface
4. Export to GGUF for llama.cpp
5. Share on HuggingFace Hub

## Resources
- [PEFT Documentation](https://huggingface.co/docs/peft)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [QLoRA Paper](https://arxiv.org/abs/2305.14314)
- [Granite Models](https://huggingface.co/ibm-granite)

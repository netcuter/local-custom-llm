# Model Information - Granite 4H Tiny

## Architecture

**Granite 4H Tiny** (IBM)
- **Type**: MoE (Mixture of Experts)
- **Total Parameters**: 7B
- **Active Parameters**: ~1B (during inference)
- **Format**: GGUF (for LM Studio)

## MoE Advantages

### Performance:
- Inference speed of 1B model
- Quality close to 7B model
- Memory efficient (only active params loaded)

### Fine-tuning:
- Can fine-tune with QLoRA/LoRA
- Lower memory requirements than full 7B
- CPU-friendly

## Fine-tuning Strategy

### Option 1: Fine-tune full model
- Treats all 7B params
- Higher memory usage
- Better results

### Option 2: Fine-tune LoRA adapters
- Only trains adapters
- Very low memory (4-6GB RAM)
- Slightly lower quality but practical

### Option 3: QLoRA (Recommended)
- 4-bit quantization + LoRA
- ~4-8GB RAM usage
- Best balance quality/resources

## Estimated Resources (QLoRA on CPU)

- **RAM**: 8-12GB
- **Training time**: 24-48h for 1000 examples
- **Disk**: ~4GB for model + 2GB for checkpoints

## Use Cases

### Desktop (7B MoE):
- Primary models (pentesting + survival)
- High quality responses
- Reasonable speed on CPU

### Mobile (1B distilled):
- Distill knowledge to Gemma 1B
- Fast inference on phone
- Quick reference tool

---

**Status**: Selected as base model
**Date**: 2025-11-23

# Model Information - DeepSeek DeepHat v1 7B

## Architecture

**DeepSeek DeepHat v1 7B**
- **Developer**: DeepSeek (mradermacher quantization)
- **Type**: Transformer-based LLM
- **Total Parameters**: 7B
- **Format**: GGUF (for LM Studio)
- **Specialization**: Coding, reasoning, security

## Why DeepSeek DeepHat for Pentesting?

### Advantages:
- **Coding focus**: Strong performance on code understanding
- **Security knowledge**: Good baseline for security concepts
- **7B size**: Better quality than 4B while still CPU-trainable
- **Active development**: Recent model (2024-2025)

### Performance:
- Inference: Medium speed on CPU
- Quality: High (7B parameter count)
- Memory efficient with quantization

## Fine-tuning Strategy

### QLoRA (Recommended for 7B on CPU)

**Memory Requirements:**
- **Model (4-bit)**: 4-5GB
- **Training overhead**: 6-8GB
- **System**: 2-3GB
- **Total**: ~12-16GB RAM ✅

**Training Time (CPU - i7 13gen 16 cores):**
- 500 examples: ~24-36h
- 1000 examples: ~48-72h
- 2000 examples: ~96-144h (4-6 days)

### Configuration:
```yaml
base_model: DeepSeek-DeepHat-v1-7B
quantization: 4-bit (bitsandbytes)
lora_r: 8
lora_alpha: 16
lora_dropout: 0.05
target_modules: [q_proj, k_proj, v_proj, o_proj]
batch_size: 1
gradient_accumulation_steps: 4
learning_rate: 2e-4
epochs: 3
```

## Target Use Case

### Web Pentesting Model:
- OWASP Top 10 2025 expertise
- Web vulnerability analysis
- Burp Suite / security tools knowledge
- CTF problem-solving
- Exploit development (ethical/authorized)
- Report writing
- Security best practices

## Comparison to Alternatives

| Model | Params | Active | Speed | Quality | Best For |
|-------|--------|--------|-------|---------|----------|
| **DeepSeek DeepHat 7B** | **7B** | **7B** | **Medium** | **High** | **Pentesting** ✅ |
| Granite 4H Tiny MoE | 7B | 1B | Fast | Good | General code |
| Gemma 2 4B | 4B | 4B | Fast | Good | Multilingual |
| Bielik 4.5B | 4.5B | 4.5B | Medium | Good (PL) | Polish content |

## Training Plan

**Phase 1: Data Collection** (Today)
- Web scraping: CTF writeups, OWASP docs, PortSwigger labs
- YouTube transcripts: IppSec, John Hammond, etc.
- User-provided links (priority)
- Target: 1,500-2,500 examples

**Phase 2: Fine-tuning** (Local PC - Tomorrow+)
- QLoRA fine-tuning
- CPU training (overnight/multi-day)
- Checkpointing every 100 steps

**Phase 3: Export** (After training)
- Merge LoRA adapters
- Quantize to various formats (Q4, Q5, Q8)
- Export to GGUF for LM Studio
- Test and evaluate

---

**Selected**: DeepSeek DeepHat v1 7B
**Purpose**: Web Pentesting Specialist
**Date**: 2025-11-23
**Status**: Ready for data collection

# Model Information - Granite 4H Tiny MoE

## Architecture

**Granite 4H Tiny** (IBM)
- **Type**: MoE (Mixture of Experts)
- **Total Parameters**: 7B
- **Active Parameters**: ~1B (during inference)
- **Format**: GGUF (for LM Studio)
- **Specialization**: Code, reasoning, security

## Why Granite 4H Tiny for Pentesting?

### Key Advantages:
- **⚡ SPEED**: MoE architecture - only 1B active = FAST inference
- **🧠 QUALITY**: 7B total parameters = good quality responses
- **💻 CODE FOCUS**: IBM's Granite = excellent for code/security
- **⚡ FAST TRAINING**: Smaller active params = faster fine-tuning
- **💾 EFFICIENT**: Lower memory requirements than full 7B

### Performance:
- **Inference**: VERY FAST (1B active)
- **Quality**: HIGH (7B total knowledge)
- **Training speed**: 2x faster than full 7B
- **Practical**: Perfect for daily pentesting work

## Fine-tuning Strategy

### QLoRA (Recommended for 7B on CPU)

**Memory Requirements (MoE advantage!):**
- **Model (4-bit)**: 3-4GB (MoE - tylko 1B aktywne!)
- **Training overhead**: 4-6GB (mniejsze niż full 7B)
- **System**: 2-3GB
- **Total**: ~9-13GB RAM ✅ (bezpiecznie < 16GB!)

**Training Time (CPU - i7 13gen 16 cores):**
- 500 examples: ~18-24h (MoE advantage!)
- 1000 examples: ~24-48h
- 2000 examples: ~48-96h (2-4 days)

### Configuration:
```yaml
base_model: Granite-4H-Tiny-7B-MoE
quantization: 4-bit (bitsandbytes)
lora_r: 16  # Higher for MoE
lora_alpha: 32
lora_dropout: 0.05
target_modules: [q_proj, k_proj, v_proj, o_proj, gate]  # MoE gate
batch_size: 1
gradient_accumulation_steps: 4
learning_rate: 3e-4  # Slightly higher for MoE
epochs: 3
```

## Target Use Case

### 100% WEB PENTESTING SPECIALIST

**Why pentesting-only:**
- User already has Qwen2.5-Coder 1.5B for programming
- Specialization = better quality
- Focused dataset = faster training

**Pentesting Expertise:**
- OWASP Top 10 2025 (including new categories)
- Web vulnerability analysis (XSS, SQLi, CSRF, etc.)
- Burp Suite / security tools knowledge
- CTF problem-solving & writeups
- Exploit development (ethical/authorized)
- Report writing & documentation
- Security best practices & methodology
- Penetration testing workflow

**Complementary Model:**
- **Qwen2.5-Coder 1.5B** → Programming, algorithms, clean code
- **Granite 4H Tiny MoE** → Web pentesting specialist

## Comparison to Alternatives

| Model | Params | Active | Speed | Quality | Best For |
|-------|--------|--------|-------|---------|----------|
| **DeepSeek DeepHat 7B** | **7B** | **7B** | **Medium** | **High** | **Pentesting** ✅ |
| Granite 4H Tiny MoE | 7B | 1B | Fast | Good | General code |
| Gemma 2 4B | 4B | 4B | Fast | Good | Multilingual |
| Bielik 4.5B | 4.5B | 4.5B | Medium | Good (PL) | Polish content |

## Training Plan

**Phase 1: Data Collection** (Today)
- **100% Pentesting Focus**:
  - OWASP Top 10 2025 official docs
  - PortSwigger Web Security Academy (all labs + solutions)
  - CTF writeups (HTB, TryHackMe, 0xdf)
  - YouTube: IppSec, John Hammond, LiveOverflow, PwnFunction
  - Security blogs & research
  - User-provided links (highest priority)
- Target: 1,500-2,000 focused examples
- Quality over quantity

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

**Selected**: Granite 4H Tiny MoE (7B total, 1B active)
**Purpose**: Web Pentesting Specialist
**Date**: 2025-11-23
**Status**: Ready for data collection

## Alternative Considered

**DeepSeek DeepHat 7B**: Better quality but significantly slower inference and training. Can be used later if Granite quality is insufficient.

**Decision rationale**: Speed > marginal quality improvement for practical pentesting use.

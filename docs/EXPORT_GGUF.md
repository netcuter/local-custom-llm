# Export to GGUF Q4_K_M

## Quick Start

### 1. Install llama.cpp
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make
cd ..
```

### 2. Train model (if not done)
```bash
python scripts/train.py
```

### 3. Export to GGUF Q4_K_M
```bash
python scripts/export_gguf.py
```

Output: `models/gguf/granite-pentesting-q4_k_m.gguf` (~1.5 GB)

### 4. Test with llama.cpp
```bash
./llama.cpp/main \
  -m models/gguf/granite-pentesting-q4_k_m.gguf \
  -p "Explain SQL injection attacks" \
  -n 256 \
  --temp 0.7
```

## What it does

1. **Merges** LoRA adapter with base model
2. **Converts** to GGUF F16 format
3. **Quantizes** to Q4_K_M (4-bit, balanced quality)

## Benefits of Q4_K_M

- **Small size**: ~1.5 GB (vs ~5 GB full model)
- **Fast inference**: CPU-friendly
- **Good quality**: Balanced quantization
- **Low RAM**: ~2-3 GB needed

## Usage with llama.cpp

### CLI
```bash
./llama.cpp/main -m model.gguf -p "prompt" -n 512
```

### Server mode
```bash
./llama.cpp/server -m model.gguf --port 8080
```

Then use API:
```bash
curl http://localhost:8080/completion \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain XSS", "n_predict": 256}'
```

## Alternative: Direct GGUF training

Skip PyTorch training, use llama.cpp directly (experimental):
```bash
# Convert base model to GGUF
# Fine-tune with llama.cpp (if supported)
# Or use Unsloth for direct GGUF fine-tuning
```

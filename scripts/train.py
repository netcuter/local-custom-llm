#!/usr/bin/env python3
"""
Fine-tune Granite model on pentesting data using LoRA/QLoRA
Optimized for CPU training with low memory footprint
"""

import json
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    TaskType
)
from datasets import Dataset
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths
DATA_DIR = Path('data/raw')
MODELS_DIR = Path('models')
OUTPUT_DIR = Path('models/granite-pentesting')
LOGS_DIR = Path('logs')

# Create directories
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class Config:
    """Training configuration"""

    # Model settings
    model_name: str = "ibm-granite/granite-3.0-2b-instruct"  # Smaller model for CPU
    use_4bit: bool = False  # DON'T use 4-bit during training (better quality for Q4_K_M export)

    # LoRA settings
    lora_r: int = 16  # LoRA rank
    lora_alpha: int = 32  # LoRA alpha (scaling)
    lora_dropout: float = 0.05
    lora_target_modules: List[str] = field(
        default_factory=lambda: ["q_proj", "v_proj", "k_proj", "o_proj"]
    )

    # Training settings
    num_epochs: int = 3
    batch_size: int = 1  # Small batch for CPU
    gradient_accumulation_steps: int = 8  # Effective batch size = 8
    learning_rate: float = 2e-4
    max_seq_length: int = 2048
    warmup_steps: int = 100
    logging_steps: int = 10
    save_steps: int = 500

    # Dataset
    data_file: str = str(DATA_DIR / 'final_dataset.jsonl')
    max_samples: Optional[int] = None  # None = use all data

    # Output
    output_dir: str = str(OUTPUT_DIR)

    # Precision (for best quality before Q4_K_M export)
    use_cpu: bool = False  # Auto-detect GPU/CPU
    fp16: bool = True  # Use FP16 for GPU (better quality than 4-bit)
    bf16: bool = False  # BF16 if your GPU supports it


def load_data(config: Config) -> Dataset:
    """Load and prepare dataset"""
    logger.info(f"Loading data from {config.data_file}")

    data = []
    with open(config.data_file, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            data.append(item)

    if config.max_samples:
        data = data[:config.max_samples]

    logger.info(f"Loaded {len(data)} examples")

    # Format data for instruction tuning
    formatted_data = []
    for item in data:
        # Create instruction-following format
        title = item.get('title', 'Pentesting Guide')
        content = item.get('content', '')
        source = item.get('source', 'unknown')

        # Format as instruction-response
        instruction = f"Explain the following pentesting technique or writeup: {title}"
        response = content[:config.max_seq_length]  # Truncate if needed

        # Combine in chat format
        text = f"""<|user|>
{instruction}
<|assistant|>
{response}
<|endoftext|>"""

        formatted_data.append({'text': text})

    # Convert to HuggingFace Dataset
    dataset = Dataset.from_list(formatted_data)
    logger.info(f"Created dataset with {len(dataset)} examples")

    return dataset


def create_model_and_tokenizer(config: Config):
    """Load model and tokenizer with quantization"""
    logger.info(f"Loading model: {config.model_name}")

    # Quantization config for QLoRA
    if config.use_4bit:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
        logger.info("Using 4-bit quantization (QLoRA)")
    else:
        bnb_config = None
        logger.info("Using standard precision")

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        config.model_name,
        trust_remote_code=True
    )

    # Set padding token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Load model
    model = AutoModelForCausalLM.from_pretrained(
        config.model_name,
        quantization_config=bnb_config if config.use_4bit else None,
        device_map="auto" if not config.use_cpu else None,
        trust_remote_code=True,
        torch_dtype=torch.float16 if config.use_4bit else torch.float32,
    )

    # Prepare for k-bit training
    if config.use_4bit:
        model = prepare_model_for_kbit_training(model)

    # Configure LoRA
    lora_config = LoraConfig(
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        target_modules=config.lora_target_modules,
        lora_dropout=config.lora_dropout,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )

    # Apply LoRA
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    logger.info("Model and tokenizer loaded successfully")
    return model, tokenizer


def tokenize_dataset(dataset: Dataset, tokenizer, config: Config) -> Dataset:
    """Tokenize dataset"""
    logger.info("Tokenizing dataset...")

    def tokenize_function(examples):
        return tokenizer(
            examples['text'],
            truncation=True,
            max_length=config.max_seq_length,
            padding='max_length',
            return_tensors=None
        )

    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=dataset.column_names,
        desc="Tokenizing"
    )

    logger.info("Tokenization complete")
    return tokenized_dataset


def train(config: Config):
    """Main training function"""
    logger.info("="*70)
    logger.info("Starting Pentesting Model Fine-tuning")
    logger.info("="*70)

    # Load data
    dataset = load_data(config)

    # Load model and tokenizer
    model, tokenizer = create_model_and_tokenizer(config)

    # Tokenize
    tokenized_dataset = tokenize_dataset(dataset, tokenizer, config)

    # Training arguments
    training_args = TrainingArguments(
        output_dir=config.output_dir,
        num_train_epochs=config.num_epochs,
        per_device_train_batch_size=config.batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        learning_rate=config.learning_rate,
        warmup_steps=config.warmup_steps,
        logging_steps=config.logging_steps,
        save_steps=config.save_steps,
        save_total_limit=3,
        fp16=config.fp16,
        bf16=config.bf16,
        logging_dir=str(LOGS_DIR),
        report_to=["tensorboard"],
        optim="adamw_torch",  # Standard optimizer for CPU
        gradient_checkpointing=True,  # Save memory
        max_grad_norm=0.3,
        lr_scheduler_type="cosine",
    )

    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False  # Causal LM, not masked LM
    )

    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator,
    )

    # Train
    logger.info("Starting training...")
    trainer.train()

    # Save final model
    logger.info("Saving final model...")
    trainer.save_model(config.output_dir)
    tokenizer.save_pretrained(config.output_dir)

    logger.info("="*70)
    logger.info(f"Training complete! Model saved to {config.output_dir}")
    logger.info("="*70)

    # Save training summary
    summary_file = LOGS_DIR / 'training_summary.txt'
    with open(summary_file, 'w') as f:
        f.write(f"Model: {config.model_name}\n")
        f.write(f"Dataset: {config.data_file}\n")
        f.write(f"Samples: {len(dataset)}\n")
        f.write(f"Epochs: {config.num_epochs}\n")
        f.write(f"LoRA rank: {config.lora_r}\n")
        f.write(f"Learning rate: {config.learning_rate}\n")
        f.write(f"Output: {config.output_dir}\n")

    logger.info(f"Training summary saved to {summary_file}")


def main():
    """Main entry point"""
    # Create config
    config = Config()

    # Check if data exists
    if not Path(config.data_file).exists():
        logger.error(f"Data file not found: {config.data_file}")
        logger.error("Please run data collection scripts first")
        return

    # Print configuration
    logger.info("\nTraining Configuration:")
    logger.info(f"  Model: {config.model_name}")
    logger.info(f"  Data: {config.data_file}")
    logger.info(f"  Quantization: {'4-bit (QLoRA)' if config.use_4bit else 'None'}")
    logger.info(f"  LoRA rank: {config.lora_r}")
    logger.info(f"  Epochs: {config.num_epochs}")
    logger.info(f"  Batch size: {config.batch_size}")
    logger.info(f"  Gradient accumulation: {config.gradient_accumulation_steps}")
    logger.info(f"  Effective batch size: {config.batch_size * config.gradient_accumulation_steps}")
    logger.info(f"  Learning rate: {config.learning_rate}")
    logger.info(f"  Output: {config.output_dir}\n")

    # Start training
    train(config)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Check if everything is ready for training
"""

import sys
from pathlib import Path
import json

def check_file(path: Path, name: str) -> bool:
    """Check if file exists"""
    if path.exists():
        print(f"  ✅ {name}: {path}")
        return True
    else:
        print(f"  ❌ {name}: NOT FOUND at {path}")
        return False

def check_data():
    """Check dataset"""
    print("\n📊 Checking dataset...")

    data_file = Path('data/raw/final_dataset.jsonl')

    if not data_file.exists():
        print(f"  ❌ Dataset not found: {data_file}")
        return False

    # Count lines
    with open(data_file, 'r') as f:
        lines = f.readlines()

    print(f"  ✅ Dataset: {data_file}")
    print(f"  📈 Examples: {len(lines)}")

    # Check first example
    try:
        first = json.loads(lines[0])
        print(f"  ✅ Format: Valid JSONL")
        print(f"  📝 First example title: {first.get('title', 'N/A')[:60]}...")
    except Exception as e:
        print(f"  ⚠️  Warning: Could not parse first line: {e}")

    return True

def check_scripts():
    """Check if training scripts exist"""
    print("\n🔧 Checking scripts...")

    scripts = {
        'Training script': Path('scripts/train.py'),
        'Inference script': Path('scripts/inference.py'),
        'Data collection (advanced)': Path('scripts/collect_data_advanced.py'),
        'Data collection (writeups)': Path('scripts/collect_writeups.py'),
        'Data collection (GitHub)': Path('scripts/collect_github_writeups.py'),
    }

    all_ok = True
    for name, path in scripts.items():
        if not check_file(path, name):
            all_ok = False

    return all_ok

def check_docs():
    """Check documentation"""
    print("\n📚 Checking documentation...")

    docs = {
        'Training guide': Path('docs/TRAINING_GUIDE.md'),
        'Focus': Path('FOCUS.md'),
        'Next steps': Path('NEXT_STEPS.md'),
    }

    all_ok = True
    for name, path in docs.items():
        if not check_file(path, name):
            all_ok = False

    return all_ok

def check_requirements():
    """Check requirements.txt"""
    print("\n📦 Checking dependencies...")

    req_file = Path('requirements.txt')

    if not req_file.exists():
        print(f"  ❌ requirements.txt not found")
        return False

    print(f"  ✅ requirements.txt exists")

    # Check for key packages
    with open(req_file, 'r') as f:
        content = f.read()

    key_packages = ['torch', 'transformers', 'peft', 'datasets', 'bitsandbytes']
    missing = []

    for pkg in key_packages:
        if pkg in content:
            print(f"  ✅ {pkg}")
        else:
            print(f"  ⚠️  {pkg} not found in requirements")
            missing.append(pkg)

    return len(missing) == 0

def main():
    print("="*70)
    print("Training Setup Check")
    print("="*70)

    checks = [
        ('Dataset', check_data),
        ('Scripts', check_scripts),
        ('Documentation', check_docs),
        ('Requirements', check_requirements),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ❌ Error checking {name}: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "="*70)
    print("Summary")
    print("="*70)

    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")
        if not result:
            all_passed = False

    print("="*70)

    if all_passed:
        print("\n🎉 All checks passed! Ready to start training.")
        print("\nNext steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Start training: python scripts/train.py")
        print("  3. Test model: python scripts/inference.py")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

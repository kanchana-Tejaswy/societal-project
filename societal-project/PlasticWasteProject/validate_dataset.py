import os

DATASET_DIR = "dataset/train"
CLASSES = ["glass", "metal", "paper", "plastic"]
MINIMUM_SAMPLES = 100

def validate_dataset():
    """
    MLOps verification script.
    Checks dataset integrity and warns against severe class imbalances securely.
    """
    print("--- DATASET VALIDATION PIPELINE ---")
    
    if not os.path.exists(DATASET_DIR):
        print(f"❌ CRITICAL ERROR: Dataset directory '{DATASET_DIR}' completely missing.")
        print(f"Please formulate the explicit tree tracking exactly: {CLASSES}")
        return False

    counts = {}
    valid = True

    # Check structural boundaries
    for cls in CLASSES:
        cls_path = os.path.join(DATASET_DIR, cls)
        if not os.path.exists(cls_path):
            print(f"❌ MISSING FOLDER: Expected structured directory -> {cls_path}")
            valid = False
            counts[cls] = 0
            continue
            
        # Count explicit valid file types dynamically checking safe constraints
        valid_files = [f for f in os.listdir(cls_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        counts[cls] = len(valid_files)

    print("\n--- CLASS DISTRIBUTION ---")
    for cls, count in counts.items():
        status = "✅ PASS" if count >= MINIMUM_SAMPLES else f"⚠️ WARNING (Needs {MINIMUM_SAMPLES})"
        print(f"[{cls}]: {count} images -> {status}")

    # Check Imbalance cleanly mathematically natively
    max_count = max(counts.values()) if counts else 0
    min_count = min(counts.values()) if counts else 0
    
    if max_count > 0 and (min_count / max_count) < 0.3:
        print("\n❌ SEVERE IMBALANCE: Standard minority classes exist heavily skewed.")
        print("Neural Networks dynamically bias cleanly mapping explicitly to the majority class natively. Equalize parameters.")
        valid = False

    print("\n--- FINAL STATUS ---")
    if valid:
        print("MOCK VALIDATION PIPELINE SECURE. Proceed cleanly executing `train_cnn.py`.")
    else:
        print("SYSTEM ABORT: Target dataset violates standard strict MLOps architecture identically tracking safely.")

if __name__ == "__main__":
    validate_dataset()

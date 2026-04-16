import os

# ----------------------------------------------------
# 1. CONFIGURATION
# ----------------------------------------------------
DATASET_DIR = "dataset/train"
CLASSES = ["glass", "metal", "paper", "plastic"]
MIN_SAMPLES = 100
IMBALANCE_THRESHOLD = 0.3

# ----------------------------------------------------
# 2. DATASET VALIDATION
# ----------------------------------------------------
def validate_dataset():
    """
    Validates dataset structure and class distribution
    for CNN training readiness.
    """

    print("\n==============================")
    print(" DATASET VALIDATION REPORT")
    print("==============================\n")

    # Check dataset root
    if not os.path.exists(DATASET_DIR):
        print(f"ERROR: Dataset folder not found -> {DATASET_DIR}")
        print("Expected structure:")
        print("dataset/train/glass")
        print("dataset/train/metal")
        print("dataset/train/paper")
        print("dataset/train/plastic\n")
        return False

    counts = {}

    # ----------------------------------------------------
    # 3. COUNT FILES PER CLASS
    # ----------------------------------------------------
    for cls in CLASSES:
        class_path = os.path.join(DATASET_DIR, cls)

        if not os.path.exists(class_path):
            print(f"WARNING: Missing folder -> {class_path}")
            counts[cls] = 0
            continue

        files = [
            f for f in os.listdir(class_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        counts[cls] = len(files)

    # ----------------------------------------------------
    # 4. DISPLAY DISTRIBUTION
    # ----------------------------------------------------
    print("CLASS DISTRIBUTION:\n")

    for cls, count in counts.items():
        status = "OK" if count >= MIN_SAMPLES else "LOW DATA"
        print(f"{cls:<10} : {count} images -> {status}")

    # ----------------------------------------------------
    # 5. IMBALANCE CHECK
    # ----------------------------------------------------
    max_count = max(counts.values()) if counts else 0
    min_count = min(counts.values()) if counts else 0

    valid = True

    if max_count > 0:
        imbalance_ratio = min_count / max_count

        if imbalance_ratio < IMBALANCE_THRESHOLD:
            print("\nWARNING: Dataset imbalance detected!")
            print(f"Imbalance Ratio: {imbalance_ratio:.2f}")
            print("Recommendation: Balance dataset for better CNN performance.")
            valid = False

    # ----------------------------------------------------
    # 6. FINAL STATUS
    # ----------------------------------------------------
    print("\n==============================")
    if valid:
        print("DATASET STATUS: READY FOR TRAINING")
    else:
        print("DATASET STATUS: NEEDS IMPROVEMENT")
    print("==============================\n")

    return valid


# ----------------------------------------------------
# 7. RUN SCRIPT
# ----------------------------------------------------
if __name__ == "__main__":
    validate_dataset()
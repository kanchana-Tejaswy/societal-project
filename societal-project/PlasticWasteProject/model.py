import pandas as pd
import numpy as np
import random
import joblib

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ----------------------------------------------------
# 1. REPRODUCIBLE SEED SETUP
# ----------------------------------------------------
np.random.seed(42)
random.seed(42)

# ----------------------------------------------------
# 2. SYNTHETIC DATASET GENERATION
# ----------------------------------------------------
plastic_types = []
quantities = []
recyclables = []

# 0 = PET, 1 = HDPE, 2 = PVC
for _ in range(150):
    ptype = random.choice([0, 1, 2])
    qty = random.randint(1, 100)

    # Realistic decision boundaries (simple ML demo logic)
    if ptype == 0:       # PET
        rec = 1 if qty < 85 else 0
    elif ptype == 1:     # HDPE
        rec = 1 if qty < 45 else 0
    else:                 # PVC
        rec = 1 if qty < 15 else 0

    plastic_types.append(ptype)
    quantities.append(qty)
    recyclables.append(rec)

df = pd.DataFrame({
    "plastic_type": plastic_types,
    "quantity": quantities,
    "recyclable": recyclables
})

# ----------------------------------------------------
# 3. FEATURES & LABELS
# ----------------------------------------------------
X = df[["plastic_type", "quantity"]]
y = df["recyclable"]

# ----------------------------------------------------
# 4. TRAIN / TEST SPLIT
# ----------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# ----------------------------------------------------
# 5. MODEL TRAINING
# ----------------------------------------------------
model = DecisionTreeClassifier(
    max_depth=4,
    random_state=42
)

model.fit(X_train, y_train)

# ----------------------------------------------------
# 6. EVALUATION
# ----------------------------------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n==============================")
print("MODEL TRAINING COMPLETED")
print("==============================")
print(f"Dataset Size      : {len(df)} rows")
print(f"Test Accuracy     : {accuracy:.4f}")
print("==============================\n")

# ----------------------------------------------------
# 7. SAVE MODEL
# ----------------------------------------------------
joblib.dump(model, "waste_model.pkl")

print("Model successfully saved as: waste_model.pkl")
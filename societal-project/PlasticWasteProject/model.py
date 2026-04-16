import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import random

# --------------------------------------
# 1. EXPANDED SYNTHETIC TRAINING DATASET
# --------------------------------------
# Creates a realistic structural demo dataset mapping standard classification boundaries safely.
np.random.seed(42)
random.seed(42)

plastic_types = []
quantities = []
recyclables = []

# Generate 150 structurally sound rows
for _ in range(150):
    ptype = random.choice([0, 1, 2]) # 0=PET, 1=HDPE, 2=PVC
    qty = random.randint(1, 100)
    
    # Establish realistic boundaries for the mock ML application
    if ptype == 0:
        rec = 1 if qty < 85 else 0
    elif ptype == 1:
        rec = 1 if qty < 45 else 0
    else: 
        rec = 1 if qty < 15 else 0
        
    plastic_types.append(ptype)
    quantities.append(qty)
    recyclables.append(rec)

df = pd.DataFrame({
    "plastic_type": plastic_types,
    "quantity": quantities,
    "recyclable": recyclables
})

# --------------------------------------
# 2. FEATURES & LABEL
# --------------------------------------
X = df[["plastic_type", "quantity"]]
y = df["recyclable"]

# --------------------------------------
# 3. TRAIN / TEST SPLIT
# --------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# --------------------------------------
# 4. MODEL TRAINING (Bounded)
# --------------------------------------
# Restricting Max-Depth prevents pure overfitting memorization on the synthetic data
model = DecisionTreeClassifier(
    max_depth=4,
    random_state=42
)

model.fit(X_train, y_train)

# --------------------------------------
# 5. EVALUATION
# --------------------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Dataset Size: {len(df)} rows")
print(f"Model Accuracy: {accuracy:.4f}")

# --------------------------------------
# 6. SAVE MODEL
# --------------------------------------
joblib.dump(model, "waste_model.pkl")
print("Model Created Successfully & Saved as waste_model.pkl")
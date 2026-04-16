import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

# Global Config
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
DATASET_DIR = "dataset"

def train_waste_cnn():
    """
    Extremely rigid standard Training Environment natively targeting 4-class folder layouts safely.
    Requires locally formatting directories precisely to execute strictly successfully.
    """
    if not os.path.exists(os.path.join(DATASET_DIR, "train")):
        print(f"Error: Could not find '{DATASET_DIR}/train' directory.")
        print("Please structure your dataset identically as:")
        print(" dataset/")
        print("   train/")
        print("     glass/")
        print("     metal/")
        print("     paper/")
        print("     plastic/")
        return

    # 1. Dataset Preprocessing Pipeline (Image Augmentation Limits explicitly bounds overfitting)
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2, # 80/20 train/validation split dynamically
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True
    )

    train_generator = train_datagen.flow_from_directory(
        os.path.join(DATASET_DIR, "train"),
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    val_generator = train_datagen.flow_from_directory(
        os.path.join(DATASET_DIR, "train"),
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )

    print("Detected Class Mapping Constraints:", train_generator.class_indices)

    # 2. Build MobileNetV2 Transfer Learning Architecture
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Freeze standard base weights blocking unneeded computations and catastrophic forgetting structurally.
    base_model.trainable = False

    # 3. Dynamic Custom Classification Head mapping 4 Explicit categories natively.
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    predictions = Dense(4, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)

    # 4. Compilation
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    print("Executing Routine Matrix Compilation...")

    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=EPOCHS
    )

    # 5. Output physical bounds securely handling Flask mappings sequentially
    model.save("waste_cnn_model.h5")
    print("\nModel Compiled Successfully -> waste_cnn_model.h5")

if __name__ == "__main__":
    train_waste_cnn()

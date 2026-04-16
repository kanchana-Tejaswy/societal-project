import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

# ----------------------------------------------------
# 1. CONFIGURATION
# ----------------------------------------------------
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
DATASET_DIR = "dataset"

# ----------------------------------------------------
# 2. TRAINING FUNCTION
# ----------------------------------------------------
def train_waste_cnn():

    train_path = os.path.join(DATASET_DIR, "train")

    # Safety check
    if not os.path.exists(train_path):
        print("\nERROR: Dataset not found!")
        print("Expected structure:")
        print("dataset/train/glass")
        print("dataset/train/metal")
        print("dataset/train/paper")
        print("dataset/train/plastic\n")
        return

    # ----------------------------------------------------
    # 3. DATA AUGMENTATION
    # ----------------------------------------------------
    datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True
    )

    train_generator = datagen.flow_from_directory(
        train_path,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    val_generator = datagen.flow_from_directory(
        train_path,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )

    print("\nClass Mapping:", train_generator.class_indices)

    # ----------------------------------------------------
    # 4. MODEL (MobileNetV2 Transfer Learning)
    # ----------------------------------------------------
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3)
    )

    base_model.trainable = False  # freeze base model

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    outputs = Dense(4, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=outputs)

    # ----------------------------------------------------
    # 5. COMPILE MODEL
    # ----------------------------------------------------
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    print("\nStarting training...\n")

    # ----------------------------------------------------
    # 6. TRAIN MODEL
    # ----------------------------------------------------
    model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=EPOCHS
    )

    # ----------------------------------------------------
    # 7. SAVE MODEL
    # ----------------------------------------------------
    model.save("waste_cnn_model.h5")

    print("\nSUCCESS: Model saved as waste_cnn_model.h5")

# ----------------------------------------------------
# 8. RUN SCRIPT
# ----------------------------------------------------
if __name__ == "__main__":
    train_waste_cnn()
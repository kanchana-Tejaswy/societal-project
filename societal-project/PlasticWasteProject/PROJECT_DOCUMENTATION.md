# 📘 Extensive Project Documentation: Plastic Waste Management System

This document provides a deep-dive analysis into every component, file, and function of the Plastic Waste Management System.

---

## 1. Backend Core (`app.py`)

The `app.py` file serves as the nervous system of the application. It uses the Flask framework to handle HTTP requests and coordinate between different modules.

### Imports and Configuration
- **Flask**: The web framework used to serve the application.
- **Joblib**: Used for loading the traditional Scikit-learn model (`waste_model.pkl`).
- **Werkzeug**: Provides utilities for safe filename handling.
- **MAX_CONTENT_LENGTH**: Set to 5MB to ensure server stability and prevent memory overflow during image uploads.

### Main Routes
- `index()`: Serves the landing page (`landing.html`).
- `submit()`: Serves the main interface for waste entry (`index.html`).
- `dashboard()`: Retrieves all records from the SQLite database, performs server-side aggregation (counting recyclable vs. non-recyclable items), and renders `dashboard.html`.

### The Intelligence Pipeline (`/add` route)
This is the most critical part of the application. When a user submits waste:
1. **Data Extraction**: It pulls `plastic_type` and `quantity` from the form.
2. **Traditional ML Fallback**: If a scikit-learn model is present, it uses the input features to predict recyclability.
3. **CNN Processing**:
    - If an image is uploaded, it's converted to bytes.
    - `process_image_for_cnn` (from `utils.py`) prepares the image.
    - `evaluate_waste_cnn` (from `ml_model.py`) runs the TensorFlow inference.
4. **Logic Merging**: The system prioritizes CNN results if they have high confidence.
5. **Persistence**: The final classification, quantity, and recyclability status are saved via `add_waste_log`.

---

## 2. Database Management (`database.py`)

The system uses SQLite for its simplicity and zero-configuration requirement.

### Schema Design
The `waste` table consists of:
- `id`: Auto-incrementing primary key.
- `plastic_type`: The detected or selected material.
- `quantity`: Number of items.
- `recyclable`: Status string (often includes confidence %).
- `created_at`: Automatic timestamp.
- `image_path`: (Optional) Path to the stored image.

### Key Functions
- `init_db()`: Checks if the database file exists and creates the table if not. It also includes an `ALTER TABLE` statement wrapped in a try-except block to gracefully upgrade existing databases without losing data.
- `add_waste_log(...)`: Uses parameterized queries to prevent SQL injection.
- `get_all_waste()`: Fetches records sorted by ID in descending order so the newest entries appear first in the dashboard.

---

## 3. Deep Learning Architecture (`ml_model.py` & `train_cnn.py`)

### The Model: MobileNetV2
We use **MobileNetV2** for several reasons:
- **Efficiency**: It is significantly faster and smaller than VGG16 or ResNet50, making it ideal for local Flask deployment.
- **Accuracy**: Despite its size, it maintains high accuracy for object classification.

### Training Logic (`train_cnn.py`)
1. **Data Augmentation**: Uses `ImageDataGenerator` to perform random rotations, shifts, and flips. This prevents the model from overfitting and helps it generalize better to real-world (often blurry or tilted) waste photos.
2. **Transfer Learning**:
    - The base model is loaded with `weights='imagenet'`.
    - `base_model.trainable = False` ensures we don't destroy the pre-learned features of the model.
    - A custom "Head" is added: `GlobalAveragePooling2D` -> `Dense(128, ReLU)` -> `Dense(4, Softmax)`.
3. **Classification**: The final layer has 4 neurons corresponding to Glass, Metal, Paper, and Plastic.

### Inference Logic (`ml_model.py`)
- Loads the `.h5` file once on startup to avoid overhead.
- Uses `np.argmax` to find the class with the highest probability.
- Returns both the label and the confidence score.

---

## 4. Utility Layer (`utils.py`)

This file contains the "Plumbing" of the ML pipeline.

- **`allowed_file`**: A security function that checks the file extension against a whitelist (`png`, `jpg`, `jpeg`).
- **`process_image_for_cnn`**:
    - Opens the image using **Pillow (PIL)**.
    - Converts it to **RGB** (removing alpha channels from PNGs).
    - Resizes it to exactly **224x224** pixels.
    - Converts it to a **Numpy Array** and scales values to **[0, 1]**.
    - Adds a **Batch Dimension**, as TensorFlow expects a 4D tensor `(batch, height, width, channels)`.

---

## 5. Frontend Aesthetics (`static/` & `templates/`)

### Design Philosophy: Glassmorphism
The UI uses a "Glassmorphism" effect, characterized by:
- **Translucency**: Backgrounds use `rgba(255, 255, 255, 0.1)` with a `backdrop-filter: blur(10px)`.
- **Vibrant Gradients**: Deep blues and purples to give a futuristic feel.
- **Floating UI**: Cards appear to float over the background with subtle shadows.

### Interactive Components
- **`dashboard.js`**: (Future) Could be used for real-time chart updates using Chart.js.
- **`main.js`**: Handles the file upload "preview" so users see their image before submitting.
- **`landing.js`**: Implements scroll animations and entrance effects for a premium feel.

---

## 6. Deployment (`vercel.json` & `requirements.txt`)

- **`vercel.json`**: Configures the project for Vercel's serverless environment, mapping the Flask entry point to the web handler.
- **`requirements.txt`**: Lists specific versions of `tensorflow`, `flask`, `scikit-learn`, and `pillow` to ensure environment parity across different machines.

---

## 7. Data Export Pipeline

The `/download` route in `app.py` implements a memory-efficient CSV generator. Instead of loading the entire dataset into memory and then sending it, it uses a **Python Generator** with `yield` to stream the CSV rows directly to the browser. This is crucial if the database grows to thousands of records.

---

## 8. Summary of Class Mapping
The system maps its 4 CNN classes to recyclability:
| Class | Recyclability Status |
|-------|----------------------|
| Glass | Recyclable |
| Metal | Recyclable |
| Paper | Recyclable |
| Plastic | Recyclable (subject to type) |

---
*This document is intended for developers and researchers looking to understand or extend the Plastic Waste Management System.*

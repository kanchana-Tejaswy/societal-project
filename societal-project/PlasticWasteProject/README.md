# ♻️ AI-Powered Plastic Waste Management System

## 🌟 Overview
The **AI-Powered Plastic Waste Management System** is a cutting-edge, end-to-end web application designed to revolutionize how we track, classify, and manage plastic waste. Built with a robust **Flask** backend and a premium, high-performance frontend, this system leverages advanced **Convolutional Neural Networks (CNN)** and traditional **Machine Learning** to provide real-time waste classification and recyclability analysis.

This project serves as a comprehensive tool for environmental monitoring, allowing users to upload images of waste, get instant classifications, and visualize environmental impact through a dynamic analytics dashboard.

---

## 🏗️ System Architecture

The application follows a modular architecture, ensuring scalability, maintainability, and high performance.

### 1. Frontend Layer
- **HTML5 & Semantic UI**: Structured for accessibility and SEO.
- **Vanilla CSS (Premium Design)**: Implements a modern "Glassmorphism" aesthetic with dark mode support, smooth transitions, and responsive layouts.
- **Dynamic JavaScript**: Handles client-side interactions, file upload previews, and interactive dashboard elements.

### 2. Backend Layer (Flask)
- **Routing Engine**: Efficiently handles requests for landing, submission, and dashboard views.
- **Logic Controller**: Orchestrates the interaction between the database, ML models, and image processing utilities.
- **File System Management**: Securely handles image streams and static asset delivery.

### 3. Intelligence Layer (AI/ML)
- **Primary CNN (MobileNetV2)**: A deep learning model trained on waste datasets to classify images into categories: `Glass`, `Metal`, `Paper`, and `Plastic`.
- **Secondary ML Fallback**: A scikit-learn based model that predicts recyclability based on material type and quantity if image classification is unavailable or has low confidence.
- **Image Preprocessing Pipeline**: Standardizes image data (resizing, normalization) before inference.

### 4. Persistence Layer (SQLite)
- **Lightweight RDBMS**: Stores waste logs, classification results, and timestamps.
- **Schema Migration**: Automatically handles schema updates (e.g., adding image paths) to maintain data integrity.

---

## 📂 Project Structure Explained

```text
PlasticWasteProject/
├── app.py              # Main Flask application entry point
├── database.py         # Database initialization and CRUD operations
├── ml_model.py         # TensorFlow/CNN inference logic
├── model.py            # Secondary ML model management
├── train_cnn.py        # Script to train/fine-tune the CNN model
├── utils.py            # Image processing and utility functions
├── database.db         # SQLite database file
├── waste_model.pkl     # Pre-trained scikit-learn model
├── waste_cnn_model.h5  # Pre-trained TensorFlow CNN model
├── requirements.txt    # Project dependencies
├── static/             # Frontend assets
│   ├── index.css       # Core styling (Glassmorphism)
│   ├── dashboard.css   # Dashboard-specific styling
│   ├── landing.css     # Landing page aesthetics
│   ├── main.js         # Core frontend logic
│   └── uploads/        # Directory for temporary file storage
└── templates/          # HTML templates
    ├── landing.html    # Entry point/Landing page
    ├── index.html      # Waste submission form
    └── dashboard.html  # Analytics and history view
```

---

## 🧠 Machine Learning Deep Dive

### Convolutional Neural Network (CNN)
The system uses a **MobileNetV2** architecture, which is optimized for mobile and edge performance. 
- **Preprocessing**: Images are resized to `224x224` and normalized to `[0, 1]` range.
- **Transfer Learning**: We leverage ImageNet weights, freezing the base layers and training a custom head for waste classification.
- **Classes**: Glass, Metal, Paper, Plastic.

### Recyclability Logic
The classification results are mapped to recyclability status:
- **High Confidence (>70%)**: The system trusts the CNN and assigns the status accordingly.
- **Low Confidence**: Falls back to a conservative "Non-Recyclable" classification or triggers the secondary ML model.

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9+
- Pip (Python Package Manager)

### Steps
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd PlasticWasteProject
   ```

2. **Setup Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   The database initializes automatically on the first run of `app.py`.

5. **Run the Application**
   ```bash
   python app.py
   ```
   The app will be available at `http://127.0.0.1:5000`.

---

## 📊 Features & Functionality

### 1. Smart Landing Page
A premium entry point that explains the mission of the project and directs users to either submit waste or view the dashboard.

### 2. Intelligent Waste Submission
- **Image Upload**: Users can drag and drop or select images of waste.
- **Real-time Inference**: The backend processes the image through the CNN immediately upon submission.
- **Manual Override**: Option to specify plastic type and quantity for secondary analysis.

### 3. Interactive Analytics Dashboard
- **Live Counters**: Real-time tracking of total items, recyclable vs. non-recyclable count.
- **Data Table**: A comprehensive history of all logged waste items.
- **Data Export**: One-click download of the entire database in `.csv` format for external reporting.
- **Management Tools**: Ability to clear historical data for new sessions.

---

## 🛡️ Data Security & Reliability
- **Input Validation**: Strictly limits file types to `jpg`, `jpeg`, and `png`.
- **Payload Limits**: Flask is configured to reject files larger than 5MB to prevent DoS attacks.
- **Schema Safety**: The database layer includes graceful patching to ensure compatibility across different deployment versions.

---

## 🚀 Future Roadmap
- **GPS Tagging**: Track the geographic location of waste clusters.
- **Multi-Object Detection**: Detect multiple items in a single image using YOLOv8.
- **User Authentication**: Allow users to maintain personal waste tracking accounts.
- **Cloud Integration**: AWS S3 for permanent image storage and AWS RDS for scaled databases.

---

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

---
**Developed with ❤️ for a Greener Planet.**

import io
import numpy as np
from PIL import Image, UnidentifiedImageError

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image_for_cnn(image_bytes, filename=""):
    """
    Safely intercepts incoming image bytes and transforms them precisely identically 
    into a mathematically valid preprocessed tensor suitable for Custom Deep Learning injection securely.
    """
    if filename and not allowed_file(filename):
        return {"valid": False, "error": "Invalid file format. Only JPG/PNG explicitly allowed natively."}
        
    try:
        # Load directly strictly off RAM buffer safely natively checking execution bounds
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Extrapolate dimensional scale to physically fit MobileNetV2 (224x224) natively without exhausting server RAM caches directly
        img = img.resize((224, 224))
        
        # Format array mathematically uniformly identically tracking preprocessing rules organically
        img_array = np.array(img, dtype=np.float32)
        img_array = img_array / 255.0
        
        # Reshape tightly explicitly enforcing (1, 224, 224, 3) matrix mapping logically natively
        img_array = np.expand_dims(img_array, axis=0)
        
        return {
            "valid": True,
            "tensor": img_array
        }
    except UnidentifiedImageError:
        return {"valid": False, "error": "Unrecognized or falsified image format."}
    except Exception as e:
        print("Image Tensor Array Generation Error:", e)
        return {"valid": False, "error": "Corrupted datastream or malicious payload intercept natively."}
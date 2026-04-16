import logging
import os
import io
import csv
from flask import Flask, render_template, request, redirect, Response

# ----------------------------------------------------
# 1. SETUP LOGGING
# ----------------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from database import init_db, add_waste_log, get_all_waste, clear_database
from utils import process_image_for_cnn
from ml_model import evaluate_waste_cnn

app = Flask(__name__, static_folder='static', static_url_path='/static')

# ----------------------------------------------------
# 2. FLASK APP STABILITY (CRITICAL SECURITY)
# ----------------------------------------------------
# Strictly rejects massively scaled payloads blocking Server memory exhausts optimally natively
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  

# Initialize Safe DB 
init_db()

@app.route('/')
def home():
    return render_template("landing.html")

@app.route('/submit')
def submit():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    data = get_all_waste()
    return render_template("dashboard.html", data=data)

@app.route('/add', methods=['POST'])
def add_waste():
    try:
        try:
            quantity = int(request.form.get('quantity', 1))
        except ValueError:
            quantity = 1

        plastic_type = request.form.get('plastic_type', 'Unknown')
        image_file = request.files.get('image')

        predicted_class = "Missing Submission"
        recyclability = "No (Default Threshold)"
        confidence_str = "0%"

        if image_file and image_file.filename != "":
            logger.info(f"Processing Upload securely bounds tracked: {image_file.filename}")
            
            image_bytes = image_file.read()
            image_file.seek(0) # Flush memory properly preventing subsequent processing leaks

            # Extract strictly normalized physical Tensor securely
            cnn_data = process_image_for_cnn(image_bytes, filename=image_file.filename)

            if cnn_data.get("valid"):
                # Predict CNN Tracking natively cleanly
                predicted_class, confidence = evaluate_waste_cnn(cnn_data.get("tensor"))
                confidence_str = f"({confidence:.1f}%)"

                if predicted_class in ["Glass", "Metal", "Paper", "Plastic"]:
                    recyclability = f"Yes {confidence_str}"
                else: 
                    recyclability = f"No {confidence_str}"
            else:
                predicted_class = cnn_data.get("error", "Corrupt Input")
                recyclability = "No (System Extraction Error)"
                logger.warning(f"Upload pre-processing aborted: {predicted_class}")
        else:
            predicted_class = plastic_type
            logger.info("Upload natively lacked Image structures; fallback securely used.")

        # Push securely onto Thread-Safe SQLite Pipeline
        add_waste_log(predicted_class, quantity, recyclability)

        return redirect('/dashboard')

    except Exception as e:
        logger.error(f"Flask Route Add Critical Fault -> {e}")
        return redirect('/dashboard')

@app.route('/download')
def download_data():
    data = get_all_waste()
    
    def generate():
        output = io.StringIO()
        writer = csv.writer(output)
        yield '\ufeff'
        writer.writerow(['ID', 'Plastic Type', 'Quantity', 'Recyclable', 'Timestamp'])
        yield output.getvalue()
        output.seek(0); output.truncate(0)

        for row in data:
            writer.writerow(row)
            yield output.getvalue()
            output.seek(0); output.truncate(0)

    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment; filename=waste_data.csv"})

@app.route('/clear', methods=['POST'])
def clear_data():
    try:
        clear_database()
    except Exception as e:
        logger.error(f"Clear Process Error Crash Tracked: {e}")
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)
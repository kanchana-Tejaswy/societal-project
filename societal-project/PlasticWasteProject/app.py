import os
import csv
import io
import joblib
from flask import Flask, render_template, request, redirect, Response

from database import init_db, add_waste_log, get_all_waste, clear_database
from utils import process_image_for_cnn
from ml_model import evaluate_waste_cnn
import werkzeug.utils
import uuid

# -------------------------
# APP SETUP
# -------------------------
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

init_db()

# -------------------------
# LOAD ML MODEL (OPTIONAL)
# -------------------------
model = None
model_path = os.path.join(os.path.dirname(__file__), "waste_model.pkl")

if os.path.exists(model_path):
    try:
        model = joblib.load(model_path)
    except:
        model = None


# -------------------------
# ROUTES
# -------------------------
@app.route('/')
def home():
    return render_template("landing.html")


@app.route('/submit')
def submit():
    return render_template("index.html")


@app.route('/dashboard')
def dashboard():
    data = get_all_waste()
    total = len(data)
    recyclable = sum(1 for row in data if 'Recyclable' in str(row[3]) and 'Non-Recyclable' not in str(row[3]))
    non_recyclable = total - recyclable
    return render_template("dashboard.html", data=data, total=total, recyclable=recyclable, non_recyclable=non_recyclable)


# -------------------------
# MAIN PREDICTION ROUTE
# -------------------------
@app.route('/add', methods=['POST'])
def add_waste():

    plastic_type = request.form.get('plastic_type', 'Unknown')
    quantity = int(request.form.get('quantity', 1))
    image_file = request.files.get('image')

    prediction = plastic_type
    # -------------------------
    # STEP 1: FALLBACK ML MODEL (OPTIONAL)
    # -------------------------
    if model:
        try:
            mapping = {"PET": 0, "HDPE": 1, "PVC": 2}
            encoded = mapping.get(plastic_type, 0)

            pred = model.predict([[encoded, quantity]])

            result = "Recyclable" if pred[0] == 1 else "Non-Recyclable"
        except:
            result = "Non-Recyclable (Error)"
    else:
        # Hardcoded fallback if no model exists
        result = "Recyclable" if plastic_type in ["PET", "HDPE"] else "Non-Recyclable"

    # -------------------------
    # STEP 2: CNN IMAGE PREDICTION (PRIMARY)
    # -------------------------
    if image_file and image_file.filename != "":
        # 2. RUN INTELLIGENCE 
        image_bytes = image_file.read()
        cnn_data = process_image_for_cnn(image_bytes)

        if cnn_data.get("valid"):
            pred_class, confidence = evaluate_waste_cnn(cnn_data["tensor"])

            # Only overwrite if it correctly inferred a valid class
            if pred_class.lower() in ["glass", "metal", "paper", "plastic"]:
                prediction = pred_class
                if confidence > 70:
                    result = f"Recyclable ({confidence:.1f}%)"
                else:
                    result = "Non-Recyclable (Low Confidence)"

    # -------------------------
    # SAVE TO DATABASE
    # -------------------------
    add_waste_log(prediction, quantity, result)

    return redirect('/dashboard')


# -------------------------
# DOWNLOAD CSV
# -------------------------
@app.route('/download')
def download_data():
    data = get_all_waste()

    def generate():
        output = io.StringIO()
        writer = csv.writer(output)

        yield '\ufeff'
        writer.writerow(['ID', 'Plastic Type', 'Quantity', 'Recyclable'])

        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        for row in data:
            writer.writerow(row)
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    return Response(generate(),
                    mimetype='text/csv',
                    headers={"Content-Disposition": "attachment; filename=waste_data.csv"})


# -------------------------
# CLEAR DATABASE
# -------------------------
@app.route('/clear', methods=['POST'])
def clear_data():
    clear_database()
    return redirect('/dashboard')


# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
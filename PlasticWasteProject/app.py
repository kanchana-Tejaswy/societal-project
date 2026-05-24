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

import joblib
from database import init_db, add_waste_log, get_all_waste, clear_database, get_iot_status, get_leaderboard
from utils import process_image_for_cnn
from ml_model import evaluate_waste_cnn
from flask import Flask, render_template, request, redirect, Response, jsonify

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Ensure Database Schema is initialized natively on startup securely.
with app.app_context():
    init_db()

# ... (manual_model loading remains same)

@app.route('/')
def home():
    return render_template("landing.html")

@app.route('/submit')
def submit():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    data = get_all_waste()
    iot_data = get_iot_status()
    leaderboard = get_leaderboard()
    
    # Advanced KPI Calculations
    total_scanned = len(data)
    
    # Aggregate quantities securely ensuring no negatives
    total_quantity = sum(max(0, int(item['quantity'] if item['quantity'] else 0)) for item in data)
    
    recyclable_items = [item for item in data if "yes" in str(item['recyclable']).lower()]
    recyclable_count = len(recyclable_items)
    
    # Let's say 1 unit = ~0.05kg of plastic
    total_plastic_kg = total_quantity * 0.05 
    
    # 1 recyclable item saves roughly 0.12kg of CO2
    carbon_saved = recyclable_count * 0.12 
    
    non_recyclable_count = total_scanned - recyclable_count
    efficiency = (recyclable_count / total_scanned * 100) if total_scanned > 0 else 0
    total_points = sum(max(0, int(item['points'] if item['points'] else 0)) for item in data)

    kpis = {
        "total_scanned": total_scanned,
        "total_quantity": total_quantity,
        "recyclable_count": recyclable_count,
        "non_recyclable": non_recyclable_count,
        "efficiency": round(efficiency, 1),
        "total_kg": round(total_plastic_kg, 2),
        "carbon_saved": round(carbon_saved, 2),
        "total_points": total_points,
        "ai_accuracy": 94.2 # Simulated baseline for UI
    }
    
    return render_template("dashboard.html", data=data, iot_data=iot_data, leaderboard=leaderboard, kpis=kpis)

@app.route('/add', methods=['POST'])
def add_waste():
    try:
        quantity = int(request.form.get('quantity', 1))
        plastic_type = request.form.get('plastic_type', 'Unknown')
        user_id = request.form.get('user_id', 'Anonymous')
        lat = request.form.get('latitude')
        lon = request.form.get('longitude')
        
        # Convert lat/lon to float safely if present and not empty
        def safe_float(val):
            try:
                return float(val) if val and str(val).strip() != "" else None
            except:
                return None

        lat = safe_float(lat)
        lon = safe_float(lon)

        image_file = request.files.get('image')

        predicted_class = "Missing Submission"
        recyclability = "No (Default Threshold)"
        confidence_str = "0%"

        if image_file and image_file.filename != "":
            logger.info(f"Processing Upload: {image_file.filename}")
            image_bytes = image_file.read()
            image_file.seek(0)

            cnn_data = process_image_for_cnn(image_bytes, filename=image_file.filename)

            if cnn_data.get("valid"):
                predicted_class, confidence = evaluate_waste_cnn(cnn_data.get("tensor"))
                confidence_str = f"({confidence:.1f}%)"

                if any(c in predicted_class for c in ["Glass", "Metal", "Paper", "Plastic"]):
                    recyclability = f"Yes {confidence_str}"
                else: 
                    recyclability = f"No {confidence_str}"
                
                logged_type = f"{plastic_type} (AI: {predicted_class})"
            else:
                logged_type = f"{plastic_type} (AI Error)"
                recyclability = "No (Error)"
        else:
            logged_type = plastic_type
            if manual_model:
                type_map = {"PET": 0, "HDPE": 1, "PVC": 2}
                numeric_type = type_map.get(plastic_type, 0)
                prediction = manual_model.predict([[numeric_type, quantity]])[0]
                recyclability = "Yes (Manual ML)" if prediction == 1 else "No (Manual ML)"

        # Push securely onto Database with GPS and User ID
        add_waste_log(logged_type, quantity, recyclability, lat, lon, user_id)

        return redirect('/dashboard')

    except Exception as e:
        logger.error(f"Flask Route Add Critical Fault -> {e}")
        return redirect('/dashboard')

# ----------------------------------------------------
# ADVANCED API ENDPOINTS
# ----------------------------------------------------

@app.route('/api/iot-status')
def iot_status_api():
    """Returns simulated IoT bin status for external monitors."""
    data = get_iot_status()
    return jsonify([dict(row) for row in data])

@app.route('/api/export/gov')
def gov_export_api():
    """Standardized endpoint for Government/Smart City platform integration."""
    data = get_all_waste()
    summary = {
        "total_entries": len(data),
        "total_recyclable": sum(1 for r in data if "yes" in r['recyclable'].lower()),
        "total_points_awarded": sum(r['points'] for r in data),
        "timestamp": "Real-time Sync Active"
    }
    return jsonify({"status": "success", "data_summary": summary})

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
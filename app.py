"""
Phase (d) - Web-Based GUI
Microscope Specimen Size Calculator
CSC 442 - Computational Biology & Interdisciplinary Studies

Built with Flask - A lightweight Python web framework.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "microscope_calculator_secret_key_2025"

# Configuration
DB_NAME = "specimen_calculations.db"
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "tiff"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================================
# MAGNIFICATION DATA
# ==========================================
MICROSCOPES = {
    "Compound Light Microscope (Low Power)": 40,
    "Compound Light Microscope (Medium Power)": 100,
    "Compound Light Microscope (High Power)": 400,
    "Compound Light Microscope (Oil Immersion)": 1000,
    "Stereo Microscope (Low)": 10,
    "Stereo Microscope (Medium)": 20,
    "Stereo Microscope (High)": 40,
    "Scanning Electron Microscope (SEM)": 10000,
    "Transmission Electron Microscope (TEM)": 50000,
    "Fluorescence Microscope": 400,
    "Confocal Microscope": 400,
    "Atomic Force Microscope (AFM)": 1000000,
}

UNIT_CONVERSIONS = {
    "nm": 1e-6,
    "µm": 1e-3,
    "mm": 1.0,
    "cm": 10.0,
    "m": 1000.0,
}

OUTPUT_UNITS = ["nm", "µm", "mm", "cm", "m"]


def format_magnification(magnification):
    """Format a magnification value without unnecessary decimal places."""
    return f"{magnification:,.2f}".rstrip("0").rstrip(".")


# ==========================================
# DATABASE FUNCTIONS
# ==========================================
def init_database():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            specimen_size REAL NOT NULL,
            specimen_unit TEXT NOT NULL,
            microscope_type TEXT NOT NULL,
            magnification INTEGER NOT NULL,
            real_size REAL NOT NULL,
            real_size_unit TEXT NOT NULL,
            image_path TEXT,
            calculation_timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_calculation(username, specimen_size, specimen_unit, microscope_type,
                     magnification, real_size, real_size_unit, image_path):
    """Save a calculation record to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO calculations 
        (username, specimen_size, specimen_unit, microscope_type, magnification, 
         real_size, real_size_unit, image_path, calculation_timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, specimen_size, specimen_unit, microscope_type,
          magnification, real_size, real_size_unit, image_path, timestamp))
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id


def get_all_records():
    """Retrieve all records from the database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM calculations ORDER BY calculation_timestamp DESC")
    records = cursor.fetchall()
    conn.close()
    return [dict(record) for record in records]


def get_record_by_id(record_id):
    """Retrieve a specific record by ID."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM calculations WHERE id = ?", (record_id,))
    record = cursor.fetchone()
    conn.close()
    return dict(record) if record else None


def delete_record(record_id):
    """Delete a record from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM calculations WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()


def allowed_file(filename):
    """Check if file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ==========================================
# FLASK ROUTES
# ==========================================
@app.route("/")
def index():
    """Home page - Calculator."""
    return render_template("index.html",
                           microscopes=MICROSCOPES,
                           units=OUTPUT_UNITS,
                           format_magnification=format_magnification)


@app.route("/calculate", methods=["POST"])
def calculate():
    """Handle calculation request."""
    try:
        username = request.form.get("username", "").strip()
        measured_size = float(request.form.get("measured_size", 0))
        magnification_source = request.form.get("magnification_source", "microscope_type")
        microscope_type = request.form.get("microscope_type", "")
        custom_magnification = request.form.get("custom_magnification", "").strip()
        output_unit = request.form.get("output_unit", "mm")

        if not username:
            return jsonify({"error": "Username is required"}), 400
        if measured_size <= 0:
            return jsonify({"error": "Measured size must be greater than zero"}), 400
        if magnification_source == "microscope_type":
            if microscope_type not in MICROSCOPES:
                return jsonify({"error": "Invalid microscope type"}), 400
            magnification = MICROSCOPES[microscope_type]
        elif magnification_source == "custom_magnification":
            try:
                magnification = float(custom_magnification)
            except ValueError:
                return jsonify({"error": "Enter a valid magnification value"}), 400
            if magnification <= 0:
                return jsonify({"error": "Magnification must be greater than zero"}), 400
            microscope_type = "Custom magnification"
        else:
            return jsonify({"error": "Invalid magnification input method"}), 400

        # Handle image upload
        image_path = ""
        if "specimen_image" in request.files:
            file = request.files["specimen_image"]
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{filename}"
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)
                image_path = file_path

        # Perform calculation
        real_size_mm = measured_size / magnification
        conversion_factor = UNIT_CONVERSIONS[output_unit]
        real_size_output = real_size_mm / conversion_factor

        # Save to database
        record_id = save_calculation(
            username, measured_size, "mm", microscope_type,
            magnification, real_size_output, output_unit, image_path
        )

        return jsonify({
            "success": True,
            "record_id": record_id,
            "real_size": round(real_size_output, 10),
            "real_size_formatted": f"{real_size_output:.6f}",
            "unit": output_unit,
            "magnification": magnification,
            "magnification_formatted": format_magnification(magnification),
            "microscope_type": microscope_type,
            "measured_size": measured_size,
            "image_path": image_path,
            "breakdown": {
                "measured_size": measured_size,
                "magnification": magnification,
                "real_size_mm": real_size_mm,
                "conversion_factor": conversion_factor,
                "real_size_output": real_size_output
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/history")
def history():
    """View all calculation history."""
    records = get_all_records()
    return render_template("history.html", records=records)


@app.route("/api/records")
def api_records():
    """API endpoint to get all records as JSON."""
    records = get_all_records()
    return jsonify(records)


@app.route("/delete/<int:record_id>", methods=["POST"])
def delete(record_id):
    """Delete a record."""
    delete_record(record_id)
    flash("Record deleted successfully", "success")
    return redirect(url_for("history"))


@app.route("/api/delete/<int:record_id>", methods=["DELETE"])
def api_delete(record_id):
    """API endpoint to delete a record."""
    delete_record(record_id)
    return jsonify({"success": True, "message": "Record deleted"})


# ==========================================
# INITIALIZE
# ==========================================
if __name__ == "__main__":
    init_database()
    app.run(debug=True, host="0.0.0.0", port=5000)
else:
    init_database()

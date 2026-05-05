"""
Phase (c) - Python-Based GUI
Microscope Specimen Size Calculator
CSC 442 - Computational Biology & Interdisciplinary Studies

Built with Tkinter - Python's standard GUI library.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import sqlite3
import os
from datetime import datetime

# ==========================================
# DATABASE SETUP
# ==========================================
DB_NAME = "specimen_calculations.db"


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
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM calculations ORDER BY calculation_timestamp DESC")
    records = cursor.fetchall()
    conn.close()
    return records


def delete_record(record_id):
    """Delete a record from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM calculations WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()


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


class MicroscopeCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Microscope Specimen Size Calculator - Phase (c)")
        self.root.geometry("900x750")
        self.root.configure(bg="#f0f4f8")

        # Initialize database
        init_database()

        # Store uploaded image path
        self.uploaded_image_path = None
        self.photo_image = None

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f0f4f8")
        style.configure("TLabel", background="#f0f4f8", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#1a5276")
        style.configure("SubHeader.TLabel", font=("Segoe UI", 12, "bold"), foreground="#2874a6")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("Accent.TButton", background="#2874a6", foreground="white")
        style.configure("TCombobox", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))

    def create_widgets(self):
        """Create all GUI widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="🔬 Microscope Specimen Size Calculator",
                                style="Header.TLabel")
        title_label.pack(pady=(0, 5))

        subtitle = ttk.Label(main_frame, text="CSC 442 - Computational Biology & Interdisciplinary Studies",
                             font=("Segoe UI", 9), foreground="#666")
        subtitle.pack(pady=(0, 15))

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Calculator
        self.calc_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.calc_tab, text="🧮 Calculator")
        self.setup_calculator_tab()

        # Tab 2: History
        self.history_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.history_tab, text="📋 History")
        self.setup_history_tab()

    def setup_calculator_tab(self):
        """Setup the calculator tab."""
        # Left panel - Inputs
        left_frame = ttk.Frame(self.calc_tab)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Username
        user_frame = ttk.LabelFrame(left_frame, text="User Information", padding="10")
        user_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(user_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.username_entry = ttk.Entry(user_frame, width=30)
        self.username_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        # Specimen Image Upload
        image_frame = ttk.LabelFrame(left_frame, text="Specimen Image", padding="10")
        image_frame.pack(fill=tk.X, pady=(0, 10))

        self.image_label = ttk.Label(image_frame, text="No image uploaded",
                                     background="#e8e8e8", relief="sunken",
                                     anchor="center", width=40)
        self.image_label.pack(pady=5)

        btn_frame = ttk.Frame(image_frame)
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="📁 Browse Image", command=self.browse_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Clear Image", command=self.clear_image).pack(side=tk.LEFT, padx=5)

        # Measurement Inputs
        input_frame = ttk.LabelFrame(left_frame, text="Measurement Details", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # Measured Size
        ttk.Label(input_frame, text="Measured Size (mm):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.size_entry = ttk.Entry(input_frame, width=20)
        self.size_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Microscope Type
        ttk.Label(input_frame, text="Microscope Type:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.microscope_var = tk.StringVar()
        self.microscope_combo = ttk.Combobox(input_frame, textvariable=self.microscope_var,
                                              values=list(MICROSCOPES.keys()),
                                              state="readonly", width=45)
        self.microscope_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.microscope_combo.current(0)

        # Output Unit
        ttk.Label(input_frame, text="Output Unit:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.unit_var = tk.StringVar()
        self.unit_combo = ttk.Combobox(input_frame, textvariable=self.unit_var,
                                        values=OUTPUT_UNITS,
                                        state="readonly", width=10)
        self.unit_combo.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.unit_combo.current(2)  # Default to mm

        # Calculate Button
        calc_btn = ttk.Button(left_frame, text="🧮 Calculate Real Size",
                              command=self.calculate, style="Accent.TButton")
        calc_btn.pack(fill=tk.X, pady=10)

        # Right panel - Results
        right_frame = ttk.Frame(self.calc_tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Result Display
        result_frame = ttk.LabelFrame(right_frame, text="Calculation Result", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)

        self.result_text = ScrolledText(result_frame, wrap=tk.WORD, width=50, height=25,
                                         font=("Consolas", 10), bg="#fafafa")
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.insert(tk.END, "Results will appear here after calculation...")
        self.result_text.config(state=tk.DISABLED)

    def setup_history_tab(self):
        """Setup the history/records tab."""
        # Controls
        ctrl_frame = ttk.Frame(self.history_tab)
        ctrl_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(ctrl_frame, text="🔄 Refresh", command=self.refresh_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(ctrl_frame, text="🗑️ Delete Selected", command=self.delete_selected).pack(side=tk.LEFT, padx=5)

        # Treeview for records
        columns = ("ID", "Username", "Specimen Size", "Microscope", "Magnification",
                   "Real Size", "Unit", "Timestamp")
        self.tree = ttk.Treeview(self.history_tab, columns=columns, show="headings",
                                  height=20)

        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        self.tree.column("ID", width=50)
        self.tree.column("Username", width=100)
        self.tree.column("Microscope", width=200)
        self.tree.column("Timestamp", width=150)

        # Scrollbars
        vsb = ttk.Scrollbar(self.history_tab, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.history_tab, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.refresh_history()

    def browse_image(self):
        """Open file dialog to browse for specimen image."""
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("All files", "*.*")
        ]
        filepath = filedialog.askopenfilename(title="Select Specimen Image",
                                               filetypes=filetypes)
        if filepath:
            self.uploaded_image_path = filepath
            try:
                # Load and display thumbnail
                img = Image.open(filepath)
                img.thumbnail((300, 200))
                self.photo_image = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.photo_image, text="")
            except Exception as e:
                self.image_label.config(text=f"Image loaded: {os.path.basename(filepath)}")
                messagebox.showwarning("Image Preview", f"Could not preview image: {e}")

    def clear_image(self):
        """Clear the uploaded image."""
        self.uploaded_image_path = None
        self.photo_image = None
        self.image_label.config(image="", text="No image uploaded")

    def calculate(self):
        """Perform the calculation and display results."""
        # Validate inputs
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter your username.")
            return

        try:
            measured_size = float(self.size_entry.get().strip())
            if measured_size <= 0:
                messagebox.showerror("Error", "Measured size must be greater than zero.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid measured size.")
            return

        microscope_type = self.microscope_var.get()
        if not microscope_type:
            messagebox.showerror("Error", "Please select a microscope type.")
            return

        output_unit = self.unit_var.get()

        # Perform calculation
        magnification = MICROSCOPES[microscope_type]
        real_size_mm = measured_size / magnification
        conversion_factor = UNIT_CONVERSIONS[output_unit]
        real_size_output = real_size_mm / conversion_factor

        # Build result text
        result = f"""╔══════════════════════════════════════════════════════════════════════╗
║                    CALCULATION RESULT                                ║
╠══════════════════════════════════════════════════════════════════════╣
║  Username:            {username:<45} ║
║  Microscope Type:     {microscope_type:<45} ║
║  Magnification:       ×{magnification:>50,} ║
╠══════════════════════════════════════════════════════════════════════╣
║  FORMULA:                                                            ║
║    Real Size = Measured Size (mm) ÷ Magnification Factor            ║
╠══════════════════════════════════════════════════════════════════════╣
║  STEP-BY-STEP CALCULATION:                                           ║
║                                                                      ║
║    1. Measured Size (from image) = {measured_size:>12.6f} mm        ║
║    2. Magnification Factor       = ×{magnification:>12,}            ║
║    3. Real Size (in mm)          = {measured_size:.6f} ÷ {magnification}    ║
║                                    = {real_size_mm:.12f} mm         ║
║    4. Convert to {output_unit:<5}        = {real_size_mm:.12f} ÷ {conversion_factor}  ║
║                                    = {real_size_output:.12f} {output_unit}      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  ★ REAL SIZE: {real_size_output:>20.6f} {output_unit:<10}                ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝"""

        # Save to database
        image_path = self.uploaded_image_path if self.uploaded_image_path else ""
        record_id = save_calculation(
            username, measured_size, "mm", microscope_type,
            magnification, real_size_output, output_unit, image_path
        )

        result += f"\n\n✅ Record saved to database with ID: {record_id}"

        # Display result
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED)

        messagebox.showinfo("Success", f"Calculation complete!\nReal Size: {real_size_output:.6f} {output_unit}")

    def refresh_history(self):
        """Refresh the history treeview."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch and display records
        records = get_all_records()
        for record in records:
            rid, username, spec_size, spec_unit, mic_type, mag, real_size, real_unit, img_path, timestamp = record
            self.tree.insert("", tk.END, values=(rid, username, f"{spec_size:.4f} {spec_unit}",
                                                  mic_type, f"×{mag:,}",
                                                  f"{real_size:.6f}", real_unit, timestamp))

    def delete_selected(self):
        """Delete the selected record from history."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a record to delete.")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected record(s)?"):
            for item in selected:
                values = self.tree.item(item, "values")
                record_id = values[0]
                delete_record(record_id)
            self.refresh_history()
            messagebox.showinfo("Deleted", "Selected record(s) deleted successfully.")


def main():
    root = tk.Tk()
    app = MicroscopeCalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
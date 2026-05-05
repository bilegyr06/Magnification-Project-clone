"""
Phase (b) - Database Integration
Microscope Specimen Size Calculator
CSC 442 - Computational Biology & Interdisciplinary Studies
"""

import sqlite3
import os
from datetime import datetime

# ==========================================
# MICROSCOPE MAGNIFICATION FACTORS
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

DB_NAME = "specimen_calculations.db"


def init_database():
    """Initialize the SQLite database with the required table."""
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
            calculation_timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print(f"✅ Database '{DB_NAME}' initialized successfully.")


def save_calculation(username, specimen_size, specimen_unit, microscope_type, 
                     magnification, real_size, real_size_unit):
    """Save a calculation record to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO calculations 
        (username, specimen_size, specimen_unit, microscope_type, magnification, real_size, real_size_unit, calculation_timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, specimen_size, specimen_unit, microscope_type, 
          magnification, real_size, real_size_unit, timestamp))

    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id


def view_all_records():
    """Display all saved calculation records."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM calculations ORDER BY calculation_timestamp DESC")
    records = cursor.fetchall()
    conn.close()

    if not records:
        print("\n📭 No records found in the database.")
        return

    print("\n" + "=" * 100)
    print("   ALL CALCULATION RECORDS")
    print("=" * 100)
    print(f"{'ID':<5} {'Username':<15} {'Specimen Size':<15} {'Microscope':<35} {'Real Size':<20} {'Timestamp'}")
    print("-" * 100)

    for record in records:
        rid, username, spec_size, spec_unit, mic_type, mag, real_size, real_unit, timestamp = record
        print(f"{rid:<5} {username:<15} {spec_size:>8.4f} {spec_unit:<5} {mic_type:<35} {real_size:>10.6f} {real_unit:<8} {timestamp}")

    print("=" * 100)
    print(f"Total records: {len(records)}")


def view_records_by_user(username):
    """Display records for a specific user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM calculations WHERE username = ? ORDER BY calculation_timestamp DESC", (username,))
    records = cursor.fetchall()
    conn.close()

    if not records:
        print(f"\n📭 No records found for user '{username}'.")
        return

    print("\n" + "=" * 100)
    print(f"   RECORDS FOR USER: {username}")
    print("=" * 100)
    print(f"{'ID':<5} {'Specimen Size':<15} {'Microscope':<35} {'Real Size':<20} {'Timestamp'}")
    print("-" * 100)

    for record in records:
        rid, _, spec_size, spec_unit, mic_type, mag, real_size, real_unit, timestamp = record
        print(f"{rid:<5} {spec_size:>8.4f} {spec_unit:<5} {mic_type:<35} {real_size:>10.6f} {real_unit:<8} {timestamp}")

    print("=" * 100)
    print(f"Total records for {username}: {len(records)}")


def delete_record(record_id):
    """Delete a specific record by ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM calculations WHERE id = ?", (record_id,))

    if cursor.rowcount > 0:
        print(f"✅ Record {record_id} deleted successfully.")
    else:
        print(f"❌ Record {record_id} not found.")

    conn.commit()
    conn.close()


def clear_all_records():
    """Clear all records from the database (with confirmation)."""
    confirm = input("⚠️  Are you sure you want to delete ALL records? This cannot be undone. (yes/no): ").strip().lower()
    if confirm in ('yes', 'y'):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM calculations")
        conn.commit()
        conn.close()
        print("✅ All records have been cleared.")
    else:
        print("❎ Operation cancelled.")


def display_microscope_menu():
    """Display the microscope selection menu."""
    print("\n" + "=" * 60)
    print("AVAILABLE MICROSCOPE TYPES")
    print("=" * 60)
    for i, (name, mag) in enumerate(MICROSCOPES.items(), 1):
        print(f"  {i:2}. {name:<45} (×{mag:,})")
    print("=" * 60)


def display_unit_menu():
    """Display the output unit selection menu."""
    print("\n" + "=" * 40)
    print("AVAILABLE OUTPUT UNITS")
    print("=" * 40)
    for i, unit in enumerate(OUTPUT_UNITS, 1):
        print(f"  {i}. {unit}")
    print("=" * 40)


def get_microscope_choice():
    """Get valid microscope choice from user."""
    while True:
        try:
            choice = int(input("\nEnter the number of the microscope type: "))
            if 1 <= choice <= len(MICROSCOPES):
                return list(MICROSCOPES.keys())[choice - 1]
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(MICROSCOPES)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_unit_choice():
    """Get valid output unit choice from user."""
    while True:
        try:
            choice = int(input("\nEnter the number of the output unit: "))
            if 1 <= choice <= len(OUTPUT_UNITS):
                return OUTPUT_UNITS[choice - 1]
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(OUTPUT_UNITS)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_measured_size():
    """Get valid measured size from user."""
    while True:
        try:
            size = float(input("\nEnter the measured size (in mm) from the microscope image: "))
            if size > 0:
                return size
            else:
                print("Size must be greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def calculate_real_size(measured_size_mm, microscope_type, output_unit):
    """Calculate the real-world size of a specimen."""
    magnification = MICROSCOPES[microscope_type]
    real_size_mm = measured_size_mm / magnification
    conversion_factor = UNIT_CONVERSIONS[output_unit]
    real_size_output = real_size_mm / conversion_factor

    breakdown = f"""
╔══════════════════════════════════════════════════════════════════════╗
║                    CALCULATION BREAKDOWN                             ║
╠══════════════════════════════════════════════════════════════════════╣
║  Microscope Type:     {microscope_type:<45} ║
║  Magnification:       ×{magnification:>50,} ║
║                                                                      ║
║  FORMULA:                                                            ║
║    Real Size = Measured Size (mm) ÷ Magnification Factor            ║
║                                                                      ║
║  STEP-BY-STEP:                                                       ║
║    1. Measured Size (from image) = {measured_size_mm:>10.6f} mm          ║
║    2. Magnification Factor       = ×{magnification:>10,}                ║
║    3. Real Size (in mm)          = {measured_size_mm:.6f} ÷ {magnification}    ║
║                                    = {real_size_mm:.10f} mm             ║
║    4. Convert to {output_unit:<5}        = {real_size_mm:.10f} ÷ {conversion_factor}  ║
║                                    = {real_size_output:.10f} {output_unit}        ║
╚══════════════════════════════════════════════════════════════════════╝
"""

    return real_size_output, magnification, breakdown


def perform_calculation():
    """Perform a new calculation and save to database."""
    print("\n" + "─" * 60)
    print("   NEW CALCULATION")
    print("─" * 60)

    # Get username
    username = input("\nEnter your username: ").strip()
    if not username:
        print("❌ Username cannot be empty.")
        return

    # Display microscope menu and get choice
    display_microscope_menu()
    microscope_type = get_microscope_choice()

    # Get measured size
    measured_size = get_measured_size()

    # Display unit menu and get choice
    display_unit_menu()
    output_unit = get_unit_choice()

    # Perform calculation
    real_size, magnification, breakdown = calculate_real_size(
        measured_size, microscope_type, output_unit
    )

    # Save to database
    record_id = save_calculation(
        username, measured_size, "mm", microscope_type, 
        magnification, real_size, output_unit
    )

    # Display results
    print("\n" + "=" * 70)
    print("   RESULT")
    print("=" * 70)
    print(f"\n   Real Size: {real_size:,.6f} {output_unit}")
    print(f"   Record saved to database with ID: {record_id}")
    print(breakdown)


def manage_records():
    """Menu for managing database records."""
    while True:
        print("\n" + "=" * 50)
        print("   RECORD MANAGEMENT")
        print("=" * 50)
        print("  1. View all records")
        print("  2. View records by user")
        print("  3. Delete a specific record")
        print("  4. Clear all records")
        print("  5. Back to main menu")
        print("=" * 50)

        try:
            choice = int(input("\nEnter your choice: "))

            if choice == 1:
                view_all_records()
            elif choice == 2:
                username = input("Enter username to search: ").strip()
                view_records_by_user(username)
            elif choice == 3:
                try:
                    record_id = int(input("Enter the record ID to delete: "))
                    delete_record(record_id)
                except ValueError:
                    print("❌ Invalid record ID.")
            elif choice == 4:
                clear_all_records()
            elif choice == 5:
                break
            else:
                print("❌ Invalid choice.")
        except ValueError:
            print("❌ Invalid input.")


def main():
    """Main function for the database-integrated program."""
    init_database()

    print("=" * 70)
    print("   MICROSCOPE SPECIMEN SIZE CALCULATOR - Phase (b)")
    print("   CSC 442 - Computational Biology & Interdisciplinary Studies")
    print("=" * 70)
    print("\nThis program calculates specimen sizes and stores results")
    print("in a SQLite database for future reference.")

    while True:
        print("\n" + "=" * 50)
        print("   MAIN MENU")
        print("=" * 50)
        print("  1. Perform new calculation")
        print("  2. Manage saved records")
        print("  3. Exit")
        print("=" * 50)

        try:
            choice = int(input("\nEnter your choice: "))

            if choice == 1:
                perform_calculation()
            elif choice == 2:
                manage_records()
            elif choice == 3:
                print("\nThank you for using the Microscope Specimen Size Calculator!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()
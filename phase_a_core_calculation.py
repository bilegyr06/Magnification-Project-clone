"""
Phase (a) - Core Calculation Program
Microscope Specimen Size Calculator
CSC 442 - Computational Biology & Interdisciplinary Studies
"""

import sys

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

# ==========================================
# UNIT CONVERSION FACTORS (to mm)
# ==========================================
UNIT_CONVERSIONS = {
    "nm": 1e-6,      # nanometers to mm
    "µm": 1e-3,      # micrometers to mm
    "mm": 1.0,       # millimeters
    "cm": 10.0,      # centimeters to mm
    "m": 1000.0,     # meters to mm
}

OUTPUT_UNITS = ["nm", "µm", "mm", "cm", "m"]


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
    """
    Calculate the real-world size of a specimen.

    Formula: Real Size = Measured Size (mm) ÷ Magnification Factor

    Args:
        measured_size_mm: The size measured from the microscope image (in mm)
        microscope_type: The type of microscope used
        output_unit: The unit to display the result in

    Returns:
        tuple: (real_size_in_output_unit, magnification_factor, formula_breakdown)
    """
    magnification = MICROSCOPES[microscope_type]
    real_size_mm = measured_size_mm / magnification

    # Convert to desired output unit
    conversion_factor = UNIT_CONVERSIONS[output_unit]
    real_size_output = real_size_mm / conversion_factor

    # Build formula breakdown
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


def main():
    """Main function for the core calculation program."""
    print("=" * 70)
    print("   MICROSCOPE SPECIMEN SIZE CALCULATOR - Phase (a)")
    print("   CSC 442 - Computational Biology & Interdisciplinary Studies")
    print("=" * 70)
    print("\nThis program calculates the real-world size of a specimen")
    print("based on its measured size from a microscope image.")

    while True:
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

        # Display results
        print("\n" + "=" * 70)
        print("   RESULT")
        print("=" * 70)
        print(f"\n   Real Size: {real_size:,.6f} {output_unit}")
        print(breakdown)

        # Ask to continue
        again = input("\nWould you like to perform another calculation? (yes/no): ").strip().lower()
        if again not in ('yes', 'y'):
            print("\nThank you for using the Microscope Specimen Size Calculator!")
            break


if __name__ == "__main__":
    main()
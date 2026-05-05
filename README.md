# 🔬 Microscope Specimen Size Calculator

**CSC 442 — Computational Biology & Interdisciplinary Studies**
Faculty of Physical Sciences, Department of Computer Science
2024/2025 Second Semester

## Project Overview

A progressive web application that calculates the real-world size of microscope specimens using the formula:

```
Real Size = Measured Size (mm) ÷ Magnification Factor
```

## Five Development Phases

### Phase (a) — Core Calculation Program
- Command-line Python program
- Microscope type selection with predefined magnification factors
- Unit conversion (nm, µm, mm, cm, m)
- Step-by-step calculation breakdown

**Run:** `python phase_a_core_calculation.py`

### Phase (b) — Database Integration
- SQLite database to store calculation history
- Records username, specimen size, microscope type, and real size
- View, filter, and delete records

**Run:** `python phase_b_database.py`

### Phase (c) — Python-Based GUI
- Tkinter graphical user interface
- Image upload with preview
- Dropdown selections for microscope type and output unit
- Tabbed interface: Calculator & History

**Run:** `python phase_c_python_gui.py`
*Requires: `pip install Pillow`*

### Phase (d) — Web-Based GUI
- Flask web application with modern responsive UI
- All features from phases (a)-(c) accessible via browser
- Drag & drop image upload
- Real-time calculation with AJAX
- Full history management

**Run:**
```bash
pip install -r requirements.txt
python app.py
```
Then open `http://localhost:5000` in your browser.

### Phase (e) — Free Hosting
Deploy to a free hosting platform:

**Option 1: Render**
1. Push code to GitHub
2. Connect repository to [render.com](https://render.com)
3. Use "Web Service" with build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`

**Option 2: Railway**
1. Push code to GitHub
2. Deploy from [railway.app](https://railway.app)
3. Add environment variable: `PORT=5000`

**Option 3: PythonAnywhere**
1. Upload files to [pythonanywhere.com](https://pythonanywhere.com)
2. Configure WSGI to point to `app.py`
3. Reload web app

## Microscope Types & Magnification Factors

| Microscope | Magnification |
|------------|--------------|
| Compound Light (Low Power) | ×40 |
| Compound Light (Medium Power) | ×100 |
| Compound Light (High Power) | ×400 |
| Compound Light (Oil Immersion) | ×1,000 |
| Stereo Microscope (Low) | ×10 |
| Stereo Microscope (Medium) | ×20 |
| Stereo Microscope (High) | ×40 |
| Scanning Electron Microscope (SEM) | ×10,000 |
| Transmission Electron Microscope (TEM) | ×50,000 |
| Fluorescence Microscope | ×400 |
| Confocal Microscope | ×400 |
| Atomic Force Microscope (AFM) | ×1,000,000 |

## File Structure

```
project1/
├── phase_a_core_calculation.py    # Phase (a) - CLI program
├── phase_b_database.py            # Phase (b) - Database version
├── phase_c_python_gui.py          # Phase (c) - Tkinter GUI
├── app.py                         # Phase (d) - Flask web app
├── requirements.txt               # Python dependencies
├── Procfile                       # Heroku/Render config
├── specimen_calculations.db       # SQLite database (auto-created)
├── static/
│   ├── css/style.css              # Stylesheet
│   ├── js/app.js                  # Frontend JavaScript
│   └── uploads/                   # Uploaded images
└── templates/
    ├── index.html                 # Calculator page
    └── history.html               # History page
```

## Marking Scheme Compliance

| Component | Marks | Status |
|-----------|-------|--------|
| (a) Core Calculation | 20 | ✅ Formula, dropdowns, unit conversion, breakdown, validation |
| (b) Database | 15 | ✅ SQLite storage, username/specimen/real size, view/manage records |
| (c) Python GUI | 20 | ✅ Tkinter GUI, image upload/preview, dropdowns, result display, history |
| (d) Web GUI | 25 | ✅ Full web interface, Python GUI files retained |
| (e) Hosting | 15 | ✅ Deployable to free platforms |
| Code Quality | 5 | ✅ Clean structure, comments, readable code |
| **TOTAL** | **100** | |

## Author
Individual Assignment — CSC 442, 400 Level

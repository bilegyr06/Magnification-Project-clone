/* ==========================================
   Microscope Specimen Size Calculator
   CSC 442 - Web GUI JavaScript
   ========================================== */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('calcForm');
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('specimen_image');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const removeImageBtn = document.getElementById('removeImage');
    const resultContainer = document.getElementById('resultContainer');
    const resultDetails = document.getElementById('resultDetails');
    const microscopeTypeGroup = document.getElementById('microscopeTypeGroup');
    const customMagnificationGroup = document.getElementById('customMagnificationGroup');
    const microscopeTypeInput = document.getElementById('microscope_type');
    const customMagnificationInput = document.getElementById('custom_magnification');
    const magnificationSourceInputs = document.querySelectorAll('input[name="magnification_source"]');

    // File upload via click
    uploadZone.addEventListener('click', () => fileInput.click());

    // File upload via drag & drop
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            showPreview(files[0]);
        }
    });

    // File input change
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            showPreview(fileInput.files[0]);
        }
    });

    // Remove image
    removeImageBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.value = '';
        imagePreview.style.display = 'none';
        uploadZone.style.display = 'block';
    });

    function showPreview(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file.');
            return;
        }
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            uploadZone.style.display = 'none';
            imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }

    function updateMagnificationInputMode() {
        const source = document.querySelector('input[name="magnification_source"]:checked').value;
        const useMicroscopeType = source === 'microscope_type';

        microscopeTypeGroup.style.display = useMicroscopeType ? 'block' : 'none';
        customMagnificationGroup.style.display = useMicroscopeType ? 'none' : 'block';
        microscopeTypeInput.required = useMicroscopeType;
        customMagnificationInput.required = !useMicroscopeType;

        if (useMicroscopeType) {
            customMagnificationInput.value = '';
        } else {
            microscopeTypeInput.value = '';
        }
    }

    magnificationSourceInputs.forEach((input) => {
        input.addEventListener('change', updateMagnificationInputMode);
    });
    updateMagnificationInputMode();

    // Form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const username = document.getElementById('username').value.trim();
        const measuredSize = parseFloat(document.getElementById('measured_size').value);
        const magnificationSource = document.querySelector('input[name="magnification_source"]:checked').value;
        const microscopeType = document.getElementById('microscope_type').value;
        const customMagnification = parseFloat(document.getElementById('custom_magnification').value);
        const outputUnit = document.getElementById('output_unit').value;

        // Validation
        if (!username) {
            showError('Please enter your username.');
            return;
        }
        if (!measuredSize || measuredSize <= 0) {
            showError('Please enter a valid measured size greater than zero.');
            return;
        }
        if (magnificationSource === 'microscope_type' && !microscopeType) {
            showError('Please select a microscope type.');
            return;
        }
        if (magnificationSource === 'custom_magnification' && (!customMagnification || customMagnification <= 0)) {
            showError('Please enter a valid magnification greater than zero.');
            return;
        }

        // Show loading
        showLoading();

        const formData = new FormData(form);

        try {
            const response = await fetch('/calculate', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok || data.error) {
                showError(data.error || 'An error occurred during calculation.');
                return;
            }

            showResult(data);
        } catch (err) {
            showError('Network error. Please try again.');
            console.error(err);
        }
    });

    function showLoading() {
        resultContainer.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>Calculating...</p>
            </div>
        `;
        resultDetails.style.display = 'none';
    }

    function showError(message) {
        resultContainer.innerHTML = `
            <div class="error-message">
                <strong>⚠️ Error:</strong> ${message}
            </div>
            <div class="result-placeholder">
                <span class="placeholder-icon">🔬</span>
                <p>Enter details and click Calculate to see results</p>
            </div>
        `;
        resultDetails.style.display = 'none';
    }

    function showResult(data) {
        const bd = data.breakdown;
        const formattedMag = data.magnification_formatted || data.magnification.toLocaleString();

        resultContainer.innerHTML = '';
        resultDetails.style.display = 'block';

        document.getElementById('resultValue').textContent = parseFloat(data.real_size_formatted).toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 6
        });
        document.getElementById('resultUnit').textContent = data.unit;

        const stepsHtml = `
            <div class="step">
                <span class="step-label">Measured Size (from image)</span>
                <span class="step-value">${bd.measured_size} mm</span>
            </div>
            <div class="step">
                <span class="step-label">Magnification Factor</span>
                <span class="step-value">×${formattedMag}</span>
            </div>
            <div class="step">
                <span class="step-label">Real Size (in mm)</span>
                <span class="step-value">${bd.measured_size} ÷ ${data.magnification} = ${bd.real_size_mm.toExponential(4)} mm</span>
            </div>
            <div class="step">
                <span class="step-label">Convert to ${data.unit}</span>
                <span class="step-value">${bd.real_size_mm.toExponential(4)} ÷ ${bd.conversion_factor} = ${bd.real_size_output.toExponential(4)} ${data.unit}</span>
            </div>
        `;

        document.getElementById('breakdownSteps').innerHTML = stepsHtml;

        // Success notification
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.innerHTML = `<strong>✅ Success!</strong> Record saved with ID #${data.record_id}`;
        resultContainer.appendChild(successDiv);
    }
});

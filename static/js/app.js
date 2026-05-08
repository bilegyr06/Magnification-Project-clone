// ==================== MAIN APP JS - Magnification Project Redesign ====================

document.addEventListener('DOMContentLoaded', () => {
    // ====================== DOM ELEMENTS ======================
    const form = document.getElementById('calcForm');
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('specimen_image');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const magnifierLens = document.getElementById('magnifierLens');
    const removeImageBtn = document.getElementById('removeImage');

    const microscopeTypeGroup = document.getElementById('microscopeTypeGroup');
    const customMagnificationGroup = document.getElementById('customMagnificationGroup');

    const radioButtons = document.querySelectorAll('input[name="magnification_source"]');

    // ====================== DRAG & DROP + UPLOAD ======================
    uploadZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleImageUpload(e.target.files[0]);
        }
    });

    // Drag & Drop handlers
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.style.borderColor = '#60a5fa';
        uploadZone.style.background = 'rgba(96, 165, 250, 0.15)';
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.style.borderColor = '#64748b';
        uploadZone.style.background = 'rgba(15, 23, 42, 0.4)';
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.style.borderColor = '#64748b';
        uploadZone.style.background = 'rgba(15, 23, 42, 0.4)';
        
        if (e.dataTransfer.files.length > 0) {
            handleImageUpload(e.dataTransfer.files[0]);
        }
    });

    function handleImageUpload(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file (PNG, JPG, GIF)');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            imagePreview.style.display = 'block';
            uploadZone.style.display = 'none';
        };
        reader.readAsDataURL(file);
    }

    // Remove image
    removeImageBtn.addEventListener('click', () => {
        previewImg.src = '';
        imagePreview.style.display = 'none';
        uploadZone.style.display = 'block';
        fileInput.value = '';   // important: reset input
    });

    // ====================== MAGNIFIER LENS LOGIC ======================
    let isMagnifying = false;

    function initMagnifier() {
        const wrapper = previewImg.parentElement;

        wrapper.addEventListener('mouseenter', () => {
            magnifierLens.style.display = 'block';
            isMagnifying = true;
        });

        wrapper.addEventListener('mouseleave', () => {
            magnifierLens.style.display = 'none';
            isMagnifying = false;
        });

        wrapper.addEventListener('mousemove', (e) => {
            if (!isMagnifying) return;

            const rect = wrapper.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Lens position (centered on cursor)
            const lensSize = magnifierLens.offsetWidth;
            let lensX = x - lensSize / 2;
            let lensY = y - lensSize / 2;

            // Keep lens inside image bounds
            lensX = Math.max(0, Math.min(lensX, rect.width - lensSize));
            lensY = Math.max(0, Math.min(lensY, rect.height - lensSize));

            magnifierLens.style.left = `${lensX}px`;
            magnifierLens.style.top = `${lensY}px`;

            // Magnify background (zoom ~ 3x)
            const zoom = 3;
            const bgX = (x / rect.width) * 100;
            const bgY = (y / rect.height) * 100;

            magnifierLens.style.backgroundImage = `url(${previewImg.src})`;
            magnifierLens.style.backgroundPosition = `${bgX}% ${bgY}%`;
            magnifierLens.style.backgroundSize = `${zoom * 100}%`;
        });
    }

    // Initialize magnifier once image is loaded
    previewImg.addEventListener('load', initMagnifier);

    // ====================== RADIO TOGGLE ======================
    radioButtons.forEach(radio => {
        radio.addEventListener('change', () => {
            if (radio.value === 'microscope_type') {
                microscopeTypeGroup.style.display = 'block';
                customMagnificationGroup.style.display = 'none';
            } else {
                microscopeTypeGroup.style.display = 'none';
                customMagnificationGroup.style.display = 'block';
            }
        });
    });

    // ====================== FORM SUBMISSION ======================
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const submitBtn = form.querySelector('.btn-calculate');
        const originalText = submitBtn.textContent;
        
        submitBtn.textContent = 'Calculating...';
        submitBtn.disabled = true;

        // For Flask - you can keep traditional submit or use FormData + fetch
        // Traditional submit (recommended if your Flask route expects POST)
        form.submit();   // Remove this line if you want to use fetch instead

        // Optional: Fetch version (uncomment if you prefer AJAX)
        /*
        const formData = new FormData(form);
        
        try {
            const response = await fetch('/', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.text();
            document.getElementById('resultContainer').innerHTML = result;
        } catch (err) {
            console.error(err);
            alert('Calculation failed. Please try again.');
        } finally {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
        */
    });

    // ====================== RESPONSIVE LENS ADJUSTMENT ======================
    function adjustLensSize() {
        if (window.innerWidth < 600) {
            magnifierLens.style.width = '140px';
            magnifierLens.style.height = '140px';
        } else {
            magnifierLens.style.width = '180px';
            magnifierLens.style.height = '180px';
        }
    }

    window.addEventListener('resize', adjustLensSize);
    adjustLensSize(); // initial call

    // ====================== KEYBOARD SUPPORT ======================
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && imagePreview.style.display !== 'none') {
            removeImageBtn.click();
        }
    });

    console.log('%c✅ MangifiCalc JS loaded successfully - Modern redesign active', 
                'color: #60a5fa; font-weight: bold');
});
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const fileName = document.getElementById('fileName');
const summarySection = document.getElementById('summarySection');
const summaryText = document.getElementById('summaryText');
const loadingSpinner = document.getElementById('loadingSpinner');
const resetBtn = document.getElementById('resetBtn');

// Click to browse
browseBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    fileInput.click();
});

uploadBox.addEventListener('click', () => {
    fileInput.click();
});

// File input change
fileInput.addEventListener('change', (e) => {
    handleFile(e.target.files[0]);
});

// Drag and drop
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('drag-over');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('drag-over');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('drag-over');
    
    const file = e.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
        handleFile(file);
    } else {
        alert('Please upload a PDF file');
    }
});

// Handle file upload and summarization
async function handleFile(file) {
    if (!file) return;
    
    if (file.type !== 'application/pdf') {
        alert('Please upload a PDF file');
        return;
    }
    
    // Show file name
    fileName.textContent = `Selected: ${file.name}`;
    
    // Show summary section and loading spinner
    summarySection.style.display = 'block';
    loadingSpinner.style.display = 'flex';
    summaryText.style.display = 'none';
    summaryText.textContent = '';
    
    // Scroll to summary section
    summarySection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Create form data
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            // Hide spinner, show summary
            loadingSpinner.style.display = 'none';
            summaryText.style.display = 'block';
            summaryText.textContent = data.summary;
        } else {
            throw new Error(data.error || 'Failed to process PDF');
        }
    } catch (error) {
        console.error('Error:', error);
        loadingSpinner.style.display = 'none';
        summaryText.style.display = 'block';
        summaryText.textContent = `Error: ${error.message}. Please try again.`;
        summaryText.style.color = '#EF4444';
    }
}

// Reset button
resetBtn.addEventListener('click', () => {
    fileInput.value = '';
    fileName.textContent = '';
    summarySection.style.display = 'none';
    summaryText.textContent = '';
    summaryText.style.color = '';
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// static/js/preview.js
document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const previewImage = document.getElementById('previewImage');
    const previewPDF = document.getElementById('previewPDF');
    const previewBox = document.getElementById('previewBox');
    const fileName = document.getElementById('fileName');

    if (!file) return;

    previewBox.style.display = 'block';
    fileName.textContent = file.name;

    if (file.type === 'application/pdf') {
        // PDF Preview
        previewImage.style.display = 'none';
        previewPDF.style.display = 'block';
        previewPDF.src = URL.createObjectURL(file);
    } else if (file.type.startsWith('image/')) {
        // Image Preview
        previewPDF.style.display = 'none';
        previewImage.style.display = 'block';
        previewImage.src = URL.createObjectURL(file);
    } else {
        alert('Please upload only JPG, PNG or PDF files');
    }
});

// Init Quill
var quill = new Quill('#editor-container', {
  modules: { toolbar: '#toolbar' },
  theme: 'snow'
});

// Restore saved content if available
const saved = localStorage.getItem('workspaceContent');
if (saved) {
  quill.root.innerHTML = saved;
}

// Autosave every 2s
setInterval(() => {
  localStorage.setItem('workspaceContent', quill.root.innerHTML);
}, 2000);

const spinner = document.getElementById('spinner');

// Spinner helpers
function showSpinner(msg) {
  spinner.textContent = msg;
  spinner.style.display = 'block';
}
function hideSpinner() {
  spinner.style.display = 'none';
}

// Save as TXT
document.getElementById('saveAsTXT').addEventListener('click', () => {
  showSpinner('Exporting TXT...');
  const text = quill.getText();
  const blob = new Blob([text], {type: 'text/plain'});
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'workspace.txt';
  link.click();
  hideSpinner();
});

// Save as Image
document.getElementById('saveAsIMG').addEventListener('click', () => {
  showSpinner('Exporting Image...');
  html2canvas(document.querySelector('#editor-container')).then(canvas => {
    const link = document.createElement('a');
    link.href = canvas.toDataURL('image/png');
    link.download = 'workspace.png';
    link.click();
    hideSpinner();
  });
});

// Save as PDF
document.getElementById('saveAsPDF').addEventListener('click', () => {
  showSpinner('Exporting PDF...');
  const html = quill.root.innerHTML;

  fetch('/workspace/save_document/', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ html: html })
  })
  .then(res => res.blob())
  .then(blob => {
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'workspace.pdf';
    link.click();
    hideSpinner();
  });
});
// Translate Button — auto detect en/ml
document.getElementById('translateBtn').addEventListener('click', () => {
  const text = quill.getText().trim();
  if (!text) return alert('Editor is empty');

  showSpinner('Translating...');
  // Detect language: if Malayalam letters present, translate to English else Malayalam
  const hasMalayalam = /[\u0D00-\u0D7F]/.test(text);
  const src = hasMalayalam ? 'ml' : 'en';
  const dest = hasMalayalam ? 'en' : 'ml';

  fetch('/api/translate/', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({text, src, dest})
  })
  .then(res => res.json())
  .then(data => {
    if (data.translated) quill.root.innerHTML = data.translated;
    else alert('Error translating');
    hideSpinner();
  });
});

// Transliterate Button — phonetic → Malayalam
document.getElementById('transliterateBtn').addEventListener('click', () => {
  const text = quill.getText().trim();
  if (!text) return alert('Editor is empty');

  showSpinner('Transliterating...');
  fetch('/api/transliterate/', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({text})
  })
  .then(res => res.json())
  .then(data => {
    if (data.transliterated) quill.root.innerHTML = data.transliterated;
    else alert('Error transliterating');
    hideSpinner();
  });
});

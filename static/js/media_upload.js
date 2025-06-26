document.addEventListener('DOMContentLoaded', () => {
  const dropArea = document.getElementById('drop-area');
  if (!dropArea) return;
  dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.classList.add('dragover');
  });
  dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('dragover');
  });
  dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    // TODO: implement upload logic
    alert(`${files.length} file(s) dropped`);
  });
});

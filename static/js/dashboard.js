document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('ranking-search');
  const items = document.querySelectorAll('#ranking-list .ranking-item');
  if (!input || !items.length) return;

  input.addEventListener('input', () => {
    const q = input.value.trim().toLowerCase();
    items.forEach((li) => {
      const name = li.dataset.name.toLowerCase();
      li.style.display = name.includes(q) ? '' : 'none';
    });
  });
});

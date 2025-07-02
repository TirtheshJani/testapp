// Simple search form handler for the homepage

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('homepage-search');
  if (!form) return;

  const input = document.getElementById('search-query');
  const button = document.getElementById('search-submit');
  const results = document.getElementById('search-results');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = input.value.trim();
    if (!query) return;

    const original = button.textContent;
    button.textContent = 'Searching…';
    button.disabled = true;

    try {
      const res = await fetch(`/api/athletes/search?q=${encodeURIComponent(query)}`);
      const data = await res.json();
      results.innerHTML = '';
      (data.results || []).forEach((ath) => {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.textContent = ath.user.full_name;
        results.appendChild(li);
      });
    } catch (err) {
      console.error('Search failed', err);
    } finally {
      button.textContent = original;
      button.disabled = false;
    }
  });
});

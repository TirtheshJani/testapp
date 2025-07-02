// Simple search form handler for the homepage

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('homepage-search');
  if (!form) return;

  const input = document.getElementById('search-query');
  const button = document.getElementById('search-submit');
  const results = document.getElementById('search-results');
  const tabs = document.querySelectorAll('#filter-tabs .nav-link');
  const featured = document.getElementById('featured-list');

  async function runSearch(params) {
    const res = await fetch(`/api/athletes/search?${params.toString()}`);
    const data = await res.json();
    return data.results || [];
  }

  async function renderFeatured(filter) {
    if (!featured) return;
    const params = new URLSearchParams();
    if (filter) {
      const f = filter.toLowerCase();
      if (['nba', 'nfl', 'mlb', 'nhl'].includes(f)) {
        params.append('sport', f.toUpperCase());
      } else {
        params.append('filter', f);
      }
    }
    const athletes = await runSearch(params);
    featured.innerHTML = '';
    athletes.forEach((ath) => {
      const li = document.createElement('li');
      li.className = 'list-group-item';
      li.textContent = ath.user.full_name;
      featured.appendChild(li);
    });
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = input.value.trim();
    if (!query) return;

    const original = button.textContent;
    button.textContent = 'Searching…';
    button.disabled = true;

    try {
      const params = new URLSearchParams();
      params.append('q', query);
      const athletes = await runSearch(params);
      results.innerHTML = '';
      athletes.forEach((ath) => {
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

  tabs.forEach((tab) => {
    tab.addEventListener('click', (e) => {
      e.preventDefault();
      tabs.forEach((t) => t.classList.remove('active'));
      tab.classList.add('active');
      renderFeatured(tab.dataset.filter);
    });
  });

  const activeTab = document.querySelector('#filter-tabs .nav-link.active');
  if (activeTab) {
    renderFeatured(activeTab.dataset.filter);
  }
});

// Interactive Features for AI Technical Support Knowledge Search

document.addEventListener('DOMContentLoaded', () => {
    // 1. Fill search input when sample query pills are clicked
    const suggestionPills = document.querySelectorAll('.suggestion-pill');
    const searchInput = document.querySelector('.search-input');
    const searchForm = document.querySelector('.search-form');

    if (suggestionPills && searchInput) {
        suggestionPills.forEach(pill => {
            pill.addEventListener('click', (e) => {
                e.preventDefault();
                const queryText = pill.getAttribute('data-query') || pill.textContent.trim();
                searchInput.value = queryText;
                if (searchForm) {
                    searchForm.submit();
                }
            });
        });
    }

    // 2. Loading Spinner effect on Search Form submission
    if (searchForm) {
        searchForm.addEventListener('submit', () => {
            const btn = searchForm.querySelector('.search-btn');
            if (btn) {
                btn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin-icon"><circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="10"></circle></svg> Searching...`;
                btn.disabled = true;
            }
        });
    }
});

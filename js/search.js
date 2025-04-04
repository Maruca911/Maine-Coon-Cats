document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchOverlay = document.getElementById('search-overlay');
    const searchResults = document.getElementById('search-results');
    const closeSearch = document.getElementById('close-search');

    // Open search overlay
    searchInput.addEventListener('focus', function() {
        searchOverlay.style.display = 'block';
        document.body.style.overflow = 'hidden';
    });

    // Close search overlay
    closeSearch.addEventListener('click', function() {
        searchOverlay.style.display = 'none';
        document.body.style.overflow = 'auto';
    });

    // Handle search input
    searchInput.addEventListener('input', function() {
        const query = this.value.toLowerCase().trim();
        if (query.length < 2) {
            searchResults.innerHTML = '';
            return;
        }

        const results = searchIndex.filter(item => {
            return item.title.toLowerCase().includes(query) ||
                   item.content.toLowerCase().includes(query) ||
                   item.category.toLowerCase().includes(query);
        });

        displayResults(results);
    });

    // Display search results
    function displayResults(results) {
        if (results.length === 0) {
            searchResults.innerHTML = '<div class="no-results">No results found</div>';
            return;
        }

        const html = results.map(item => `
            <div class="search-result-item">
                <h3><a href="${item.url}">${item.title}</a></h3>
                <p class="category">${item.category}</p>
                <p class="excerpt">${item.content}</p>
            </div>
        `).join('');

        searchResults.innerHTML = html;
    }

    // Close search on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            searchOverlay.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });

    // Handle mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }
}); 
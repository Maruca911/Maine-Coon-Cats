document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('.search-input');
    const searchResults = document.querySelector('.search-results');
    const searchOverlay = document.querySelector('.search-overlay');
    const closeSearch = document.querySelector('.close-search');

    // Show search overlay when clicking search button or pressing enter
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        searchOverlay.classList.add('active');
        searchInput.focus();
        performSearch(searchInput.value);
    });

    // Close search overlay
    closeSearch.addEventListener('click', function() {
        searchOverlay.classList.remove('active');
    });

    // Handle search input changes in overlay
    searchOverlay.querySelector('.search-input').addEventListener('input', function() {
        performSearch(this.value);
    });

    // Close search on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && searchOverlay.classList.contains('active')) {
            searchOverlay.classList.remove('active');
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

    if (searchInput && searchResults) {
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            if (query.length < 2) {
                searchResults.style.display = 'none';
                return;
            }
            
            // Basic search functionality
            const results = window.searchIndex.filter(item => 
                item.title.toLowerCase().includes(query) || 
                item.content.toLowerCase().includes(query)
            );
            
            displayResults(results);
        });
    }

    function performSearch(query) {
        if (!query.trim()) {
            searchResults.innerHTML = `
                <div class="search-suggestions">
                    <h3>Popular Searches</h3>
                    <div class="suggestion-tags">
                        <span>cat food</span>
                        <span>grooming tips</span>
                        <span>behavior guide</span>
                        <span>health care</span>
                        <span>dental care</span>
                    </div>
                </div>
            `;
            return;
        }

        const searchTerm = query.toLowerCase();
        const results = searchIndex.filter(post => {
            // Check title
            if (post.title.toLowerCase().includes(searchTerm)) return true;
            
            // Check excerpt
            if (post.excerpt.toLowerCase().includes(searchTerm)) return true;
            
            // Check keywords with fuzzy matching
            return post.keywords.some(keyword => {
                // Exact match
                if (keyword.toLowerCase().includes(searchTerm)) return true;
                
                // Fuzzy match (words in any order)
                const searchWords = searchTerm.split(' ');
                const keywordWords = keyword.toLowerCase().split(' ');
                return searchWords.every(word => 
                    keywordWords.some(kw => kw.includes(word))
                );
            });
        });

        displayResults(results, searchTerm);
    }

    function displayResults(results, searchTerm) {
        if (results.length === 0) {
            searchResults.innerHTML = `
                <div class="no-results">
                    <p>No results found for "${searchTerm}". Try these suggestions:</p>
                    <div class="suggestion-tags">
                        <span>cat food</span>
                        <span>grooming tips</span>
                        <span>behavior guide</span>
                        <span>health care</span>
                        <span>dental care</span>
                    </div>
                </div>
            `;
            return;
        }

        const resultsHTML = results.map(post => {
            // Highlight matching terms in title and excerpt
            const highlightedTitle = highlightText(post.title, searchTerm);
            const highlightedExcerpt = highlightText(post.excerpt, searchTerm);
            
            // Get matching keywords
            const matchingKeywords = post.keywords.filter(keyword => 
                keyword.toLowerCase().includes(searchTerm)
            );

            return `
                <div class="search-result-item">
                    <h3><a href="${post.url}">${highlightedTitle}</a></h3>
                    <p>${highlightedExcerpt}</p>
                    <div class="result-meta">
                        <span class="category">${post.category}</span>
                        ${matchingKeywords.length > 0 ? 
                            `<span class="matching-keywords">Related: ${matchingKeywords.join(', ')}</span>` : 
                            ''}
                    </div>
                </div>
            `;
        }).join('');

        searchResults.innerHTML = resultsHTML;
    }

    function highlightText(text, searchTerm) {
        if (!searchTerm) return text;
        const regex = new RegExp(`(${searchTerm})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
}); 
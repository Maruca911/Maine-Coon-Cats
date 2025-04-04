// Reading Progress
document.addEventListener('DOMContentLoaded', () => {
    const progressBar = document.querySelector('.progress-bar');
    const saveButton = document.querySelector('.save-for-later');
    
    // Update reading progress
    window.addEventListener('scroll', () => {
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight - windowHeight;
        const scrolled = window.scrollY;
        const progress = (scrolled / documentHeight) * 100;
        progressBar.style.width = `${progress}%`;
    });

    // Save for Later functionality
    if (saveButton) {
        const savedArticles = JSON.parse(localStorage.getItem('savedArticles') || '[]');
        const currentArticle = {
            title: document.title,
            url: window.location.href,
            date: new Date().toISOString()
        };

        // Check if article is already saved
        if (savedArticles.some(article => article.url === currentArticle.url)) {
            saveButton.classList.add('saved');
            saveButton.querySelector('span').textContent = 'Saved';
        }

        saveButton.addEventListener('click', () => {
            const index = savedArticles.findIndex(article => article.url === currentArticle.url);
            
            if (index === -1) {
                savedArticles.push(currentArticle);
                saveButton.classList.add('saved');
                saveButton.querySelector('span').textContent = 'Saved';
            } else {
                savedArticles.splice(index, 1);
                saveButton.classList.remove('saved');
                saveButton.querySelector('span').textContent = 'Save';
            }

            localStorage.setItem('savedArticles', JSON.stringify(savedArticles));
        });
    }

    // Newsletter form submission
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = newsletterForm.querySelector('input[type="email"]').value;
            
            try {
                const response = await fetch('/subscribe', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email })
                });

                if (response.ok) {
                    alert('Thank you for subscribing!');
                    newsletterForm.reset();
                } else {
                    throw new Error('Subscription failed');
                }
            } catch (error) {
                alert('Sorry, there was an error. Please try again later.');
            }
        });
    }
});

// Blog functionality
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }

    // Newsletter form handling
    const newsletterForm = document.getElementById('mc-embedded-subscribe-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Add newsletter subscription logic here
            alert('Thank you for subscribing!');
            this.reset();
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Lazy loading for images
    const lazyImages = document.querySelectorAll('img[loading="lazy"]');
    if ('loading' in HTMLImageElement.prototype) {
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
        });
    } else {
        // Fallback for browsers that don't support lazy loading
        const lazyLoadScript = document.createElement('script');
        lazyLoadScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/lazysizes/5.2.2/lazysizes.min.js';
        document.body.appendChild(lazyLoadScript);
    }

    // Table of contents generation
    const generateTableOfContents = () => {
        const content = document.querySelector('.blog-post-content');
        const headings = content.querySelectorAll('h2, h3');
        const toc = document.createElement('div');
        toc.className = 'table-of-contents';
        
        if (headings.length > 0) {
            toc.innerHTML = '<h3>Table of Contents</h3><ul>';
            headings.forEach((heading, index) => {
                const id = `heading-${index}`;
                heading.id = id;
                const level = heading.tagName.toLowerCase();
                const text = heading.textContent;
                toc.innerHTML += `<li class="${level}"><a href="#${id}">${text}</a></li>`;
            });
            toc.innerHTML += '</ul>';
            content.insertBefore(toc, content.firstChild);
        }
    };

    generateTableOfContents();
}); 
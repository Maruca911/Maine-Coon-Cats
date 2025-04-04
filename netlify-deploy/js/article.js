// Article Page Functionality
document.addEventListener('DOMContentLoaded', () => {
    // Back to Top Button
    const backToTopButton = document.getElementById('backToTop');
    if (backToTopButton) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('visible');
            } else {
                backToTopButton.classList.remove('visible');
            }
        });

        backToTopButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            // Close all FAQ items
            faqItems.forEach(faq => {
                faq.classList.remove('active');
            });

            // Open clicked item if it wasn't active
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });

    // Smooth Scroll for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 80; // Adjust based on your header height
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Intersection Observer for Animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observe sections and cards
    document.querySelectorAll('.recipe-section, .recipe-card, .tip-item').forEach(element => {
        observer.observe(element);
    });

    // Newsletter Form
    const newsletterForm = document.getElementById('newsletterForm');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = newsletterForm.querySelector('input[type="email"]').value;
            
            // Add loading state
            const submitButton = newsletterForm.querySelector('button');
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Subscribing...';
            submitButton.disabled = true;

            // Simulate API call
            setTimeout(() => {
                // Show success message
                const message = document.createElement('div');
                message.className = 'form-message success';
                message.textContent = 'Thank you for subscribing!';
                newsletterForm.appendChild(message);

                // Reset form
                newsletterForm.reset();
                submitButton.textContent = originalText;
                submitButton.disabled = false;

                // Remove message after 5 seconds
                setTimeout(() => {
                    message.remove();
                }, 5000);
            }, 1500);
        });
    }

    // Print Functionality
    const printButton = document.querySelector('.print-button');
    if (printButton) {
        printButton.addEventListener('click', () => {
            window.print();
        });
    }

    // Save for Later Functionality
    const saveButton = document.querySelector('.save-button');
    if (saveButton) {
        saveButton.addEventListener('click', () => {
            const articleData = {
                title: document.title,
                url: window.location.href,
                date: new Date().toISOString()
            };

            // Get saved articles
            let savedArticles = JSON.parse(localStorage.getItem('savedArticles') || '[]');
            
            // Check if article is already saved
            const isSaved = savedArticles.some(article => article.url === articleData.url);
            
            if (isSaved) {
                // Remove from saved articles
                savedArticles = savedArticles.filter(article => article.url !== articleData.url);
                saveButton.classList.remove('saved');
                saveButton.querySelector('span').textContent = 'Save for Later';
            } else {
                // Add to saved articles
                savedArticles.push(articleData);
                saveButton.classList.add('saved');
                saveButton.querySelector('span').textContent = 'Saved!';
            }

            // Save to localStorage
            localStorage.setItem('savedArticles', JSON.stringify(savedArticles));

            // Reset button state after 2 seconds
            setTimeout(() => {
                saveButton.classList.remove('saved');
                saveButton.querySelector('span').textContent = 'Save for Later';
            }, 2000);
        });
    }
}); 
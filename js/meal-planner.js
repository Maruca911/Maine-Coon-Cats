document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.meal-planner-form');
    const submitButton = form.querySelector('.submit-button');
    const originalButtonText = submitButton.textContent;
    const previewSection = document.querySelector('.meal-plan-preview');
    const previewContent = document.querySelector('.preview-content');

    // Update preview when form inputs change
    form.addEventListener('input', updatePreview);
    form.addEventListener('change', updatePreview);

    function updatePreview() {
        const formData = new FormData(form);
        const catName = formData.get('cat-name') || 'Your Cat';
        const catAge = formData.get('cat-age') || '0';
        const catWeight = formData.get('cat-weight') || '0';
        const activityLevel = formData.get('activity-level') || 'moderate';
        const numRecipes = formData.get('preferred-recipes') || '3';

        // Calculate daily calories (same as server-side calculation)
        const caloriesPerPound = {
            'sedentary': 20,
            'moderate': 25,
            'active': 30,
            'very-active': 35
        };
        const dailyCalories = Math.round(catWeight * caloriesPerPound[activityLevel]);

        // Update preview content
        previewContent.innerHTML = `
            <div class="preview-item">
                <h4>Cat Information</h4>
                <p>Name: ${catName}</p>
                <p>Age: ${catAge} years</p>
                <p>Weight: ${catWeight} lbs</p>
                <p>Activity Level: ${activityLevel.replace('-', ' ').title()}</p>
                <p>Daily Calories: ${dailyCalories}</p>
            </div>
            <div class="preview-item">
                <h4>Meal Schedule</h4>
                <p>3 meals per day</p>
                <p>${Math.round(dailyCalories/3)} calories per meal</p>
                <p>Meal times: 8:00, 14:00, 20:00</p>
            </div>
            <div class="preview-item">
                <h4>Recipe Collection</h4>
                <p>${numRecipes} personalized recipes</p>
                <p>Detailed instructions</p>
                <p>Nutritional information</p>
            </div>
            <div class="preview-item">
                <h4>Shopping List</h4>
                <p>Complete ingredient list</p>
                <p>Quantities for ${numRecipes} recipes</p>
                <p>Supplement recommendations</p>
            </div>
        `;

        // Show/hide preview based on form completion
        if (catName && catAge && catWeight) {
            previewSection.style.display = 'block';
        } else {
            previewSection.style.display = 'none';
        }
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Disable submit button and show loading state
        submitButton.disabled = true;
        submitButton.textContent = 'Generating Meal Plan...';
        
        try {
            const formData = new FormData(form);
            
            const response = await fetch('/generate-meal-plan', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Show success message
                showMessage('success', 'Your meal plan has been generated and sent to your email!');
                form.reset();
                previewSection.style.display = 'none';
            } else {
                // Show error message
                showMessage('error', result.message || 'An error occurred. Please try again.');
            }
        } catch (error) {
            showMessage('error', 'An error occurred. Please try again.');
            console.error('Error:', error);
        } finally {
            // Re-enable submit button and restore original text
            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
        }
    });
});

function showMessage(type, message) {
    // Remove any existing messages
    const existingMessage = document.querySelector('.form-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create new message element
    const messageElement = document.createElement('div');
    messageElement.className = `form-message ${type}`;
    messageElement.textContent = message;
    
    // Insert message after the form
    const form = document.querySelector('.meal-planner-form');
    form.parentNode.insertBefore(messageElement, form.nextSibling);
    
    // Remove message after 5 seconds
    setTimeout(() => {
        messageElement.remove();
    }, 5000);
}

// Add form validation
document.querySelectorAll('.meal-planner-form input, .meal-planner-form select').forEach(input => {
    input.addEventListener('invalid', function(e) {
        e.preventDefault();
        this.classList.add('invalid');
    });
    
    input.addEventListener('input', function() {
        if (this.classList.contains('invalid')) {
            this.classList.remove('invalid');
        }
    });
}); 
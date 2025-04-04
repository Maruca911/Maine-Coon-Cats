// Cookie Consent Banner
document.addEventListener('DOMContentLoaded', function() {
    const cookieBanner = document.createElement('div');
    cookieBanner.id = 'cookie-consent-banner';
    cookieBanner.innerHTML = `
        <div class="cookie-content">
            <p>We use cookies to enhance your browsing experience, serve personalized content, and analyze our traffic. By clicking "Accept All", you consent to our use of cookies.</p>
            <div class="cookie-buttons">
                <button id="accept-all-cookies" class="cookie-button accept">Accept All</button>
                <button id="reject-cookies" class="cookie-button reject">Reject</button>
                <button id="cookie-settings" class="cookie-button settings">Cookie Settings</button>
            </div>
        </div>
    `;
    document.body.appendChild(cookieBanner);

    // Cookie Settings Modal
    const cookieModal = document.createElement('div');
    cookieModal.id = 'cookie-settings-modal';
    cookieModal.innerHTML = `
        <div class="modal-content">
            <h2>Cookie Settings</h2>
            <div class="cookie-options">
                <div class="cookie-option">
                    <input type="checkbox" id="analytics-cookies" checked disabled>
                    <label for="analytics-cookies">Analytics Cookies</label>
                    <p>These cookies help us understand how visitors interact with our website.</p>
                </div>
                <div class="cookie-option">
                    <input type="checkbox" id="functional-cookies" checked>
                    <label for="functional-cookies">Functional Cookies</label>
                    <p>These cookies enable the website to provide enhanced functionality.</p>
                </div>
                <div class="cookie-option">
                    <input type="checkbox" id="marketing-cookies">
                    <label for="marketing-cookies">Marketing Cookies</label>
                    <p>These cookies are used to track visitors across websites.</p>
                </div>
            </div>
            <div class="modal-buttons">
                <button id="save-cookie-settings" class="cookie-button accept">Save Settings</button>
                <button id="close-cookie-settings" class="cookie-button reject">Close</button>
            </div>
        </div>
    `;
    document.body.appendChild(cookieModal);

    // Event Listeners
    document.getElementById('accept-all-cookies').addEventListener('click', () => {
        setCookieConsent(true, true, true);
        hideBanner();
    });

    document.getElementById('reject-cookies').addEventListener('click', () => {
        setCookieConsent(false, false, false);
        hideBanner();
    });

    document.getElementById('cookie-settings').addEventListener('click', () => {
        document.getElementById('cookie-settings-modal').style.display = 'block';
    });

    document.getElementById('save-cookie-settings').addEventListener('click', () => {
        const analytics = document.getElementById('analytics-cookies').checked;
        const functional = document.getElementById('functional-cookies').checked;
        const marketing = document.getElementById('marketing-cookies').checked;
        setCookieConsent(analytics, functional, marketing);
        hideBanner();
        document.getElementById('cookie-settings-modal').style.display = 'none';
    });

    document.getElementById('close-cookie-settings').addEventListener('click', () => {
        document.getElementById('cookie-settings-modal').style.display = 'none';
    });

    // Check if user has already made a choice
    if (!getCookie('cookie_consent')) {
        cookieBanner.style.display = 'block';
    }

    function setCookieConsent(analytics, functional, marketing) {
        const consent = {
            analytics: analytics,
            functional: functional,
            marketing: marketing,
            timestamp: new Date().getTime()
        };
        setCookie('cookie_consent', JSON.stringify(consent), 365);
    }

    function hideBanner() {
        document.getElementById('cookie-consent-banner').style.display = 'none';
    }

    function setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = "expires=" + date.toUTCString();
        document.cookie = name + "=" + value + ";" + expires + ";path=/";
    }

    function getCookie(name) {
        const value = "; " + document.cookie;
        const parts = value.split("; " + name + "=");
        if (parts.length === 2) return parts.pop().split(";").shift();
    }
}); 
// Basic Session Check for Landing Page
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('dynacuity_token');
    const user = JSON.parse(localStorage.getItem('dynacuity_user'));
    const launchBtn = document.querySelector('a[id="ctaBtn"]');
    const welcomeTitle = document.querySelector('.hero h1');

    if (token && user) {
        if (launchBtn) {
            launchBtn.innerText = "Back to Dashboard";
            launchBtn.href = "dashboard.html";
        }
        if (welcomeTitle && user.full_name) {
            welcomeTitle.innerText = `Welcome back, ${user.full_name}`;
        }
    }
});

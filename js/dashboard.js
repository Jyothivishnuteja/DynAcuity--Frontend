/**
 * dashboard.js
 * Handles Dashboard data fetching and UI updates.
 */

// dashboard.js uses BASE_URL defined in auth.js

document.addEventListener('DOMContentLoaded', () => {
    if (!isAuthenticated()) {
        window.location.href = 'auth/login.html';
        return;
    }

    const user = getCurrentUser();
    if (user) {
        // Update Welcome Text
        const welcomeH1 = document.querySelector('.user-text h1');
        if (welcomeH1) welcomeH1.innerText = `Welcome back, ${user.full_name || user.first_name || user.username || 'User'}`;

        // Update Avatar
        if (user.avatar) {
            const avatarImg = document.querySelector('.avatar-img');
            if (avatarImg) {
                avatarImg.src = `assets/images/${user.avatar}`;
            }
        }
    }

    fetchUserStats();

    // Auto-refresh when user returns to dashboard
    window.addEventListener('focus', () => {
        fetchUserStats();
    });
});

/**
 * Fetch results from backend to update dashboard stats
 */
async function fetchUserStats() {
    const token = localStorage.getItem('dynacuity_token');
    if (!token || !BASE_URL) return;

    try {
        // Fetch user details which contain calculated stats (Best Score, Accuracy, Streak)
        const response = await fetch(`${BASE_URL}/auth/user/`, {
            headers: {
                'Authorization': `Token ${token}`,
                'ngrok-skip-browser-warning': 'true'
            }
        });

        if (response.ok) {
            const user = await response.json();
            console.log('Dashboard Stats Updated:', user);
            updateDashboardUI(user);
        } else {
            console.error('Dashboard Stats Fetch Error:', response.status);
        }
    } catch (error) {
        console.error('Dashboard Stats Fetch Exception:', error);
    }
}

/**
 * Update Dashboard DOM with real backend data
 */
function updateDashboardUI(user) {
    if (!user) return;

    // Update Best Score Stat
    const scoreVal = document.getElementById('stat-best-score');
    if (scoreVal) {
        const bestScore = (user.best_score !== undefined && user.best_score !== null) ? user.best_score : 0;
        scoreVal.innerText = bestScore >= 1000 ? (bestScore / 1000).toFixed(1) + 'k' : bestScore;
    }

    // Update Accuracy Stat
    const accuracyVal = document.getElementById('stat-accuracy');
    if (accuracyVal) {
        const accuracy = (user.accuracy !== undefined && user.accuracy !== null) ? user.accuracy : 0;
        accuracyVal.innerText = `${Math.round(accuracy)}%`;
    }

    // Update Streak Stat
    const streakVal = document.getElementById('stat-streak');
    if (streakVal) {
        const streak = (user.streak !== undefined && user.streak !== null) ? user.streak : 0;
        streakVal.innerText = streak;
        localStorage.setItem('dayStreak', streak);
    }

    // Update Level and XP
    const lvEl = document.getElementById('userLevel');
    const xpEl = document.getElementById('userNextXp');
    if (lvEl) lvEl.innerText = user.level || '--';
    if (xpEl) {
        const nextLevelXp = (user.level || 1) * 1000;
        const xpToNext = Math.max(0, nextLevelXp - (user.xp || 0));
        xpEl.innerText = xpToNext.toLocaleString();
    }
}

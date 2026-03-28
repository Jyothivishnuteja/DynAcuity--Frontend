/**
 * sound-manager.js
 * Handles global audio feedback for DynAcuity Web.
 */

const SoundManager = {
    // Sound URLs (Using high-quality, subtle UI sounds)
    sounds: {
        click: 'https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3', // Soft UI tap
        success: 'https://assets.mixkit.co/active_storage/sfx/600/600-preview.mp3', // Pleasant bell chime
        levelUp: 'https://assets.mixkit.co/active_storage/sfx/2019/2019-preview.mp3', // Short melodic success
        error: 'https://assets.mixkit.co/active_storage/sfx/2573/2573-preview.mp3', // Subtle error pop
        bgm: 'https://assets.mixkit.co/music/preview/mixkit-funky-rock-guitar-604.mp3' // Energetic guitar BGM
    },
    bgmPlayer: null,
    currentSpeed: 1.0,

    isEnabled() {
        const val = localStorage.getItem('dynacuity_sounds');
        return val !== 'false'; // Defaults to true if null
    },

    isBGMEnabled() {
        const val = localStorage.getItem('dynacuity_bgm');
        return val !== 'false'; // Defaults to true if null
    },

    play(soundName) {
        if (!this.isEnabled()) return;

        const url = this.sounds[soundName];
        if (!url) return;

        try {
            const audio = new Audio(url);
            audio.volume = 0.4; // Keep it pleasant and subtle
            audio.play().catch(e => console.log("Audio play blocked until user interaction", e));
        } catch (err) {
            console.error("Sound Manager Error:", err);
        }
    },

    // Shortcut methods
    playClick() { this.play('click'); },
    playSuccess() { this.play('success'); },
    playError() { this.play('error'); },
    playLevelUp() { this.play('levelUp'); },

    startBGM() {
        if (localStorage.getItem('dynacuity_bgm') === 'false') return;
        if (this.bgmPlayer) return;

        this.bgmPlayer = new Audio(this.sounds.bgm);
        this.bgmPlayer.loop = true;
        this.bgmPlayer.volume = 0.25;
        this.bgmPlayer.playbackRate = this.currentSpeed;

        const playAttempt = this.bgmPlayer.play();
        if (playAttempt !== undefined) {
            playAttempt.catch(e => {
                console.log("BGM auto-play blocked. Waiting for user interaction...");
                const startOnInteract = () => {
                    this.bgmPlayer.play();
                    document.removeEventListener('click', startOnInteract);
                    document.removeEventListener('keydown', startOnInteract);
                };
                document.addEventListener('click', startOnInteract);
                document.addEventListener('keydown', startOnInteract);
            });
        }
    },

    setBGMSpeed(speed) {
        this.currentSpeed = speed;
        // Map 1-6x game speed to 1.0-2.0x audio speed if desired, or 1:1 up to 2.0x
        const audioSpeed = Math.min(1.0 + (speed - 1) * 0.2, 2.0);
        if (this.bgmPlayer) {
            this.bgmPlayer.playbackRate = audioSpeed;
        }
    },

    stopBGM() {
        if (this.bgmPlayer) {
            this.bgmPlayer.pause();
            this.bgmPlayer = null;
        }
    }
};

// Auto-bind to common navigation elements if on dashboard or settings
document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-link, .btn, .benefit-card, .game-list-item');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            SoundManager.playClick();
        });
    });

    // Auto-start BGM if enabled
    SoundManager.startBGM();
});

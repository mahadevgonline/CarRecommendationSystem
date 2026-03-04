/**
 * ═══════════════════════════════════════════════════
 *  INTERACTIVE LOGIN — script.js
 *  Car mascot with cursor-tracking eyes
 * ═══════════════════════════════════════════════════
 */

'use strict';

/* ─────────────────────── DOM References ─────────────────────────── */
const leftEye       = document.getElementById('left-eye');
const rightEye      = document.getElementById('right-eye');
const leftPupil     = document.getElementById('left-pupil');
const rightPupil    = document.getElementById('right-pupil');
const face          = document.getElementById('face');
const emailInput    = document.getElementById('email');
const passwordInput = document.getElementById('password');
const togglePwBtn   = document.getElementById('toggle-pw');
const pwEyeIcon     = document.getElementById('pw-eye-icon');
const loginForm     = document.getElementById('login-form');
const btnSignIn     = document.getElementById('btn-signin');
const speechBubble  = document.getElementById('speech-bubble');
const speechText    = document.getElementById('speech-text');

/* ─────────────────────── Constants ──────────────────────────────── */
// Maximum distance (px) a pupil can move inside its eye white
const MAX_PUPIL_OFFSET = 9;

/* ─────────────────────── State ──────────────────────────────────── */
let isShyMode     = false;  // true while password field is focused
let bubbleTimeout = null;

/* ═══════════════════════════════════════════════════════════════════
   PUPIL HELPERS
═══════════════════════════════════════════════════════════════════ */

/**
 * Returns the screen-space centre (x, y) of a given eye element.
 */
function getEyeCenter(eyeEl) {
    const r = eyeEl.getBoundingClientRect();
    return {
        x: r.left + r.width  / 2,
        y: r.top  + r.height / 2,
    };
}

/**
 * Moves a pupil element toward (targetX, targetY) in screen space,
 * clamped to MAX_PUPIL_OFFSET pixels from the eye's centre.
 *
 * @param {HTMLElement} pupilEl   - The pupil div to move
 * @param {number}      eyeCx     - Eye centre X (screen px)
 * @param {number}      eyeCy     - Eye centre Y (screen px)
 * @param {number}      targetX   - Target X to look toward (screen px)
 * @param {number}      targetY   - Target Y to look toward (screen px)
 */
function aimPupil(pupilEl, eyeCx, eyeCy, targetX, targetY) {
    const dx    = targetX - eyeCx;
    const dy    = targetY - eyeCy;
    const dist  = Math.hypot(dx, dy);

    // Clamp: pupil offset is proportional to distance but never exceeds MAX
    const offset = Math.min(MAX_PUPIL_OFFSET, dist / 7);
    const angle  = Math.atan2(dy, dx);

    const px = Math.cos(angle) * offset;
    const py = Math.sin(angle) * offset;

    pupilEl.style.transform = `translate(calc(-50% + ${px}px), calc(-50% + ${py}px))`;
}

/**
 * Aim both pupils simultaneously toward (x, y) in screen space.
 */
function aimBothPupils(x, y) {
    const lc = getEyeCenter(leftEye);
    const rc = getEyeCenter(rightEye);
    aimPupil(leftPupil,  lc.x, lc.y, x, y);
    aimPupil(rightPupil, rc.x, rc.y, x, y);
}

/**
 * Snap (with css animation class) pupils to look toward (x, y).
 */
function snapPupilsTo(x, y) {
    leftPupil.classList.add('snap');
    rightPupil.classList.add('snap');
    aimBothPupils(x, y);
    setTimeout(() => {
        leftPupil.classList.remove('snap');
        rightPupil.classList.remove('snap');
    }, 500);
}

/**
 * Reset pupils to centre (animated).
 */
function centrePupils() {
    leftPupil.classList.add('snap');
    rightPupil.classList.add('snap');
    leftPupil.style.transform  = 'translate(-50%, -50%)';
    rightPupil.style.transform = 'translate(-50%, -50%)';
    setTimeout(() => {
        leftPupil.classList.remove('snap');
        rightPupil.classList.remove('snap');
    }, 500);
}

/* ═══════════════════════════════════════════════════════════════════
   EYE OPEN / CLOSE
═══════════════════════════════════════════════════════════════════ */
function openEyes() {
    leftEye.classList.remove('closed');
    rightEye.classList.remove('closed');
}
function closeEyes() {
    leftEye.classList.add('closed');
    rightEye.classList.add('closed');
}

/* ═══════════════════════════════════════════════════════════════════
   SPEECH BUBBLE
═══════════════════════════════════════════════════════════════════ */
/**
 * Show a speech bubble with a message.
 * @param {string} msg      - Message to display (supports emoji)
 * @param {number} duration - ms to keep visible; 0 = stay until hidden manually
 */
function showBubble(msg, duration = 3000) {
    clearTimeout(bubbleTimeout);
    speechText.textContent = msg;
    speechBubble.classList.add('show');
    if (duration > 0) {
        bubbleTimeout = setTimeout(hideBubble, duration);
    }
}
function hideBubble() {
    clearTimeout(bubbleTimeout);
    speechBubble.classList.remove('show');
}

/* ═══════════════════════════════════════════════════════════════════
   EVENT: Mouse Move — Cursor Tracking
   Pupils smoothly follow the cursor at all times (unless shy mode).
═══════════════════════════════════════════════════════════════════ */
document.addEventListener('mousemove', function (e) {
    if (isShyMode) return;          // password field active → no tracking
    aimBothPupils(e.clientX, e.clientY);
});

/* ═══════════════════════════════════════════════════════════════════
   EVENT: Email Field — Focus / Blur
═══════════════════════════════════════════════════════════════════ */
emailInput.addEventListener('focus', function () {
    // Ensure normal state
    isShyMode = false;
    openEyes();
    face.classList.remove('shy');

    // Snap eyes to look toward the email input centre
    const r  = emailInput.getBoundingClientRect();
    const cx = r.left + r.width  / 2;
    const cy = r.top  + r.height / 2;
    snapPupilsTo(cx, cy);

    showBubble("I can see you! 👀", 2200);
});

emailInput.addEventListener('blur', function () {
    hideBubble();
    // Eyes return to free-tracking on next mousemove automatically
});

/* ═══════════════════════════════════════════════════════════════════
   EVENT: Password Field — Focus / Blur (Shy Mode)
═══════════════════════════════════════════════════════════════════ */
passwordInput.addEventListener('focus', function () {
    isShyMode = true;
    face.classList.add('shy');   // applies .shy to face

    // Snap pupils to look far upper-right (away)
    leftPupil.classList.add('snap');
    rightPupil.classList.add('snap');
    leftPupil.style.transform  = `translate(calc(-50% + ${MAX_PUPIL_OFFSET}px), calc(-50% - ${MAX_PUPIL_OFFSET - 2}px))`;
    rightPupil.style.transform = `translate(calc(-50% + ${MAX_PUPIL_OFFSET}px), calc(-50% - ${MAX_PUPIL_OFFSET - 2}px))`;
    setTimeout(() => {
        leftPupil.classList.remove('snap');
        rightPupil.classList.remove('snap');
    }, 500);

    // Then close eyes behind hands
    setTimeout(closeEyes, 140);

    showBubble("Not looking! 🙈", 0);   // stay until blur
});

passwordInput.addEventListener('blur', function () {
    isShyMode = false;
    face.classList.remove('shy');
    openEyes();
    hideBubble();
    // On next mousemove the pupils resume cursor tracking automatically
});

/* ═══════════════════════════════════════════════════════════════════
   EVENT: Password Visibility Toggle
═══════════════════════════════════════════════════════════════════ */
togglePwBtn.addEventListener('click', function () {
    const isHidden = passwordInput.type === 'password';
    passwordInput.type = isHidden ? 'text' : 'password';

    // Swap icon
    pwEyeIcon.innerHTML = isHidden
        // Strikethrough eye (hidden)
        ? `<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8
                    a18.45 18.45 0 0 1 5.06-5.94"/>
           <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8
                    a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07
                    a3 3 0 1 1-4.24-4.24"/>
           <line x1="1" y1="1" x2="23" y2="23"/>`
        // Open eye
        : `<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
           <circle cx="12" cy="12" r="3"/>`;

    // Mascot reacts
    if (!isShyMode) {
        const msg = isHidden ? "I see your password now! 😏" : "Okay okay, hiding! 😅";
        showBubble(msg, 2000);
    }
});

/* ═══════════════════════════════════════════════════════════════════
   EVENT: Form Submit
═══════════════════════════════════════════════════════════════════ */
loginForm.addEventListener('submit', function (e) {
    e.preventDefault();

    // Return mascot to normal
    isShyMode = false;
    face.classList.remove('shy');
    openEyes();
    centrePupils();

    // Animate button
    btnSignIn.classList.add('loading');
    btnSignIn.querySelector('.btn-text').textContent = 'Signing in…';
    btnSignIn.querySelector('.btn-icon').textContent = '⏳';

    showBubble("🚗 Vroooom! Logging you in!", 0);

    // Simulate async request
    setTimeout(() => {
        btnSignIn.classList.remove('loading');
        btnSignIn.querySelector('.btn-text').textContent = 'Sign In';
        btnSignIn.querySelector('.btn-icon').textContent = '→';
        showBubble("✅ Done! Welcome back.", 3000);
    }, 2200);
});

/* ═══════════════════════════════════════════════════════════════════
   INIT — Welcome greeting on page load
═══════════════════════════════════════════════════════════════════ */
window.addEventListener('load', function () {
    // Short delay so animations settle first
    setTimeout(() => showBubble("Hello there! 👋 Sign in to continue.", 3500), 900);
});

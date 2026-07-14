/* ═══════════════════════════════════════════════════════
   MAIN.JS — OMR System Frontend Logic
   ═══════════════════════════════════════════════════════ */

// ── Token Management ──────────────────────────────────
function getToken() {
    return localStorage.getItem("access_token");
}

function setToken(token) {
    localStorage.setItem("access_token", token);
}

function removeToken() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("current_user");
}

// ── API Fetch Wrapper ─────────────────────────────────
async function apiFetch(endpoint, options = {}) {
    const token = getToken();
    const headers = { ...options.headers };
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(endpoint, { ...options, headers });

    if (response.status === 401) {
        removeToken();
        window.location.href = "/login";
    }

    return response;
}

// ── Fetch Current User ────────────────────────────────
async function fetchCurrentUser() {
    const token = getToken();
    if (!token) return null;

    try {
        const res = await apiFetch("/auth/me");
        if (res.ok) {
            const user = await res.json();
            localStorage.setItem("current_user", JSON.stringify(user));
            return user;
        }
    } catch (e) {
        console.error("Error fetching user:", e);
    }
    return null;
}

// ── Build Sidebar ─────────────────────────────────────
function buildSidebar(user) {
    const sidebarNav = document.getElementById("sidebar-nav");
    const sidebarFooter = document.getElementById("sidebar-footer");
    if (!sidebarNav || !user) return;

    const currentPath = window.location.pathname;
    const isTeacher = user.role === "teacher" || user.role === "admin";

    let navHTML = `
        <div class="nav-section-title">Menu</div>
        <a href="/" class="${currentPath === '/' ? 'active' : ''}">
            <span class="material-icons-outlined">dashboard</span>
            Tổng quan
        </a>
    `;

    if (isTeacher) {
        navHTML += `
            <div class="nav-section-title">Quản lý</div>
            <a href="/exams" class="${currentPath === '/exams' ? 'active' : ''}">
                <span class="material-icons-outlined">description</span>
                Đề thi
            </a>
            <a href="/scan" class="${currentPath === '/scan' ? 'active' : ''}">
                <span class="material-icons-outlined">document_scanner</span>
                Quét & Chấm bài
            </a>
            <a href="/results" class="${currentPath === '/results' ? 'active' : ''}">
                <span class="material-icons-outlined">leaderboard</span>
                Bảng điểm
            </a>
        `;
    } else {
        navHTML += `
            <div class="nav-section-title">Học sinh</div>
            <a href="/results" class="${currentPath === '/results' ? 'active' : ''}">
                <span class="material-icons-outlined">grade</span>
                Điểm của tôi
            </a>
        `;
    }

    navHTML += `
        <div class="nav-section-title">Tài khoản</div>
        <button id="logout-btn">
            <span class="material-icons-outlined">logout</span>
            Đăng xuất
        </button>
    `;

    sidebarNav.innerHTML = navHTML;

    // Sidebar footer user info
    if (sidebarFooter) {
        const initials = (user.full_name || user.username).charAt(0).toUpperCase();
        sidebarFooter.innerHTML = `
            <div class="sidebar-user">
                <div class="user-avatar">${initials}</div>
                <div class="user-info">
                    <div class="user-name">${user.full_name || user.username}</div>
                    <div class="user-role">${user.role}</div>
                </div>
            </div>
        `;
    }

    // Logout handler
    document.getElementById("logout-btn").addEventListener("click", () => {
        removeToken();
        window.location.href = "/login";
    });
}

// ── Show Alert ────────────────────────────────────────
function showAlert(elementId, message, type = "error") {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.textContent = message;
    el.className = `alert alert-${type} show`;
    if (type === "success") {
        setTimeout(() => { el.classList.remove("show"); }, 3000);
    }
}

// ── Image Modal ───────────────────────────────────────
function openImageModal(src) {
    const overlay = document.getElementById("image-modal");
    if (!overlay) return;
    overlay.querySelector("img").src = src;
    overlay.classList.add("active");
}

function closeImageModal() {
    const overlay = document.getElementById("image-modal");
    if (overlay) overlay.classList.remove("active");
}

// ── Score CSS Class ───────────────────────────────────
function getScoreClass(score, maxScore) {
    if (maxScore === 0) return "score-mid";
    const pct = (score / maxScore) * 100;
    if (pct >= 70) return "score-high";
    if (pct >= 40) return "score-mid";
    return "score-low";
}

// ── Init App ──────────────────────────────────────────
document.addEventListener("DOMContentLoaded", async () => {
    const currentPath = window.location.pathname;
    const publicPaths = ["/login", "/register"];

    // Skip sidebar for auth pages
    if (publicPaths.includes(currentPath)) {
        const token = getToken();
        if (token) {
            const user = await fetchCurrentUser();
            if (user) {
                window.location.href = "/";
                return;
            }
        }
        window.currentUser = null;
        return;
    }

    // Protected pages
    const user = await fetchCurrentUser();
    if (!user) {
        window.location.href = "/login";
        return;
    }

    window.currentUser = user;
    buildSidebar(user);
});

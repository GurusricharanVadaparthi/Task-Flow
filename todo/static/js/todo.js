// ===================
// THEME MANAGEMENT
// ===================
function applyTheme(theme) {
    if (theme === 'system') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.body.classList.toggle('dark', prefersDark);
    } else {
        document.body.classList.toggle('dark', theme === 'dark');
    }
    updateThemeIcon(document.body.classList.contains('dark'));
}

function initTheme() {
    // Priority: server-set (data-theme) > localStorage > default light
    const bodyTheme = document.body.getAttribute('data-theme');
    const localTheme = localStorage.getItem('theme');
    const theme = bodyTheme && bodyTheme !== 'None' ? bodyTheme : (localTheme || 'light');
    applyTheme(theme);

    // Listen to system theme changes if theme = system
    if (theme === 'system' && window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)')
            .addEventListener('change', () => applyTheme('system'));
    }
}

function toggleTheme() {
    const isDark = document.body.classList.contains('dark');
    const newTheme = isDark ? 'light' : 'dark';
    document.body.classList.toggle('dark');
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(!isDark);
}

function updateThemeIcon(isDark) {
    const btn = document.getElementById('themeToggle');
    if (btn) btn.innerHTML = isDark ? '☀️' : '🌙';
}

// ===================
// DELETE MODAL
// ===================
let deleteUrl = '';

function openDeleteModal(url, taskName) {
    deleteUrl = url;
    document.getElementById('deleteTaskName').textContent = taskName;
    document.getElementById('deleteModal').classList.add('active');
}

function closeDeleteModal() {
    document.getElementById('deleteModal').classList.remove('active');
    deleteUrl = '';
}

function confirmDelete() {
    if (deleteUrl) {
        // Loading state
        const btn = document.querySelector('.modal-confirm');
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = 'Deleting...';
        }
        window.location.href = deleteUrl;
    }
}

// ===================
// MOBILE NAV
// ===================
function initMobileNav() {
    const toggle = document.getElementById('navToggle');
    const links = document.getElementById('navLinks');
    if (toggle && links) {
        toggle.addEventListener('click', () => links.classList.toggle('active'));
    }
}

// ===================
// LOADING STATE ON FORMS
// ===================
function initFormLoading() {
    const addForm = document.getElementById('addTaskForm');
    if (addForm) {
        addForm.addEventListener('submit', function() {
            const btn = this.querySelector('.add-btn');
            if (btn) {
                btn.disabled = true;
                const text = btn.querySelector('.btn-text');
                const spinner = btn.querySelector('.btn-spinner');
                if (text) text.style.display = 'none';
                if (spinner) spinner.style.display = 'inline-block';
            }
        });
    }

    // Save buttons on other forms
    document.querySelectorAll('.save-btn').forEach(btn => {
        const form = btn.closest('form');
        if (form) {
            form.addEventListener('submit', () => {
                btn.disabled = true;
                btn.textContent = 'Saving...';
            });
        }
    });
}

// ===================
// NATIVE OS NOTIFICATIONS
// ===================
const SHOWN_NOTIFICATIONS_KEY = 'shownNotifications';
const NOTIFICATION_CHECK_INTERVAL = 60000; // Check every 60 seconds

function initBrowserNotifications() {
    if (!('Notification' in window)) {
        console.log('Browser does not support notifications');
        return;
    }

    if (Notification.permission === 'default') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                checkAndShowNotifications();
            }
        });
    } else if (Notification.permission === 'granted') {
        // First check immediately
        checkAndShowNotifications();
        // Then poll every minute
        setInterval(checkAndShowNotifications, NOTIFICATION_CHECK_INTERVAL);
    }
}

function getShownNotifications() {
    try {
        const stored = localStorage.getItem(SHOWN_NOTIFICATIONS_KEY);
        if (!stored) return {};
        const data = JSON.parse(stored);
        // Clear entries older than 24 hours
        const now = Date.now();
        const cleaned = {};
        for (const [key, timestamp] of Object.entries(data)) {
            if (now - timestamp < 24 * 60 * 60 * 1000) {
                cleaned[key] = timestamp;
            }
        }
        return cleaned;
    } catch (e) {
        return {};
    }
}

function markNotificationShown(id) {
    const shown = getShownNotifications();
    shown[id] = Date.now();
    localStorage.setItem(SHOWN_NOTIFICATIONS_KEY, JSON.stringify(shown));
}

function checkAndShowNotifications() {
    if (Notification.permission !== 'granted') return;

    fetch('/api/notifications/', {
        credentials: 'same-origin'
    })
    .then(response => {
        if (!response.ok) throw new Error('Failed to fetch');
        return response.json();
    })
    .then(data => {
        const shown = getShownNotifications();

        data.notifications.forEach(notif => {
            // Only show if not already shown in the last 24 hours
            if (!shown[notif.id]) {
                showNativeToast(notif);
                markNotificationShown(notif.id);
            }
        });
    })
    .catch(err => console.log('Notification check failed:', err));
}

function showNativeToast(notif) {
    const notification = new Notification(notif.title, {
        body: notif.body,
        icon: '/static/icon.png', // Optional: add an icon
        tag: notif.id,
        requireInteraction: notif.type === 'overdue', // Overdue stays until clicked
        silent: false
    });

    notification.onclick = function() {
        window.focus();
        window.location.href = '/notifications/';
        notification.close();
    };

    // Auto-close non-critical notifications after 8 seconds
    if (notif.type !== 'overdue') {
        setTimeout(() => notification.close(), 8000);
    }
}

// ===================
// DOM READY
// ===================
document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    initMobileNav();
    initFormLoading();
    initBrowserNotifications();

    // Modal outside click
    const modal = document.getElementById('deleteModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) closeDeleteModal();
        });
    }

    // Auto-submit filter form
    document.querySelectorAll('.filter-group select').forEach(select => {
        select.addEventListener('change', function() {
            this.closest('form').submit();
        });
    });
});

// ===================
// CHART.JS
// ===================
function initCharts(labels, createdData, completedData, priorityData) {
    const isDark = document.body.classList.contains('dark');
    const textColor = isDark ? '#e2e8f0' : '#1e293b';
    const gridColor = isDark ? '#334155' : '#e2e8f0';

    const activityCtx = document.getElementById('activityChart');
    if (activityCtx) {
        new Chart(activityCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Created',
                        data: createdData,
                        borderColor: '#2563eb',
                        backgroundColor: 'rgba(37,99,235,0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Completed',
                        data: completedData,
                        borderColor: '#16a34a',
                        backgroundColor: 'rgba(22,163,74,0.1)',
                        tension: 0.4,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { labels: { color: textColor } } },
                scales: {
                    x: { ticks: { color: textColor }, grid: { color: gridColor } },
                    y: { ticks: { color: textColor, stepSize: 1 }, grid: { color: gridColor }, beginAtZero: true }
                }
            }
        });
    }

    const priorityCtx = document.getElementById('priorityChart');
    if (priorityCtx) {
        new Chart(priorityCtx, {
            type: 'doughnut',
            data: {
                labels: ['High', 'Medium', 'Low'],
                datasets: [{
                    data: priorityData,
                    backgroundColor: ['#ef4444', '#f59e0b', '#16a34a'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { color: textColor } }
                }
            }
        });
    }
}
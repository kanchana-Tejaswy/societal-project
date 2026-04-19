/* ============================================================
   DASHBOARD ARCHITECTURE - STATIC LIVE SERVER MODE
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }
});

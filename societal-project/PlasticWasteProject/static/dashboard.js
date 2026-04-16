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

    const tableBody = document.getElementById('tableBody');
    const emptyState = document.getElementById('emptyState');
    const totalEl = document.getElementById('stat-total');
    const recyclableEl = document.getElementById('stat-recyclable');
    const nonEl = document.getElementById('stat-non');
    const clearButton = document.getElementById('clearData');

    const logs = JSON.parse(localStorage.getItem('smartWasteLogs') || '[]');
    let recyclable = 0;
    let nonRecyclable = 0;

    if (logs.length === 0) {
        if (emptyState) emptyState.style.display = 'block';
    } else {
        if (emptyState) emptyState.style.display = 'none';
        logs.forEach(log => {
            if (!tableBody) return;
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>#${log.id}</td>
                <td>${log.type}</td>
                <td>${log.quantity}</td>
                <td>${log.result}</td>
            `;
            tableBody.appendChild(row);

            if (String(log.result).toLowerCase().includes('yes')) {
                recyclable += 1;
            } else {
                nonRecyclable += 1;
            }
        });
    }

    if (totalEl) totalEl.textContent = logs.length;
    if (recyclableEl) recyclableEl.textContent = recyclable;
    if (nonEl) nonEl.textContent = nonRecyclable;

    if (clearButton) {
        clearButton.addEventListener('click', () => {
            localStorage.removeItem('smartWasteLogs');
            window.location.reload();
        });
    }
});

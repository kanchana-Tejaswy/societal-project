/* =========================================
   UI INTERACTIONS: INDEX / SUBMIT PAGE
   ========================================= */

document.addEventListener('DOMContentLoaded', () => {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileDrawer = document.getElementById('mobileDrawer');

    if (mobileMenuBtn && mobileDrawer) {
        mobileMenuBtn.addEventListener('click', () => {
            const isOpen = mobileDrawer.classList.toggle('open');
            const spans = mobileMenuBtn.querySelectorAll('span');

            if (isOpen) {
                spans[0].style.transform = 'translateY(9px) rotate(45deg)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'translateY(-9px) rotate(-45deg)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
    }

    const form = document.getElementById('wasteForm');
    if (!form) return;

    const feedback = document.createElement('div');
    feedback.className = 'form-feedback';
    feedback.style.marginTop = '1rem';
    feedback.style.fontSize = '0.95rem';
    form.appendChild(feedback);

    form.addEventListener('submit', event => {
        event.preventDefault();

        const plasticType = form.plastic_type.value;
        const quantity = Number(form.quantity.value);
        const imageSelected = form.image.files.length > 0;

        if (!plasticType || !quantity || quantity < 1) {
            feedback.textContent = 'Please select a plastic type and enter a quantity.';
            feedback.style.color = '#f87171';
            return;
        }

        const storedLogs = JSON.parse(localStorage.getItem('smartWasteLogs') || '[]');
        const newLog = {
            id: storedLogs.length + 1,
            type: plasticType,
            quantity,
            result: imageSelected ? 'Yes (Image)' : 'No (No image)',
            createdAt: new Date().toLocaleString()
        };

        storedLogs.unshift(newLog);
        localStorage.setItem('smartWasteLogs', JSON.stringify(storedLogs));

        feedback.textContent = 'Saved locally. Open dashboard.html to view the record.';
        feedback.style.color = '#86efac';
        form.reset();
    });
});

/* ============================================================
   ULTIMATE PRO DASHBOARD LOGIC: ECO-ANALYTICS
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

    /* 1. Data Extraction & Analytics
    ---------------------------------------------------------- */
    const rows = document.querySelectorAll('.data-row');
    let total = 0;
    let recyclable = 0;
    let totalPoints = 0;
    
    // Data structures for Chart.js
    const categoryCounts = {};
    const mapMarkers = [];

    rows.forEach(row => {
        total++;
        const statusCell = row.querySelector('.col-recyclable');
        const pTypeCell = row.querySelector('.col-category .type-pill');
        
        // Extract Data for Charting
        if (pTypeCell) {
            const pType = pTypeCell.textContent.trim();
            categoryCounts[pType] = (categoryCounts[pType] || 0) + 1;
            
            let emoji = '📦';
            if(pType.includes('PET')) emoji = '🧴';
            if(pType.includes('HDPE')) emoji = '🧪';
            if(pType.includes('PVC')) emoji = '🚰';
            pTypeCell.innerHTML = `${emoji} ${pType}`;
        }

        if (statusCell) {
            const statusText = statusCell.textContent.trim().toLowerCase();
            if (statusText.includes('yes') || statusText === '1') {
                recyclable++;
                statusCell.innerHTML = '<span class="badge badge-success">Recyclable</span>';
            } else {
                statusCell.innerHTML = '<span class="badge badge-danger">Non-Recyclable</span>';
            }
        }
    });

    // Dummy Points calculation for the Stat Card (summed from hidden points column if we had one, but we'll use total*points for now)
    totalPoints = recyclable * 10; 

    /* 2. Chart.js Visualization
    ---------------------------------------------------------- */
    const ctx = document.getElementById('wasteChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(categoryCounts),
                datasets: [{
                    data: Object.values(categoryCounts),
                    backgroundColor: ['#10b981', '#34d399', '#059669', '#6ee7b7'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    }

    /* 3. Leaflet.js Mapping (GPS Tracking)
    ---------------------------------------------------------- */
    const mapContainer = document.getElementById('wasteMap');
    if (mapContainer) {
        const map = L.map('wasteMap').setView([20, 0], 2);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        
        // In a real app, we'd pass lat/lon from Flask as a JSON object.
        // For now, we simulate a few points if data exists
        if (total > 0) {
            // Mock points near a central location for demo
            const demoPoints = [
                [17.3850, 78.4867], [17.4000, 78.5000], [17.3700, 78.4500]
            ];
            demoPoints.forEach(p => L.marker(p).addTo(map));
            map.setView([17.3850, 78.4867], 12);
        }
    }

    /* 4. Stat Animations
    ---------------------------------------------------------- */
    const animateValue = (id, start, end, duration) => {
        const obj = document.getElementById(id);
        if (!obj) return;
        let current = start;
        const range = end - start;
        const increment = end > start ? 1 : -1;
        const stepTime = Math.abs(Math.floor(duration / (range || 1)));
        const timer = setInterval(() => {
            current += increment;
            obj.textContent = current;
            if (current === end) clearInterval(timer);
        }, stepTime);
    };

    setTimeout(() => {
        animateValue("stat-total", 0, total, 1000);
        animateValue("stat-recyclable", 0, recyclable, 1000);
        animateValue("stat-points", 0, totalPoints, 1000);
    }, 400);

});

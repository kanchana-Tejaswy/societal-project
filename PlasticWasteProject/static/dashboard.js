/* ============================================================
   ENTERPRISE SAAS DASHBOARD - LOGIC & VISUALIZATIONS
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

    /* ----------------------------------------------------
       1. MOBILE SIDEBAR NAVIGATION
    ---------------------------------------------------- */
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileCloseBtn = document.getElementById('mobileCloseBtn');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    const toggleSidebar = (isOpen) => {
        if (isOpen) {
            sidebar.classList.add('open');
            sidebarOverlay.classList.add('open');
            document.body.style.overflow = 'hidden';
        } else {
            sidebar.classList.remove('open');
            sidebarOverlay.classList.remove('open');
            document.body.style.overflow = '';
        }
    };

    if(mobileMenuBtn) mobileMenuBtn.addEventListener('click', () => toggleSidebar(true));
    if(mobileCloseBtn) mobileCloseBtn.addEventListener('click', () => toggleSidebar(false));
    if(sidebarOverlay) sidebarOverlay.addEventListener('click', () => toggleSidebar(false));

    /* ----------------------------------------------------
       2. DATA AGGREGATION FROM PAYLOAD
    ---------------------------------------------------- */
    const data = window.WasteDataPayload || [];
    
    if (data.length > 0) {
        let materialCounts = { 'Plastic': 0, 'Paper': 0, 'Glass': 0, 'Metal': 0, 'Other': 0 };
        
        data.forEach(item => {
            let type = String(item.material).toLowerCase();
            let qty = parseInt(item.quantity) || 1;
            
            if(type.includes('plastic') || type.includes('pet') || type.includes('hdpe')) materialCounts['Plastic'] += qty;
            else if(type.includes('paper') || type.includes('cardboard')) materialCounts['Paper'] += qty;
            else if(type.includes('glass')) materialCounts['Glass'] += qty;
            else if(type.includes('metal') || type.includes('alum')) materialCounts['Metal'] += qty;
            else materialCounts['Other'] += qty;
        });

        /* ----------------------------------------------------
           3. CHART.JS INTEGRATION (DOUGHNUT)
        ---------------------------------------------------- */
        const ctx = document.getElementById('distributionChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Plastic', 'Paper', 'Glass', 'Metal', 'Other'],
                    datasets: [{
                        data: [
                            materialCounts['Plastic'], 
                            materialCounts['Paper'], 
                            materialCounts['Glass'], 
                            materialCounts['Metal'], 
                            materialCounts['Other']
                        ],
                        backgroundColor: ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#94a3b8'],
                        borderWidth: 0,
                        hoverOffset: 10
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '75%',
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: {
                                padding: 20,
                                font: { family: 'Inter', size: 12, weight: '600' },
                                usePointStyle: true,
                                color: '#64748b'
                            }
                        }
                    }
                }
            });
        }
    }

    /* ----------------------------------------------------
       4. LEAFLET.JS - ADVANCED GPS TRACKING
    ---------------------------------------------------- */
    const mapEl = document.getElementById('gpsMap');
    if (mapEl) {
        // Initialize Map (Default center, roughly global/city level)
        // We'll center on first valid coordinate or default to New York for demo
        let defaultLat = 40.7128;
        let defaultLon = -74.0060;
        
        let validCoords = data.filter(d => d.lat && d.lon && d.lat !== "None" && d.lon !== "None");
        if (validCoords.length > 0) {
            defaultLat = parseFloat(validCoords[0].lat);
            defaultLon = parseFloat(validCoords[0].lon);
        }

        const map = L.map('gpsMap', { zoomControl: false }).setView([defaultLat, defaultLon], 13);
        
        // Add Zoom Control at bottom right
        L.control.zoom({ position: 'bottomright' }).addTo(map);

        // CartoDB Dark Matter Base Map (Futuristic/Enterprise Feel)
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; CartoDB',
            subdomains: 'abcd',
            maxZoom: 20
        }).addTo(map);

        // Custom Marker Icons
        const createMarkerIcon = (color) => {
            return L.divIcon({
                className: 'custom-marker',
                html: `<div style="background-color: ${color}; width: 14px; height: 14px; border-radius: 50%; box-shadow: 0 0 10px ${color}, 0 0 0 3px rgba(255,255,255,0.2);"></div>`,
                iconSize: [14, 14],
                iconAnchor: [7, 7]
            });
        };

        const ecoIcon = createMarkerIcon('#10b981'); // Emerald
        const alertIcon = createMarkerIcon('#ef4444'); // Red

        // Plot Actual Data Points
        validCoords.forEach(item => {
            const isRecyclable = String(item.recyclable).toLowerCase().includes('yes');
            const icon = isRecyclable ? ecoIcon : alertIcon;
            
            L.marker([parseFloat(item.lat), parseFloat(item.lon)], { icon: icon })
             .addTo(map)
             .bindPopup(`
                <div style="font-family: Inter; padding: 5px;">
                    <strong style="color: #0f172a; display: block; margin-bottom: 4px;">Log #${item.id}</strong>
                    <span style="color: #64748b;">Material:</span> <b>${item.material}</b><br>
                    <span style="color: #64748b;">Qty:</span> <b>${item.quantity}</b><br>
                    <span style="color: #64748b;">Status:</span> <b style="color: ${isRecyclable ? '#10b981' : '#ef4444'};">${isRecyclable ? 'Recyclable' : 'Waste'}</b>
                </div>
             `);
        });

        // ==========================================
        // SIMULATE LIVE FLEET VEHICLE MOVEMENT
        // ==========================================
        const fleetMarker = L.divIcon({
            className: 'fleet-marker',
            html: `<div style="background-color: #3b82f6; width: 18px; height: 18px; border-radius: 50%; box-shadow: 0 0 15px #3b82f6, 0 0 0 4px rgba(59, 130, 246, 0.3);"></div>`,
            iconSize: [18, 18],
            iconAnchor: [9, 9]
        });

        let vehicleLat = defaultLat + 0.01;
        let vehicleLon = defaultLon + 0.01;
        const vehicle = L.marker([vehicleLat, vehicleLon], { icon: fleetMarker }).addTo(map);
        vehicle.bindPopup("<b>Fleet Alpha-1</b><br>Status: Collecting");

        // Simple Random Walk Simulation for Fleet Vehicle
        setInterval(() => {
            vehicleLat += (Math.random() - 0.5) * 0.002;
            vehicleLon += (Math.random() - 0.5) * 0.002;
            vehicle.setLatLng([vehicleLat, vehicleLon]);
        }, 3000);
    }

});

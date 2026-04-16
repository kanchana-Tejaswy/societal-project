/* ============================================================
   DASHBOARD ARCHITECTURE - VANILLA JS LOGIC
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

    /* 1. Mobile Sidebar Toggle
    ---------------------------------------------------------- */
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }

    /* 2. Client-Side Analytics Parsing & Stat Calculation
    ---------------------------------------------------------- */
    const rows = document.querySelectorAll('.data-row');
    let total = 0;
    let recyclable = 0;
    let nonRecyclable = 0;
    
    // Process Table elements securely without touching Jinja context
    rows.forEach(row => {
        total++;
        const statusCell = row.querySelector('.col-recyclable');
        const pTypeCell = row.querySelector('.col-category .type-pill');
        
        if (pTypeCell) {
            const pType = pTypeCell.textContent.trim();
            // Aesthetic enhancement: Assign Emojis dynamically based on text
            let emoji = '📦';
            if(pType.includes('PET')) emoji = '🧴';
            if(pType.includes('HDPE')) emoji = '🧪';
            if(pType.includes('PVC')) emoji = '🚰';
            pTypeCell.innerHTML = `${emoji} ${pType}`;
        }

        if (statusCell) {
            const statusText = statusCell.textContent.trim().toLowerCase();
            
            // Dynamic UI Badge generation mapping from raw text
            if (statusText.includes('yes') || statusText === '1') {
                recyclable++;
                statusCell.innerHTML = '<span class="badge badge-success">Recyclable</span>';
            } else {
                nonRecyclable++;
                statusCell.innerHTML = '<span class="badge badge-danger">Non-Recyclable</span>';
            }
        }
    });

    /* 3. Number Counter Animation for KPI Stats
    ---------------------------------------------------------- */
    const animateValue = (id, start, end, duration) => {
        if (start === end) {
            const el = document.getElementById(id);
            if(el) el.textContent = end;
            return;
        }
        
        const obj = document.getElementById(id);
        if (!obj) return;

        const range = end - start;
        let current = start;
        const increment = end > start ? 1 : -1;
        const stepTime = Math.abs(Math.floor(duration / range));
        
        const timer = setInterval(() => {
            current += increment;
            obj.textContent = current;
            if (current === end) clearInterval(timer);
        }, stepTime);
    };

    // Staggered KPI injection
    setTimeout(() => {
        animateValue("stat-total", 0, total, 1200);
        animateValue("stat-recyclable", 0, recyclable, 1200);
        animateValue("stat-non", 0, nonRecyclable, 1200);
    }, 400);

    /* 4. Scroll Reveal Intersection Observer Mechanism
    ---------------------------------------------------------- */
    const revealElements = document.querySelectorAll('.scroll-reveal');
    if ('IntersectionObserver' in window) {
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if(entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        revealElements.forEach(el => revealObserver.observe(el));
    } else {
        // Fallback
        revealElements.forEach(el => el.classList.add('visible'));
    }

    /* 5. Eco-Themed Background Particles Generation
    ---------------------------------------------------------- */
    const particlesContainer = document.getElementById('particles');
    if (particlesContainer) {
        const particleCount = window.innerWidth < 768 ? 10 : 25; // Less intensive on mobile
        
        for(let i = 0; i < particleCount; i++) {
            let p = document.createElement('div');
            p.className = 'particle';
            
            let size = Math.random() * 25 + 10;
            p.style.width = size + 'px';
            p.style.height = (size * 1.5) + 'px'; // organic proportion
            p.style.left = Math.random() * 100 + 'vw';
            
            // Randomize speeds and offsets to feel natural
            p.style.animationDuration = Math.random() * 15 + 12 + 's';
            p.style.animationDelay = Math.random() * 10 + 's';
            p.style.opacity = Math.random() * 0.4 + 0.1;
            
            particlesContainer.appendChild(p);
        }
    }
});

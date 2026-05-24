/* ============================================================
   SMART WASTE - GLOBAL CORE LOGIC
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

    /* 0. PWA Service Worker Registration
    ---------------------------------------------------------- */
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/static/sw.js')
                .then(reg => console.log('SW Registered'))
                .catch(err => console.log('SW Registration Failed', err));
        });
    }

    /* 1. Universal Particle Engine
    ---------------------------------------------------------- */
    // ... (rest of code)
    const initParticles = () => {
        const particleContainer = document.getElementById('particles') || (() => {
            const div = document.createElement('div');
            div.id = 'particles';
            document.body.prepend(div);
            return div;
        })();

        particleContainer.innerHTML = ''; // Reset
        const count = window.innerWidth < 768 ? 20 : 40;
        
        for(let i = 0; i < count; i++) {
            const p = document.createElement('div');
            const depth = Math.floor(Math.random() * 3) + 1;
            p.className = `particle depth-${depth}`;
            
            const size = Math.random() * 25 + 15;
            p.style.width = size + 'px';
            p.style.height = (size * 1.4) + 'px';
            p.style.left = Math.random() * 100 + 'vw';
            
            const baseSpeed = depth === 1 ? 12 : depth === 2 ? 18 : 25;
            p.style.animationDuration = (Math.random() * 8 + baseSpeed) + 's';
            p.style.animationDelay = (Math.random() * 10) + 's';
            p.style.opacity = Math.random() * 0.3 + 0.2;
            
            particleContainer.appendChild(p);
        }
    };

    initParticles();
    window.addEventListener('resize', () => {
        // Debounced resize could be better, but simple re-init for now
        if (window.innerWidth < 768) initParticles();
    });

    /* 2. Unified Navigation Controller
    ---------------------------------------------------------- */
    // Top Navbar Drawer (Landing & Index)
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileDrawer = document.getElementById('mobileDrawer');
    
    // Dashboard Sidebar
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');

    const toggleMenu = (btn, target, className = 'open') => {
        if (!btn || !target) return;
        
        const updateHamburger = (isOpen) => {
            const spans = btn.querySelectorAll('span');
            if (spans.length === 3) {
                spans[0].style.transform = isOpen ? 'translateY(8px) rotate(45deg)' : 'none';
                spans[1].style.opacity = isOpen ? '0' : '1';
                spans[2].style.transform = isOpen ? 'translateY(-8px) rotate(-45deg)' : 'none';
            }
        };

        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isOpen = target.classList.toggle(className);
            updateHamburger(isOpen);
        });

        // Close when clicking links
        target.querySelectorAll('.nav-item').forEach(link => {
            link.addEventListener('click', () => {
                target.classList.remove(className);
                updateHamburger(false);
            });
        });

        // Close when clicking outside
        document.addEventListener('click', (e) => {
            if (target.classList.contains(className) && !target.contains(e.target) && !btn.contains(e.target)) {
                target.classList.remove(className);
                updateHamburger(false);
            }
        });
    };

    toggleMenu(mobileMenuBtn, mobileDrawer, 'open');
    toggleMenu(menuToggle, sidebar, 'active');

    /* 3. Ripple & Interaction Effects
    ---------------------------------------------------------- */
    const applyRipple = (e) => {
        const btn = e.currentTarget;
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const ripple = document.createElement('span');
        ripple.className = 'ripple';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        
        btn.appendChild(ripple);
        setTimeout(() => ripple.remove(), 800);
    };

    document.querySelectorAll('.btn, .btn-submit, .btn-new, .nav-item, button').forEach(el => {
        if (!el.classList.contains('no-ripple')) {
            el.addEventListener('mousedown', applyRipple);
        }
    });

    /* 4. Intersection Observer for Smooth Reveal
    ---------------------------------------------------------- */
    const revealOptions = { threshold: 0.15, rootMargin: "0px 0px -50px 0px" };
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                revealObserver.unobserve(entry.target);
            }
        });
    }, revealOptions);

    /* 5. Geolocation Logic (GPS Tracking)
    ---------------------------------------------------------- */
    const wasteForm = document.getElementById('wasteForm');
    if (wasteForm && navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const latInput = document.createElement('input');
            latInput.type = 'hidden';
            latInput.name = 'latitude';
            latInput.value = position.coords.latitude;
            
            const lonInput = document.createElement('input');
            lonInput.type = 'hidden';
            lonInput.name = 'longitude';
            lonInput.value = position.coords.longitude;
            
            wasteForm.appendChild(latInput);
            wasteForm.appendChild(lonInput);
            console.log("GPS Location Captured");
        }, (err) => {
            console.warn("Geolocation denied or unavailable", err);
        });
    }

});

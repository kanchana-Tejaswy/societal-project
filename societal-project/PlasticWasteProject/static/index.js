/* =========================================
   UI INTERACTIONS: INDEX (LANDING PAGE)
   ========================================= */

   document.addEventListener('DOMContentLoaded', () => {

    /* 1. Dynamic Eco Leaves (Particles) Generator
    ---------------------------------------------------------- */
    // Ensure we don't duplicate on multiple loads
    if (!document.getElementById('particles')) {
        const particlesContainer = document.createElement('div');
        particlesContainer.id = 'particles';
        document.body.prepend(particlesContainer);
        
        // Responsive particle generation
        const particleCount = window.innerWidth < 768 ? 8 : 18;
        
        for(let i = 0; i < particleCount; i++) {
            let p = document.createElement('div');
            p.className = 'particle';
            let size = Math.random() * 20 + 10;
            p.style.width = size + 'px';
            p.style.height = (size * 1.5) + 'px'; // Gives the leaf its elongated shape
            p.style.left = Math.random() * 100 + 'vw';
            
            // Randomize speeds so they float organically
            p.style.animationDuration = Math.random() * 15 + 10 + 's';
            p.style.animationDelay = Math.random() * 8 + 's';
            particlesContainer.appendChild(p);
        }
    }

    /* 2. Mobile Drawer Navigation Toggle
    ---------------------------------------------------------- */
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileDrawer = document.getElementById('mobileDrawer');
    
    if (mobileMenuBtn && mobileDrawer) {
        mobileMenuBtn.addEventListener('click', () => {
            const isOpen = mobileDrawer.classList.toggle('open');
            
            // Hamburger to Cross Animation Context
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

    /* 3. Material Ripple Effect for Premium Button UI
    ---------------------------------------------------------- */
    const rippleButtons = document.querySelectorAll('.ripple-btn');
    
    rippleButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            // Note: Since these elements are <a> tags acting as strict routes natively, 
            // the ripple fires briefly as visual confirmation before the browser handles 
            // document unloading and routing instantly.
            
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

});

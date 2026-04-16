document.addEventListener("DOMContentLoaded", () => {
    // 1. Create Floating Particles for the Eco Vibe
    const particlesContainer = document.createElement("div");
    particlesContainer.id = "particles";
    document.body.appendChild(particlesContainer);
  
    for (let i = 0; i < 20; i++) {
      const p = document.createElement("div");
      p.classList.add("particle");
      const size = Math.random() * 15 + 5;
      p.style.width = `${size}px`;
      p.style.height = `${size}px`;
      p.style.left = `${Math.random() * 100}vw`;
      p.style.animationDuration = `${Math.random() * 10 + 8}s`;
      p.style.animationDelay = `${Math.random() * 5}s`;
      particlesContainer.appendChild(p);
    }
  
    // 2. Ripple Effect on Buttons
    const buttons = document.querySelectorAll("button");
    buttons.forEach(btn => {
      // prevent overflow so ripple stays inside the button
      btn.style.position = 'relative';
      btn.style.overflow = 'hidden';

      btn.addEventListener("click", function(e) {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const circle = document.createElement("span");
        circle.classList.add("ripple");
        circle.style.left = `${x}px`;
        circle.style.top = `${y}px`;
        
        this.appendChild(circle);
        setTimeout(() => circle.remove(), 600);
      });
    });
  
    // 3. Form logic & micro-interactions
    const form = document.querySelector("form");
    if (form) {
      // Wrap bare text nodes in form to spans for better styling
      const childNodes = Array.from(form.childNodes);
      childNodes.forEach(node => {
        if (node.nodeType === 3 && node.nodeValue.trim() !== "") {
          const span = document.createElement('span');
          span.textContent = node.nodeValue;
          span.style.fontWeight = '600';
          span.style.color = 'var(--text-dark)';
          span.style.display = 'block';
          span.style.marginBottom = '-5px';
          span.style.marginTop = '10px';
          form.replaceChild(span, node);
        }
      });
  
      const submitBtn = form.querySelector('button[type="submit"]');
      form.addEventListener("submit", (e) => {
        // Natural submission takes place, just add visual processing effect
        submitBtn.innerHTML = "Processing ♻️...";
        submitBtn.style.opacity = '0.8';
        submitBtn.style.transform = 'scale(0.98)';
      });
    }
  
    // 4. Dashboard Enhancements
    const table = document.querySelector("table");
    if (table) {
      // Ensure it displays dynamically without flex overriding the row styles
      table.style.display = 'table';
      
      const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent);
      const rows = table.querySelectorAll('tr');
      
      rows.forEach((row, rowIndex) => {
        if (rowIndex === 0) return; // Skip header row
        const cells = row.querySelectorAll('td');
        cells.forEach((cell, cellIndex) => {
          // Set data-label for mobile view
          if (headers[cellIndex]) {
            cell.setAttribute('data-label', headers[cellIndex]);
          }
          
          // Recyclable badge injection
          if (headers[cellIndex] === 'Recyclable') {
            const text = cell.textContent.trim();
            if (text.toLowerCase() === 'yes' || text === '1') {
              cell.innerHTML = `<span class="badge badge-success">✓ ${text}</span>`;
            } else {
              cell.innerHTML = `<span class="badge badge-danger">✗ ${text}</span>`;
            }
          }
        });
      });
    }
  });

 // Enhanced particle system
function createParticles() {
    const particlesContainer = document.getElementById('particles');
    
    for (let i = 0; i < 80; i++) {
        setTimeout(() => {
            const particle = document.createElement('div');
            particle.className = 'birthday-particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 4 + 's';
            particle.style.animationDuration = (Math.random() * 3 + 2) + 's';
            particle.style.width = (Math.random() * 10 + 5) + 'px';
            particle.style.height = particle.style.width;
            particlesContainer.appendChild(particle);
            
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.parentNode.removeChild(particle);
                }
            }, 6000);
        }, i * 50);
    }
}

// Scroll progress bar
function updateScrollProgress() {
    const scrollProgress = document.getElementById('scroll-progress');
    const scrollTop = window.pageYOffset;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;
    scrollProgress.style.width = scrollPercent + '%';
}

// Continuous particle generation
setInterval(createParticles, 2000);
createParticles();

// Scroll progress updates
window.addEventListener('scroll', updateScrollProgress);

// Enhanced smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

 
// Enhanced parallax effect
let ticking = false;
function updateParallax() {
    const scrolled = window.pageYOffset;
    const shapes = document.querySelectorAll('.shape');
    
    shapes.forEach((shape, index) => {
        const speed = 0.3 + (index * 0.1);
        const yPos = -(scrolled * speed);
        shape.style.transform = `translateY(${yPos}px) rotate(${scrolled * 0.1}deg)`;
    });
    
    ticking = false;
}

function requestTick() {
    if (!ticking) {
        requestAnimationFrame(updateParallax);
        ticking = true;
    }
}

window.addEventListener('scroll', requestTick);

// Enhanced intersection observer for staggered animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            setTimeout(() => {
                entry.target.style.animation = 'fadeInUp 0.8s ease-out forwards';
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }, index * 100);
        }
    });
}, observerOptions);

// Observe all feature cards and contact items
document.querySelectorAll('.feature-card, .contact-item').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(50px)';
    observer.observe(card);
});

// Add mouse move effect for hero section
const hero = document.querySelector('.hero');
hero.addEventListener('mousemove', (e) => {
    const rect = hero.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    
    const rotateX = (y - centerY) / centerY * 5;
    const rotateY = (centerX - x) / centerX * 5;
    
    const heroContent = document.querySelector('.hero-content');
    heroContent.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
});

// Reset hero content transform when mouse leaves
hero.addEventListener('mouseleave', () => {
    const heroContent = document.querySelector('.hero-content');
    heroContent.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg)';
});

// Add floating animation to feature icons on hover
document.querySelectorAll('.feature-card').forEach(card => {
    const icon = card.querySelector('.feature-icon');
    
    card.addEventListener('mouseenter', () => {
        icon.style.animation = 'iconFloat 0.6s ease-in-out infinite';
    });
    
    card.addEventListener('mouseleave', () => {
        icon.style.animation = 'iconFloat 3s ease-in-out infinite';
    });
});

// Add typewriter effect to hero title
function typewriterEffect() {
    const title = document.querySelector('.hero h1');
    const text = title.textContent;
    title.textContent = '';
    title.style.opacity = '1';
    
    let i = 0;
    const speed = 100;
    
    function typeWriter() {
        if (i < text.length) {
            title.textContent += text.charAt(i);
            i++;
            setTimeout(typeWriter, speed);
        }
    }
    
    setTimeout(typeWriter, 1000);
}

// Enhanced page load animations
window.addEventListener('load', () => {
    // Trigger typewriter effect
    typewriterEffect();
    
    // Staggered animation for navigation links
    document.querySelectorAll('.nav-links a').forEach((link, index) => {
        setTimeout(() => {
            link.style.animation = 'fadeInUp 0.6s ease-out forwards';
        }, index * 100);
    });
    
    // Animate CTA buttons
    document.querySelectorAll('.cta-buttons .btn').forEach((btn, index) => {
        setTimeout(() => {
            btn.style.animation = 'fadeInUp 0.8s ease-out forwards';
        }, 1500 + (index * 200));
    });
});

// Add ripple effect to buttons
function createRipple(event) {
    const button = event.currentTarget;
    const circle = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;
    
    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
    circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
    circle.classList.add('ripple');
    
    const ripple = button.getElementsByClassName('ripple')[0];
    if (ripple) {
        ripple.remove();
    }
    
    button.appendChild(circle);
    
    setTimeout(() => {
        circle.remove();
    }, 600);
}

// Add ripple CSS dynamically
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.4);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(rippleStyle);

// Add ripple effect to all buttons
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', createRipple);
});

// Add scroll-triggered counter animation
function animateCounters() {
    const counters = [
        { element: null, target: 1000, suffix: '+', label: 'Happy Birthdays' },
        { element: null, target: 50, suffix: '+', label: 'Communities' },
        { element: null, target: 99, suffix: '%', label: 'Satisfaction' }
    ];
    
    // This would be used if you add counter elements to your HTML
    counters.forEach(counter => {
        if (counter.element) {
            let current = 0;
            const increment = counter.target / 100;
            const timer = setInterval(() => {
                current += increment;
                if (current >= counter.target) {
                    current = counter.target;
                    clearInterval(timer);
                }
                counter.element.textContent = Math.floor(current) + counter.suffix;
            }, 20);
        }
    });
}

// Add keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
        const focusedElement = document.activeElement;
        if (focusedElement.classList.contains('btn')) {
            e.preventDefault();
            focusedElement.click();
        }
    }
});

// Add accessibility improvements
document.querySelectorAll('.btn').forEach(button => {
    button.setAttribute('tabindex', '0');
    button.setAttribute('role', 'button');
});

// Performance optimization - throttle scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Apply throttling to scroll events
window.addEventListener('scroll', throttle(updateScrollProgress, 16));
window.addEventListener('scroll', throttle(requestTick, 16));

// Add dynamic favicon change based on scroll
function updateFavicon() {
    const favicon = document.querySelector('link[rel="icon"]') || document.createElement('link');
    favicon.rel = 'icon';
    favicon.href = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🎂</text></svg>';
    document.head.appendChild(favicon);
}

// Call favicon update on load
updateFavicon();

// Add easter egg - konami code
let konamiCode = [];
const konami = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.keyCode);
    if (konamiCode.length > konami.length) {
        konamiCode.shift();
    }
    
    if (konamiCode.join(',') === konami.join(',')) {
        // Easter egg triggered
        createParticles();
        createParticles();
        alert('🎉 Birthday surprise activated! Extra particles for you!');
        konamiCode = [];
    }
}); 
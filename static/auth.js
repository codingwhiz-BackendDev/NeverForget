 // Particle system
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            
            for (let i = 0; i < 50; i++) {
                setTimeout(() => {
                    const particle = document.createElement('div');
                    particle.className = 'birthday-particle';
                    particle.style.left = Math.random() * 100 + '%';
                    particle.style.animationDelay = Math.random() * 4 + 's';
                    particle.style.animationDuration = (Math.random() * 3 + 2) + 's';
                    particle.style.width = (Math.random() * 8 + 4) + 'px';
                    particle.style.height = particle.style.width;
                    particlesContainer.appendChild(particle);
                    
                    setTimeout(() => {
                        if (particle.parentNode) {
                            particle.parentNode.removeChild(particle);
                        }
                    }, 6000);
                }, i * 80);
            }
        }

        // Start particle animation
        setInterval(createParticles, 3000);
        createParticles();

        // Password toggle functionality
        document.getElementById('togglePassword').addEventListener('click', function() {
            const passwordInput = document.getElementById('password');
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });

        // Form submission
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const container = document.querySelector('.login-container');
            const btn = document.querySelector('.login-btn');
            
            // Add loading state
            container.classList.add('loading');
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing In...';
            
            // Simulate login process
            setTimeout(() => {
                container.classList.remove('loading');
                btn.innerHTML = '<i class="fas fa-check"></i> Success!';
                
                setTimeout(() => {
                    alert('🎉 Login successful! Redirecting to dashboard...');
                    btn.innerHTML = '<i class="fas fa-sign-in-alt"></i> Sign In';
                }, 1500);
            }, 2000);
        });

        // Input focus effects
        document.querySelectorAll('.form-input').forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'scale(1.02)';
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.style.transform = 'scale(1)';
            });
        });

        // Floating shapes parallax effect
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

        // Add ripple CSS
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

        // Add ripple to buttons
        document.querySelectorAll('.login-btn, .social-btn').forEach(button => {
            button.addEventListener('click', createRipple);
        });

        // Add mouse move effect to container
        const container = document.querySelector('.login-container');
        container.addEventListener('mousemove', (e) => {
            const rect = container.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / centerY * 2;
            const rotateY = (centerX - x) / centerX * 2;
            
            container.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });

        container.addEventListener('mouseleave', () => {
            container.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg)';
        });

        // Add dynamic favicon
        function updateFavicon() {
            const favicon = document.querySelector('link[rel="icon"]') || document.createElement('link');
            favicon.rel = 'icon';
            favicon.href = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🎂</text></svg>';
            document.head.appendChild(favicon);
        }

        updateFavicon();
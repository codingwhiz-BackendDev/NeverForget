        // Enhanced particle system
            function createParticles() {
                const particlesContainer = document.getElementById("particles")

                for (let i = 0; i < 60; i++) {
                    setTimeout(() => {
                        const particle = document.createElement("div")
                        particle.className = "birthday-particle"
                        particle.style.left = Math.random() * 100 + "%"
                        particle.style.animationDelay = Math.random() * 4 + "s"
                        particle.style.animationDuration = Math.random() * 3 + 2 + "s"
                        particle.style.width = Math.random() * 10 + 5 + "px"
                        particle.style.height = particle.style.width
                        particlesContainer.appendChild(particle)

                        setTimeout(() => {
                            if (particle.parentNode) {
                                particle.parentNode.removeChild(particle)
                            }
                        }, 6000)
                    }, i * 50)
                }
            }

            // Scroll progress bar
            function updateScrollProgress() {
                const scrollProgress = document.getElementById("scroll-progress")
                const scrollTop = window.pageYOffset
                const docHeight = document.documentElement.scrollHeight - window.innerHeight
                const scrollPercent = (scrollTop / docHeight) * 100
                scrollProgress.style.width = scrollPercent + "%"
            }

            // Continuous particle generation
            setInterval(createParticles, 3000)
            createParticles()

            // Enhanced parallax effect for floating shapes
            let ticking = false
            function updateParallax() {
                const scrolled = window.pageYOffset
                const shapes = document.querySelectorAll(".floating-shapes .shape")

                shapes.forEach((shape, index) => {
                    const speed = 0.2 + index * 0.05
                    const yPos = -(scrolled * speed)
                    shape.style.transform = `translateY(${yPos}px) rotate(${scrolled * 0.05}deg)`
                })

                ticking = false
            }

            function requestTick() {
                if (!ticking) {
                    requestAnimationFrame(updateParallax)
                    ticking = true
                }
            }

            // Enhanced intersection observer for staggered animations
            const observerOptions = {
                threshold: 0.1,
                rootMargin: "0px 0px -50px 0px",
            }

            const observer = new IntersectionObserver((entries) => {
                entries.forEach((entry, index) => {
                    if (entry.isIntersecting) {
                        setTimeout(() => {
                            entry.target.style.animation = "fadeInUp 0.8s ease-out forwards"
                            entry.target.style.opacity = "1"
                            entry.target.style.transform = "translateY(0)"
                        }, index * 100)
                    }
                })
            }, observerOptions)

            // Observe all cards
            document.querySelectorAll(".stat-card, .birthday-item, .member-card").forEach((card) => {
                card.style.opacity = "0"
                card.style.transform = "translateY(30px)"
                observer.observe(card)
            })

            // Modal functions with enhanced animations
            function addBirthday() {
                const modal = document.getElementById("addBirthdayModal")
                modal.style.display = "block" 

                // Add entrance animation
                const modalContent = modal.querySelector(".modal-content")
                modalContent.style.animation = "modalSlideIn 0.4s ease-out"

                // Focus on first input
                setTimeout(() => {
                    document.getElementById("personName").focus()
                }, 100)
            }

            function closeModal() {
                const modal = document.getElementById("addBirthdayModal")
                const modalContent = modal.querySelector(".modal-content")

                modalContent.style.animation = "modalSlideOut 0.3s ease-in"
                setTimeout(() => {
                    modal.style.display = "none"
                }, 300)
            }

            // Enhanced notification system
            function toggleNotifications() {
                const badge = document.querySelector(".notification-badge")
                const bellIcon = document.querySelector(".btn-icon i")

                // Animate notification bell
                bellIcon.style.animation = "shake 0.5s ease-in-out"

                // Create notification panel (simulated)
                showNotificationPanel()

                // Reset animation
                setTimeout(() => {
                    bellIcon.style.animation = ""
                }, 500)
            }

            // Function to toggle the profile menu panel
            function toggleProfileMenu() {
                const profileToggle = document.querySelector(".profile-toggle");
                const profilePic = profileToggle.querySelector(".profile-pic");

                // Animate profile pic (re-using shake animation)
                profilePic.style.animation = "shake 0.5s ease-in-out";

                showProfilePanel(); // Call the function to show/hide the panel

                // Reset animation after it completes
                setTimeout(() => {
                    profilePic.style.animation = "";
                }, 500);
            }
            function showProfilePanel() {
                let panel = document.getElementById("profilePanel");

                if (!panel) {
                    // Create the panel if it doesn't exist
                    panel = document.createElement("div");
                    panel.id = "profilePanel";
                    panel.className = "profile-panel";
                    panel.innerHTML = `
                        <div class="profile-header">
                            <h3><i class="fas fa-user-circle"></i> My Profile</h3>
                            <button onclick="this.parentElement.parentElement.remove()" class="close-btn">&times;</button>
                        </div>
                        <div class="profile-list">
                            <a href="#"><i class="fas fa-user"></i> Profile</a>
                            <a href="#"><i class="fas fa-cog"></i> Settings</a>
                            <a href="#"><i class="fas fa-share-alt"></i> Share Link</a>
                            <a href="logout"><i class="fas fa-sign-out-alt"></i> Logout</a>
                        </div>
                    `;
                    document.body.appendChild(panel);
                    panel.style.display = "block";
                    panel.style.animation = "slideInRight 0.3s ease-out";
                } else {
                    // Toggle visibility if panel already exists
                    if (panel.style.display === "block") {
                        panel.style.animation = "modalSlideOut 0.3s ease-in";
                        setTimeout(() => {
                            panel.style.display = "none";
                            panel.remove(); // Remove from DOM after animation
                        }, 300);
                    } else {
                        panel.style.display = "block";
                        panel.style.animation = "slideInRight 0.3s ease-out";
                    }
                }
            }
// Function to show/hide the profile panel
function showProfilePanel() {
    let panel = document.getElementById("profilePanel");

    if (!panel) {
        // Create the panel if it doesn't exist
        panel = document.createElement("div");
        panel.id = "profilePanel";
        panel.className = "profile-panel";
        panel.innerHTML = `
            <div class="profile-header">
                <h3><i class="fas fa-user-circle"></i> My Profile</h3>
                <button onclick="this.parentElement.parentElement.remove()" class="close-btn">&times;</button>
            </div>
            <div class="profile-list">
                <a href="#"><i class="fas fa-user"></i> Profile</a>
                <a href="#"><i class="fas fa-cog"></i> Settings</a>
                <a href="#"><i class="fas fa-share-alt"></i> Share Link</a>
                <a href="logout"><i class="fas fa-sign-out-alt"></i> Logout</a>
            </div>
        `;
        document.body.appendChild(panel);
        panel.style.display = "block";
        panel.style.animation = "slideInRight 0.3s ease-out";
    } else {
        // Toggle visibility if panel already exists
        if (panel.style.display === "block") {
            panel.style.animation = "modalSlideOut 0.3s ease-in";
            setTimeout(() => {
                panel.style.display = "none";
                panel.remove(); // Remove from DOM after animation
            }, 300);
        } else {
            panel.style.display = "block";
            panel.style.animation = "slideInRight 0.3s ease-out";
        }
    }
}

// --- IMPORTANT: Update your existing functions ---

// Modify showNotificationPanel to use an ID and remove itself
function showNotificationPanel() {
    let panel = document.getElementById("notificationPanel"); // Give it an ID
    if (!panel) {
        panel = document.createElement("div");
        panel.id = "notificationPanel"; // Assign ID
        panel.className = "notification-panel";
        panel.innerHTML = `
            <div class="notification-header">
                <h3><i class="fas fa-bell"></i> Notifications</h3>
                <button onclick="this.parentElement.parentElement.remove()" class="close-btn">&times;</button>
            </div>
            <div class="notification-list">
                <div class="notification-item">
                    <i class="fas fa-birthday-cake"></i>
                    <div class="notification-content">
                        <h4>Sarah's Birthday Today!</h4>
                        <p>Don't forget to wish her happy birthday</p>
                    </div>
                </div>
                <div class="notification-item">
                    <i class="fas fa-bell"></i>
                    <div class="notification-content">
                        <h4>Mike's Birthday Tomorrow</h4>
                        <p>Reminder: Mike turns 32 tomorrow</p>
                    </div>
                </div>
                <div class="notification-item">
                    <i class="fas fa-users"></i>
                    <div class="notification-content">
                        <h4>New Member Joined</h4>
                        <p>Lisa Wang joined the community</p>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(panel);
        panel.style.display = "block"; // Show it
        panel.style.animation = "slideInRight 0.3s ease-out";
    } else {
        // Toggle visibility if panel already exists
        if (panel.style.display === "block") {
            panel.style.animation = "modalSlideOut 0.3s ease-in"; // Re-use modalSlideOut for closing
            setTimeout(() => {
                panel.style.display = "none";
                panel.remove(); // Remove from DOM after animation
            }, 300);
        } else {
            panel.style.display = "block";
            panel.style.animation = "slideInRight 0.3s ease-out";
        }
    }
}

            // Enhanced view toggle for members
            function initViewToggle() {
                const toggleBtns = document.querySelectorAll(".toggle-btn")
                const membersContainer = document.getElementById("membersContainer")

                toggleBtns.forEach((btn) => {
                    btn.addEventListener("click", () => {
                        toggleBtns.forEach((b) => b.classList.remove("active"))
                        btn.classList.add("active")

                        const view = btn.dataset.view
                        membersContainer.style.transition = "all 0.3s ease"

                        if (view === "list") {
                            membersContainer.style.gridTemplateColumns = "1fr"
                            membersContainer.classList.add("list-view")
                        } else {
                            membersContainer.style.gridTemplateColumns = "repeat(auto-fill, minmax(250px, 1fr))"
                            membersContainer.classList.remove("list-view")
                        }
                    })
                })
            }

             
              

            function createCelebrationEffect(button) {
                const rect = button.getBoundingClientRect()
                const centerX = rect.left + rect.width / 2
                const centerY = rect.top + rect.height / 2

                // Create confetti burst
                for (let i = 0; i < 20; i++) {
                    const confetti = document.createElement("div")
                    confetti.style.position = "fixed"
                    confetti.style.left = centerX + "px"
                    confetti.style.top = centerY + "px"
                    confetti.style.width = "6px"
                    confetti.style.height = "6px"
                    confetti.style.backgroundColor = ["#ff6b6b", "#ffd700", "#98fb98", "#00bfff", "#ff69b4"][
                        Math.floor(Math.random() * 5)
                    ]
                    confetti.style.borderRadius = "50%"
                    confetti.style.pointerEvents = "none"
                    confetti.style.zIndex = "9999"

                    const angle = (Math.PI * 2 * i) / 20
                    const velocity = 100 + Math.random() * 100
                    const vx = Math.cos(angle) * velocity
                    const vy = Math.sin(angle) * velocity

                    confetti.style.animation = `confetti-${i} 1s ease-out forwards`

                    // Create unique animation for each confetti
                    const style = document.createElement("style")
                    style.textContent = `
            @keyframes confetti-${i} {
                0% { transform: translate(0, 0) rotate(0deg); opacity: 1; }
                100% { transform: translate(${vx}px, ${vy + 200}px) rotate(720deg); opacity: 0; }
            }
        `
                    document.head.appendChild(style)

                    document.body.appendChild(confetti)

                    setTimeout(() => {
                        confetti.remove()
                        style.remove()
                    }, 1000)
                }
            }

            

            // Add ripple effect to buttons
            function createRipple(event) {
                const button = event.currentTarget
                const circle = document.createElement("span")
                const diameter = Math.max(button.clientWidth, button.clientHeight)
                const radius = diameter / 2

                circle.style.width = circle.style.height = `${diameter}px`
                circle.style.left = `${event.clientX - button.offsetLeft - radius}px`
                circle.style.top = `${event.clientY - button.offsetTop - radius}px`
                circle.classList.add("ripple")

                const ripple = button.getElementsByClassName("ripple")[0]
                if (ripple) {
                    ripple.remove()
                }

                button.appendChild(circle)

                setTimeout(() => {
                    circle.remove()
                }, 600)
            }

            // Enhanced stats animation
            function animateStats() {
                const statNumbers = document.querySelectorAll(".stat-info h3")

                statNumbers.forEach((stat) => {
                    const target = Number.parseInt(stat.textContent)
                    let current = 0
                    const increment = target / 50

                    const timer = setInterval(() => {
                        current += increment
                        if (current >= target) {
                            current = target
                            clearInterval(timer)
                        }
                        stat.textContent = Math.floor(current)
                    }, 30)
                })
            }

            // Keyboard navigation
            document.addEventListener("keydown", (e) => {
                if (e.key === "Escape") {
                    closeModal()
                }

                if (e.key === "Enter" || e.key === " ") {
                    const focusedElement = document.activeElement
                    if (focusedElement.classList.contains("btn")) {
                        e.preventDefault()
                        focusedElement.click()
                    }
                }
            })

            // Performance optimization - throttle scroll events
            function throttle(func, limit) {
                let inThrottle
                return function () {
                    const args = arguments

                    if (!inThrottle) {
                        func.apply(this, args)
                        inThrottle = true
                        setTimeout(() => (inThrottle = false), limit)
                    }
                }
            }

            // Close modal when clicking outside
            window.addEventListener("click", (e) => {
                const modal = document.getElementById("addBirthdayModal")
                if (e.target === modal) {
                    closeModal()
                }
            })

            // Add dynamic styles for enhanced effects
            const enhancedStyles = document.createElement("style")
            enhancedStyles.textContent = `
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
    
    @keyframes shake {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(-10deg); }
        75% { transform: rotate(10deg); }
    }
    
    @keyframes modalSlideOut {
        from {
            transform: translateY(0);
            opacity: 1;
        }
        to {
            transform: translateY(-50px);
            opacity: 0;
        }
    }
    
    .notification-panel {
        position: fixed;
        top: 80px;
        right: 20px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 15px;
        padding: 1rem;
        min-width: 300px;
        max-width: 400px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        z-index: 2000;
        animation: slideInRight 0.3s ease-out;
    }
    
    .notification-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .notification-header h3 {
        color: white;
        font-size: 1.1rem;
        margin: 0;
    }
    
    .notification-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.8rem;
        margin-bottom: 0.5rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .notification-item:hover {
        background: rgba(255, 255, 255, 0.1);
    }
    
    .notification-item i {
        color: #ffd700;
        font-size: 1.2rem;
    }
    
    .notification-content h4 {
        color: white;
        margin: 0 0 0.2rem 0;
        font-size: 0.9rem;
    }
    
    .notification-content p {
        color: rgba(255, 255, 255, 0.8);
        margin: 0;
        font-size: 0.8rem;
    }
    
    .toast-notification {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(45deg, #98fb98, #00ff7f);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 500;
        z-index: 2000;
        animation: slideInUp 0.3s ease-out;
    }
    
    .list-view .member-card {
        display: flex;
        align-items: center;
        text-align: left;
        padding: 1rem;
    }
    
    .list-view .member-avatar {
        margin-bottom: 0;
        margin-right: 1rem;
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideInUp {
        from {
            transform: translateY(100%);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateY(0);
            opacity: 1;
        }
        to {
            transform: translateY(-100%);
            opacity: 0;
        }
    }
`

            document.head.appendChild(enhancedStyles)

            // Initialize everything when page loads
            document.addEventListener("DOMContentLoaded", () => {
                initViewToggle()  

                // Add scroll event listeners with throttling
                window.addEventListener("scroll", throttle(updateScrollProgress, 16))
                window.addEventListener("scroll", throttle(requestTick, 16))

                // Add ripple effect to all buttons
                document.querySelectorAll(".btn, .btn-small").forEach((button) => {
                    button.addEventListener("click", createRipple)
                    button.setAttribute("tabindex", "0")
                    button.setAttribute("role", "button")
                })

                // Animate stats on load
                setTimeout(animateStats, 500)

                // Add entrance animations with staggered timing
                const cards = document.querySelectorAll(".stat-card, .birthday-item, .member-card")
                cards.forEach((card, index) => {
                    card.style.animationDelay = index * 0.1 + "s"
                })

                // Profile menu dropdown logic
                const userMenu = document.querySelector('.user-menu');
                if (userMenu) {
                    userMenu.addEventListener('click', function(event) {
                        event.stopPropagation(); // Prevents the window.onclick from closing it immediately
                        document.getElementById("profileDropdown").classList.toggle("show");
                    });
                }
            })
            
            // Close the dropdown menu if the user clicks outside of it
            window.onclick = function(event) {
                // Check if the click was outside the user-menu area
                if (!event.target.closest('.user-menu')) {
                    var dropdowns = document.getElementsByClassName("dropdown");
                    for (var i = 0; i < dropdowns.length; i++) {
                        var openDropdown = dropdowns[i];
                        if (openDropdown.classList.contains('show')) {
                            openDropdown.classList.remove('show');
                        }
                    }
                }
            }


            // Easter egg - konami code
            let konamiCode = []
            const konami = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]

            document.addEventListener("keydown", (e) => {
                konamiCode.push(e.keyCode)
                if (konamiCode.length > konami.length) {
                    konamiCode.shift()
                }

                if (konamiCode.join(",") === konami.join(",")) {
                    // Easter egg triggered - birthday party mode!
                    createParticles()
                    createParticles()
                    createParticles()

                    // Change background temporarily
                    document.body.style.background = "linear-gradient(135deg, #ff6b6b 0%, #ffd700 50%, #98fb98 100%)"

                    // Show party message
                    const partyMessage = document.createElement("div")
                    partyMessage.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            padding: 2rem;
            border-radius: 20px;
            color: white;
            font-size: 1.5rem;
            text-align: center;
            z-index: 9999;
            animation: modalSlideIn 0.5s ease-out;
        `
                    partyMessage.innerHTML = `
            <h2>🎉 PARTY MODE ACTIVATED! 🎉</h2>
            <p>It's celebration time!</p>
        `

                    document.body.appendChild(partyMessage)

                    setTimeout(() => {
                        partyMessage.remove()
                        document.body.style.background = "linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)"
                    }, 3000)

                    konamiCode = []
                }
            })
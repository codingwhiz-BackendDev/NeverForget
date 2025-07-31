// Enhanced particle system
function createParticles() {
    const particlesContainer = document.getElementById("particles");

    for (let i = 0; i < 60; i++) {
        setTimeout(() => {
            const particle = document.createElement("div");
            particle.className = "birthday-particle";
            particle.style.left = Math.random() * 100 + "%";
            particle.style.animationDelay = Math.random() * 4 + "s";
            particle.style.animationDuration = Math.random() * 3 + 2 + "s";
            particle.style.width = Math.random() * 10 + 5 + "px";
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
    const scrollProgress = document.getElementById("scroll-progress");
    const scrollTop = window.pageYOffset;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;
    scrollProgress.style.width = scrollPercent + "%";
}

// Continuous particle generation
setInterval(createParticles, 3000);
createParticles();

// Enhanced intersection observer for staggered animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            setTimeout(() => {
                entry.target.style.animation = "fadeInUp 0.8s ease-out forwards";
                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0)";
            }, index * 100);
        }
    });
}, observerOptions);

// Observe all cards
document.querySelectorAll(".dashboard-card, .info-card").forEach((card) => {
    card.style.opacity = "0";
    card.style.transform = "translateY(30px)";
    observer.observe(card);
});

// Profile Functions
function editProfile() {
    const modal = document.getElementById("editProfileModal");
    modal.style.display = "block";

    // Add entrance animation
    const modalContent = modal.querySelector(".modal-content");
    modalContent.style.animation = "modalSlideIn 0.4s ease-out";

    // Focus on first input
    setTimeout(() => {
        document.getElementById("editFullName").focus();
    }, 100);
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    const modalContent = modal.querySelector(".modal-content");

    modalContent.style.animation = "modalSlideOut 0.3s ease-in";
    setTimeout(() => {
        modal.style.display = "none";
    }, 300);
}

function changeProfilePhoto() {
    // Create file input
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = "image/*";
    fileInput.style.display = "none";

    fileInput.onchange = function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById("profileImage").src = e.target.result;
                showToast("Profile photo updated successfully!", "success");
            };
            reader.readAsDataURL(file);
        }
    };

    document.body.appendChild(fileInput);
    fileInput.click();
    document.body.removeChild(fileInput);
}

function shareProfile() {
     
    const username = document.getElementById('admin-data').dataset.username;

    const profileUrl = `${window.location.origin}/profile/${username}`;

    if (navigator.share) {
        navigator.share({
            title: 'NeverForget - Admin Profile',
            text: 'Check out my admin profile on NeverForget!',
            url: profileUrl
        });
    } else {
        navigator.clipboard.writeText(profileUrl).then(() => {
            showToast("Profile link copied to clipboard!", "success");
        });
    }
}


function goHome() {
    window.location.href = "/home"; 
}

// Dashboard Functions
function refreshCommunityData() {
    const refreshBtn = document.querySelector(".btn-icon-small");
    const icon = refreshBtn.querySelector("i");
    
    // Add spinning animation
    icon.style.animation = "rotateIcon 1s linear infinite";
    
    // Simulate data refresh
    setTimeout(() => {
        icon.style.animation = "";
        showToast("Community data refreshed!", "success");
        
        // Update some numbers (simulate real data)
        const statNumbers = document.querySelectorAll(".overview-info h4");
        statNumbers.forEach(stat => {
            const currentValue = parseInt(stat.textContent);
            const newValue = currentValue + Math.floor(Math.random() * 5);
            animateNumber(stat, currentValue, newValue);
        });
    }, 1500);
}

function viewAllActivity() {
    showToast("Redirecting to activity log...", "info");
    // In a real app, this would navigate to a detailed activity page
}

function addNewMember() {
    showToast("Opening member registration form...", "info");
    // In a real app, this would open a member registration modal
}

function sendReminders() {
    showToast("Sending birthday reminders...", "info");
    
    // Simulate sending reminders
    setTimeout(() => {
        showToast("Reminders sent to 12 members!", "success");
    }, 2000);
}
 

 

function editPersonalInfo() {
    editProfile(); // Reuse the edit profile modal
}

// Notification Functions
function toggleNotifications() {
    const badge = document.querySelector(".notification-badge");
    const bellIcon = document.querySelector(".btn-icon i");

    // Animate notification bell
    bellIcon.style.animation = "shake 0.5s ease-in-out";

    // Create notification panel
    showNotificationPanel();

    // Reset animation
    setTimeout(() => {
        bellIcon.style.animation = "";
    }, 500);
}

function showNotificationPanel() {
    let panel = document.getElementById("notificationPanel");
    
    if (!panel) {
        panel = document.createElement("div");
        panel.id = "notificationPanel";
        panel.className = "notification-panel";
        panel.innerHTML = `
            <div class="notification-header">
                <h3><i class="fas fa-bell"></i> Admin Notifications</h3>
                <button onclick="this.parentElement.parentElement.remove()" class="close-btn">&times;</button>
            </div>
            <div class="notification-list">
                <div class="notification-item">
                    <i class="fas fa-user-plus"></i>
                    <div class="notification-content">
                        <h4>New Member Request</h4>
                        <p>Sarah Johnson wants to join the community</p>
                        <span class="notification-time">5 minutes ago</span>
                    </div>
                </div>
                <div class="notification-item">
                    <i class="fas fa-birthday-cake"></i>
                    <div class="notification-content">
                        <h4>Birthday Alert</h4>
                        <p>3 birthdays coming up this week</p>
                        <span class="notification-time">1 hour ago</span>
                    </div>
                </div>
                <div class="notification-item">
                    <i class="fas fa-exclamation-triangle"></i>
                    <div class="notification-content">
                        <h4>System Update</h4>
                        <p>Scheduled maintenance tonight at 2 AM</p>
                        <span class="notification-time">3 hours ago</span>
                    </div>
                </div>
                <div class="notification-item">
                    <i class="fas fa-chart-line"></i>
                    <div class="notification-content">
                        <h4>Monthly Report</h4>
                        <p>Community statistics report is ready</p>
                        <span class="notification-time">1 day ago</span>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(panel);
        panel.style.display = "block";
        panel.style.animation = "slideInRight 0.3s ease-out";
    } else {
        if (panel.style.display === "block") {
            panel.style.animation = "modalSlideOut 0.3s ease-in";
            setTimeout(() => {
                panel.style.display = "none";
                panel.remove();
            }, 300);
        } else {
            panel.style.display = "block";
            panel.style.animation = "slideInRight 0.3s ease-out";
        }
    }
}

function toggleProfileMenu() {
    const profileToggle = document.querySelector(".profile-toggle");
    const profilePic = profileToggle.querySelector(".profile-pic");

    // Animate profile pic
    profilePic.style.animation = "shake 0.5s ease-in-out";

    showProfilePanel();

    // Reset animation
    setTimeout(() => {
        profilePic.style.animation = "";
    }, 500);
}

function showProfilePanel() {
    let panel = document.getElementById("profilePanel");

    if (!panel) {
        panel = document.createElement("div");
        panel.id = "profilePanel";
        panel.className = "profile-panel";
        panel.innerHTML = `
            <div class="profile-header">
                <h3><i class="fas fa-user-circle"></i> Admin Menu</h3>
                <button onclick="this.parentElement.parentElement.remove()" class="close-btn">&times;</button>
            </div>
            <div class="profile-list">
                <a href="#" onclick="editProfile()"><i class="fas fa-user-edit"></i> Edit Profile</a>  
                <a href="#" onclick="shareProfile()"><i class="fas fa-share-alt"></i> Share Profile</a>
                <a href="logout"><i class="fas fa-sign-out-alt"></i> Logout</a>
            </div>
        `;
        document.body.appendChild(panel);
        panel.style.display = "block";
        panel.style.animation = "slideInRight 0.3s ease-out";
    } else {
        if (panel.style.display === "block") {
            panel.style.animation = "modalSlideOut 0.3s ease-in";
            setTimeout(() => {
                panel.style.display = "none";
                panel.remove();
            }, 300);
        } else {
            panel.style.display = "block";
            panel.style.animation = "slideInRight 0.3s ease-out";
        }
    }
}
 

 

// Utility Functions
function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = `toast-notification ${type}`;
    
    const icon = type === "success" ? "fas fa-check-circle" : 
                 type === "error" ? "fas fa-exclamation-circle" : 
                 "fas fa-info-circle";
    
    toast.innerHTML = `
        <i class="${icon}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(toast);
    
    // Remove toast after 3 seconds
    setTimeout(() => {
        toast.style.animation = "slideOut 0.3s ease-in";
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 3000);
}

function animateNumber(element, start, end) {
    const duration = 1000;
    const startTime = performance.now();
    
    function updateNumber(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (end - start) * progress);
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }
    
    requestAnimationFrame(updateNumber);
}

// // Form Handling
// document.addEventListener("DOMContentLoaded", function() {
//     const editForm = document.getElementById("editProfileForm");
//     if (editForm) {
//         editForm.addEventListener("submit", function(e) {
//             e.preventDefault();
            
//             // Get form data
//             const formData = new FormData(editForm);
//             const fullName = formData.get("editFullName") || document.getElementById("editFullName").value;
//             const email = formData.get("editEmail") || document.getElementById("editEmail").value;
//             const phone = formData.get("editPhone") || document.getElementById("editPhone").value;
//             const birthday = formData.get("editBirthday") || document.getElementById("editBirthday").value;
//             const timezone = formData.get("editTimezone") || document.getElementById("editTimezone").value;
            
//             // Update profile information
//             document.getElementById("profileName").textContent = fullName;
//             document.getElementById("fullName").textContent = fullName;
//             document.getElementById("emailAddress").textContent = email;
//             document.getElementById("phoneNumber").textContent = phone;
            
//             // Format and update birthday
//             if (birthday) {
//                 const date = new Date(birthday);
//                 const options = { year: 'numeric', month: 'long', day: 'numeric' };
//                 document.getElementById("birthday").textContent = date.toLocaleDateString('en-US', options);
//             }
            
//             document.getElementById("timeZone").textContent = timezone;
            
//             // Close modal and show success message
//             closeModal("editProfileModal");
//             showToast("Profile updated successfully!", "success");
//         });
//     }
// });

// Performance optimization - throttle scroll events
function throttle(func, limit) {
    let inThrottle;
    return function () {
        const args = arguments;
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => (inThrottle = false), limit);
        }
    };
}

// Add scroll event listeners with throttling
window.addEventListener("scroll", throttle(updateScrollProgress, 16));

// Close modal when clicking outside
window.addEventListener("click", (e) => {
    const modals = document.querySelectorAll(".modal");
    modals.forEach(modal => {
        if (e.target === modal) {
            const modalId = modal.id;
            closeModal(modalId);
        }
    });
});

// Keyboard navigation
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        // Close any open modals
        const openModals = document.querySelectorAll(".modal[style*='display: block']");
        openModals.forEach(modal => {
            closeModal(modal.id);
        });
        
        // Close any open panels
        const openPanels = document.querySelectorAll("#profilePanel, #notificationPanel");
        openPanels.forEach(panel => {
            panel.remove();
        });
    }
});

// Add ripple effect to buttons
function createRipple(event) {
    const button = event.currentTarget;
    const circle = document.createElement("span");
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
    circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
    circle.classList.add("ripple");

    const ripple = button.getElementsByClassName("ripple")[0];
    if (ripple) {
        ripple.remove();
    }

    button.appendChild(circle);

    setTimeout(() => {
        circle.remove();
    }, 600);
}

// Add dynamic styles for enhanced effects
const enhancedStyles = document.createElement("style");
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
    
    .notification-panel {
        position: fixed;
        top: 80px;
        right: 20px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 15px;
        padding: 1rem;
        min-width: 350px;
        max-width: 400px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        z-index: 2000;
        animation: slideInRight 0.3s ease-out;
        max-height: 500px;
        overflow-y: auto;
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
        align-items: flex-start;
        gap: 1rem;
        padding: 1rem;
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
        margin-top: 0.2rem;
    }
    
    .notification-content h4 {
        color: white;
        margin: 0 0 0.3rem 0;
        font-size: 0.95rem;
    }
    
    .notification-content p {
        color: rgba(255, 255, 255, 0.8);
        margin: 0 0 0.3rem 0;
        font-size: 0.85rem;
    }
    
    .notification-time {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.75rem;
    }
    
    .profile-panel {
        position: fixed;
        top: 80px;
        right: 20px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 15px;
        padding: 1rem;
        min-width: 250px;
        max-width: 300px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        z-index: 2000;
        animation: slideInRight 0.3s ease-out;
    }
    
    .profile-panel .profile-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .profile-panel .profile-header h3 {
        color: white;
        font-size: 1.1rem;
        margin: 0;
    }
    
    .profile-panel .profile-list a {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.8rem;
        margin-bottom: 0.5rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        transition: all 0.3s ease;
        color: white;
        text-decoration: none;
    }
    
    .profile-panel .profile-list a:hover {
        background: rgba(255, 255, 255, 0.1);
    }
    
    .profile-panel .profile-list a i {
        color: #ffd700;
        font-size: 1.1rem;
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
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .toast-notification.error {
        background: linear-gradient(45deg, #ff6b6b, #ff4757);
    }
    
    .toast-notification.info {
        background: linear-gradient(45deg, #00bfff, #1e90ff);
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
`;

document.head.appendChild(enhancedStyles);

// Initialize everything when page loads
document.addEventListener("DOMContentLoaded", () => {
    // Add ripple effect to all buttons
    document.querySelectorAll(".btn, .btn-secondary, .quick-action-btn").forEach((button) => {
        button.addEventListener("click", createRipple);
        button.setAttribute("tabindex", "0");
        button.setAttribute("role", "button");
    });

    // Add entrance animations with staggered timing
    const cards = document.querySelectorAll(".dashboard-card, .info-card");
    cards.forEach((card, index) => {
        card.style.animationDelay = index * 0.1 + "s";
    });

    // Initialize toggle switches
    const toggleSwitches = document.querySelectorAll('.toggle-switch input');
    toggleSwitches.forEach(toggle => {
        toggle.addEventListener('change', function() {
            const settingName = this.closest('.setting-item').querySelector('h4').textContent;
            const status = this.checked ? 'enabled' : 'disabled';
            showToast(`${settingName} ${status}`, 'info');
        });
    });
});
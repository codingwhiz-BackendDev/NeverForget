// Enhanced particle system
function createParticles() {
  // Create particles container if it doesn't exist
  let particlesContainer = document.querySelector(".birthday-animation")
  if (!particlesContainer) {
    particlesContainer = document.createElement("div")
    particlesContainer.className = "birthday-animation"
    document.body.appendChild(particlesContainer)
  }

  for (let i = 0; i < 40; i++) {
    setTimeout(() => {
      const particle = document.createElement("div")
      particle.className = "birthday-particle"
      particle.style.left = Math.random() * 100 + "%"
      particle.style.animationDelay = Math.random() * 4 + "s"
      particle.style.animationDuration = Math.random() * 3 + 2 + "s"
      particle.style.width = Math.random() * 8 + 4 + "px"
      particle.style.height = particle.style.width
      particlesContainer.appendChild(particle)

      setTimeout(() => {
        if (particle.parentNode) {
          particle.parentNode.removeChild(particle)
        }
      }, 6000)
    }, i * 100)
  }
}

// Toast notification system
function showToast(message, type = "info", duration = 3000) {
  const toast = document.createElement("div")
  toast.className = `toast ${type}`

  const icon = type === "success" ? "✓" : type === "error" ? "✗" : "ℹ"
  toast.innerHTML = `<span>${icon}</span><span>${message}</span>`

  document.body.appendChild(toast)

  setTimeout(() => {
    toast.style.animation = "toastSlideOut 0.3s ease-in"
    setTimeout(() => toast.remove(), 300)
  }, duration)
}

// Form validation
function validateField(field) {
  const value = field.value.trim()
  const fieldName = field.name
  let isValid = true
  let errorMessage = ""

  // Remove existing error/success states
  field.classList.remove("field-error", "field-success")
  const existingMessage = field.parentNode.querySelector(".error-message, .success-message")
  if (existingMessage) {
    existingMessage.remove()
  }

  // Validation rules
  switch (fieldName) {
    case "personName":
      if (value.length < 2) {
        isValid = false
        errorMessage = "Name must be at least 2 characters long"
      }
      break

    case "email":
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (value && !emailRegex.test(value)) {
        isValid = false
        errorMessage = "Please enter a valid email address"
      }
      break

    case "phoneNumber":
      const phoneRegex = /^[+]?[0-9\s\-$$$$]{10,}$/
      if (value && !phoneRegex.test(value)) {
        isValid = false
        errorMessage = "Please enter a valid phone number"
      }
      break

    case "matric":
      if (value && value.length < 3) {
        isValid = false
        errorMessage = "Matric number seems too short"
      }
      break

    case "level":
      const level = Number.parseInt(value)
      if (value && (level < 100 || level > 800)) {
        isValid = false
        errorMessage = "Level should be between 100 and 800"
      }
      break

    case "birthDate":
      if (value) {
        const birthDate = new Date(value)
        const today = new Date()
        const age = today.getFullYear() - birthDate.getFullYear()
        if (age < 10 || age > 100) {
          isValid = false
          errorMessage = "Please enter a valid birth date"
        }
      }
      break
  }

  // Apply validation state
  if (!isValid) {
    field.classList.add("field-error")
    const errorDiv = document.createElement("div")
    errorDiv.className = "error-message"
    errorDiv.textContent = errorMessage
    field.parentNode.appendChild(errorDiv)
  } else if (value) {
    field.classList.add("field-success")
    const successDiv = document.createElement("div")
    successDiv.className = "success-message"
    successDiv.textContent = "✓ Looks good!"
    field.parentNode.appendChild(successDiv)
  }

  return isValid
}

// Enhanced edit/save functionality
function initializeProfileForm() {
  const editBtn = document.getElementById("editBtn")
  const cancelBtn = document.getElementById("cancelBtn")
  const saveBtn = document.getElementById("saveBtn")
  const form = document.getElementById("profileForm")
  const inputs = form.querySelectorAll("input, select")

  let isEditing = false

  // Add field labels
  addFieldLabels()

  // Edit button click
  editBtn.addEventListener("click", () => {
    if (!isEditing) {
      enterEditMode()
    } else {
      exitEditMode()
    }
  })

  
  cancelBtn.addEventListener("click", () =>{
    window.location.href = "/home"
  })
  
  // Save button click
  saveBtn.addEventListener("click", (e) => {
    e.preventDefault()
    saveProfile()
  })

  function enterEditMode() {
    isEditing = true

    // Enable all inputs
    inputs.forEach((input) => {
      input.removeAttribute("readonly")
      input.removeAttribute("disabled")
      input.style.animation = "pulse 0.5s ease-out"
    })

    // Update buttons
    editBtn.innerHTML = '<i class="fas fa-times"></i> Cancel'
    editBtn.style.background = "linear-gradient(45deg, #ff6b6b, #ff4757)"
    saveBtn.style.display = "inline-flex"
    cancelBtn.style.display = 'none'

    // Add real-time validation
    inputs.forEach((input) => {
      input.addEventListener("input", () => validateField(input))
      input.addEventListener("blur", () => validateField(input))
    })

    // Show edit mode toast
    showToast("Edit mode enabled! Make your changes and click Save.", "info")

    // Add glow effect to profile image
    const profileImg = document.querySelector(".profile-image img")
    profileImg.style.animation = "glow 2s ease-in-out infinite"
  }

  function exitEditMode() {
    isEditing = false

    // Disable all inputs
    inputs.forEach((input) => {
      input.setAttribute("readonly", "true")
      if (input.tagName === "SELECT") {
        input.setAttribute("disabled", "true")
      }
      input.classList.remove("field-error", "field-success")
      input.style.animation = ""
    })

    // Clear validation messages
    document.querySelectorAll(".error-message, .success-message").forEach((msg) => msg.remove())

    // Update buttons
    editBtn.innerHTML = '<i class="fas fa-edit"></i> Edit'
    editBtn.style.background = "linear-gradient(45deg, #ff6b6b, #ffa500, #ff1493)"
    saveBtn.style.display = "none"

    // Remove glow effect
    const profileImg = document.querySelector(".profile-image img")
    profileImg.style.animation = "profileImageFloat 3s ease-in-out infinite"

    showToast("Edit mode cancelled", "info")
  }

  function saveProfile() {
    // Validate all fields
    let isFormValid = true
    inputs.forEach((input) => {
      if (!validateField(input)) {
        isFormValid = false
      }
    })

    if (!isFormValid) {
      showToast("Please fix the errors before saving", "error")
      return
    }

    // Show loading state
    saveBtn.classList.add("loading")
    saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...'

    // Simulate API call
    setTimeout(() => {
      // Success state
      saveBtn.classList.remove("loading")
      saveBtn.classList.add("success")
      saveBtn.innerHTML = '<i class="fas fa-check"></i> Saved!'

      // Create celebration effect
      createCelebrationEffect(saveBtn)

      // Exit edit mode after delay
      setTimeout(() => {
        exitEditMode()
        saveBtn.classList.remove("success")
        saveBtn.innerHTML = '<i class="fas fa-save"></i> Save'
        showToast("Profile updated successfully!", "success")

        // Submit the actual form
        form.submit()
      }, 1500)
    }, 2000)
  }
}

// Add field labels
function addFieldLabels() {
  const fieldLabels = {
    personName: "Full Name",
    birthDate: "Birth Date",
    email: "Email Address",
    phoneNumber: "Phone Number",
    matric: "Matric Number",
    department: "Department",
    level: "Level",
    gender: "Gender",
    trainingLevel: "Training Level",
  }

  Object.entries(fieldLabels).forEach(([fieldName, label]) => {
    const field = document.querySelector(`[name="${fieldName}"]`)
    if (field && field.parentNode.tagName === "P") {
      const fieldGroup = document.createElement("div")
      fieldGroup.className = "field-group"

      const labelElement = document.createElement("div")
      labelElement.className = "field-label"
      labelElement.textContent = label

      field.parentNode.insertBefore(fieldGroup, field)
      fieldGroup.appendChild(labelElement)
      fieldGroup.appendChild(field)
    }
  })
}

// Celebration effect
function createCelebrationEffect(element) {
  const rect = element.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 2

  // Create confetti burst
  for (let i = 0; i < 30; i++) {
    const confetti = document.createElement("div")
    confetti.style.position = "fixed"
    confetti.style.left = centerX + "px"
    confetti.style.top = centerY + "px"
    confetti.style.width = "8px"
    confetti.style.height = "8px"
    confetti.style.backgroundColor = ["#ffd700", "#ff69b4", "#00bfff", "#98fb98", "#ff6347"][
      Math.floor(Math.random() * 5)
    ]
    confetti.style.borderRadius = "50%"
    confetti.style.pointerEvents = "none"
    confetti.style.zIndex = "9999"

    const angle = (Math.PI * 2 * i) / 30
    const velocity = 150 + Math.random() * 100
    const vx = Math.cos(angle) * velocity
    const vy = Math.sin(angle) * velocity

    confetti.style.animation = `confetti-${i} 1.5s ease-out forwards`

    // Create unique animation for each confetti
    const style = document.createElement("style")
    style.textContent = `
            @keyframes confetti-${i} {
                0% { transform: translate(0, 0) rotate(0deg); opacity: 1; }
                100% { transform: translate(${vx}px, ${vy + 300}px) rotate(720deg); opacity: 0; }
            }
        `
    document.head.appendChild(style)

    document.body.appendChild(confetti)

    setTimeout(() => {
      confetti.remove()
      style.remove()
    }, 1500)
  }
}

// Ripple effect for buttons
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

// Keyboard navigation
function initKeyboardNavigation() {
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      const editBtn = document.getElementById("editBtn")
      if (editBtn.textContent.includes("Cancel")) {
        editBtn.click()
      }
    }

    if (e.ctrlKey && e.key === "s") {
      e.preventDefault()
      const saveBtn = document.getElementById("saveBtn")
      if (saveBtn.style.display !== "none") {
        saveBtn.click()
      }
    }

    if (e.ctrlKey && e.key === "e") {
      e.preventDefault()
      const editBtn = document.getElementById("editBtn")
      editBtn.click()
    }
  })
}

// Profile image interactions
function initProfileImageEffects() {
  const profileImg = document.querySelector(".profile-image img")

  profileImg.addEventListener("click", () => {
    // Create a pulse effect
    profileImg.style.animation = "pulse 0.6s ease-out"
    setTimeout(() => {
      profileImg.style.animation = "profileImageFloat 3s ease-in-out infinite"
    }, 600)

    // Show a fun message
    showToast("Looking good! 📸", "info", 2000)
  })

  // Add hover sound effect (visual feedback)
  profileImg.addEventListener("mouseenter", () => {
    profileImg.style.filter = "brightness(1.1) saturate(1.2)"
  })

  profileImg.addEventListener("mouseleave", () => {
    profileImg.style.filter = "brightness(1) saturate(1)"
  })
}

// Add dynamic styles
function addDynamicStyles() {
  const style = document.createElement("style")
  style.textContent = `
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
        
        @keyframes toastSlideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `
  document.head.appendChild(style)
}

// Initialize everything when page loads
document.addEventListener("DOMContentLoaded", () => {
  // Start particle system
  createParticles()
  setInterval(createParticles, 4000)

  // Initialize all functionality
  initializeProfileForm()
  initKeyboardNavigation()
  initProfileImageEffects()
  addDynamicStyles()

  // Add ripple effect to buttons
  document.querySelectorAll(".btn").forEach((button) => {
    button.addEventListener("click", createRipple)
  })

  // Show welcome message
  setTimeout(() => {
    showToast("Profile loaded successfully! Click Edit to make changes.", "success", 4000)
  }, 1000)

  // Add entrance animation to profile card
  const profileCard = document.querySelector(".profile-card")
  profileCard.classList.add("animated")

  // Keyboard shortcuts help
  document.addEventListener("keydown", (e) => {
    if (e.key === "F1") {
      e.preventDefault()
      showToast("Shortcuts: Ctrl+E (Edit), Ctrl+S (Save), Esc (Cancel)", "info", 5000)
    }
  })
})

// Easter egg - konami code
let konamiCode = []
const konami = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]

document.addEventListener("keydown", (e) => {
  konamiCode.push(e.keyCode)
  if (konamiCode.length > konami.length) {
    konamiCode.shift()
  }

  if (konamiCode.join(",") === konami.join(",")) {
    // Easter egg triggered - profile party mode!
    createParticles()
    createParticles()

    const profileImg = document.querySelector(".profile-image img")
    profileImg.style.animation = "spin 2s linear infinite"

    showToast("🎉 Profile Party Mode Activated! 🎉", "success", 3000)

    setTimeout(() => {
      profileImg.style.animation = "profileImageFloat 3s ease-in-out infinite"
    }, 2000)

    konamiCode = []
  }
})

// Performance optimization
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

// Add accessibility improvements
function initAccessibility() {
  // Add ARIA labels
  document.querySelectorAll("input, select").forEach((field) => {
    const label = field.parentNode.querySelector(".field-label")
    if (label) {
      field.setAttribute("aria-label", label.textContent)
    }
  })

  // Add keyboard focus indicators
  document.querySelectorAll("input, select, button").forEach((element) => {
    element.addEventListener("focus", () => {
      element.style.outline = "2px solid #ffd700"
      element.style.outlineOffset = "2px"
    })

    element.addEventListener("blur", () => {
      element.style.outline = "none"
    })
  })
}

// Initialize accessibility on load
document.addEventListener("DOMContentLoaded", initAccessibility)

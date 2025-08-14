class PWAManager {
  constructor() {
    this.isSupported = "serviceWorker" in navigator && "PushManager" in window
    this.registration = null
    this.vapidPublicKey = null
  }

  async init() {
    if (!this.isSupported) {
      console.log("PWA features not supported")
      return
    }

    try {
      // Register service worker
      this.registration = await navigator.serviceWorker.register("/sw.js")
      console.log("Service Worker registered successfully:", this.registration)

      // Get VAPID public key from server
      await this.loadVapidPublicKey()

      // Only proceed if we have a valid VAPID key
      if (!this.vapidPublicKey) {
        console.error("Cannot setup push notifications: VAPID key not available")
        return
      }

      // Request notification permission
      await this.requestNotificationPermission()

      // Setup push notifications
      await this.setupPushNotifications()
    } catch (error) {
      console.error("PWA initialization failed:", error)
    }
  }

// Load VAPID public key from server with better error handling
  async loadVapidPublicKey() {
    try {
      console.log("Fetching VAPID public key from server...")
      const response = await fetch("/api/vapid-public-key/")
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      const data = await response.json()
      console.log("VAPID key response:", data)

      if (data.success && data.public_key) {
        this.vapidPublicKey = data.public_key
        console.log("VAPID public key loaded successfully:", this.vapidPublicKey)
      } else {
        throw new Error(data.error || "No public key in response")
      }
    } catch (error) {
      console.error("Failed to load VAPID public key from server:", error)
      
      // Try fallback to window variable
      if (window.VAPID_PUBLIC_KEY) {
        console.log("Using fallback VAPID key from window")
        this.vapidPublicKey = window.VAPID_PUBLIC_KEY
      } else {
        console.error("No fallback VAPID key available")
        this.vapidPublicKey = null
      }
    }
  }

  // Request notification permission
async requestNotificationPermission() {
    if (!("Notification" in window)) {
      console.log("This browser does not support notifications")
      return
    }

    if (Notification.permission === "default") {
      const permission = await Notification.requestPermission()
      if (permission === "granted") {
        console.log("Notification permission granted")
      } else {
        console.log("Notification permission denied")
      }
    }
  }

  // Setup push notifications
async setupPushNotifications() {
    if (!this.registration) {
      console.error("Cannot setup push notifications: no service worker registration")
      return
    }

    if (!this.vapidPublicKey) {
      console.error("Cannot setup push notifications: no VAPID key")
      return
    }

    if (Notification.permission !== "granted") {
      console.log("Notification permission not granted")
      return
    }

    try {
      const subscription = await this.registration.pushManager.getSubscription()

      if (!subscription) {
        console.log("Creating new push subscription...")
        console.log("Converting VAPID key:", this.vapidPublicKey)
        
        const convertedKey = this.urlBase64ToUint8Array(this.vapidPublicKey)
        console.log("Converted key:", convertedKey)

        const newSubscription = await this.registration.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: convertedKey,
        })

        await this.sendSubscriptionToServer(newSubscription)
        console.log("Push subscription successful")
      } else {
        console.log("Already subscribed to push notifications")
        await this.sendSubscriptionToServer(subscription)
      }
    } catch (error) {
      console.error("Push notification setup failed:", error)

      if (error.name === "InvalidAccessError") {
        console.error("VAPID key format error. Key:", this.vapidPublicKey)
      } else if (error.name === "NotSupportedError") {
        console.error("Push messaging not supported by this browser.")
      }
    }
  }

  // Convert VAPID key - Updated with better error handling
  // Convert VAPID key with comprehensive error handling
  urlBase64ToUint8Array(base64String) {
    console.log("Converting base64 string:", base64String, "Type:", typeof base64String)
    
    if (!base64String) {
      throw new Error("VAPID public key is empty or undefined")
    }

    if (typeof base64String !== 'string') {
      throw new Error(`VAPID public key must be a string, got: ${typeof base64String}`)
    }

    try {
      const padding = "=".repeat((4 - (base64String.length % 4)) % 4)
      const base64 = (base64String + padding).replace(/-/g, "+").replace(/_/g, "/")

      const rawData = window.atob(base64)
      const outputArray = new Uint8Array(rawData.length)

      for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i)
      }

      console.log("VAPID key converted successfully, length:", outputArray.length)
      return outputArray
    } catch (error) {
      console.error("Error converting VAPID key:", error)
      console.error("Input was:", base64String)
      throw new Error(`Invalid VAPID key format: ${error.message}`)
    }
  }

  // Send subscription to server
async sendSubscriptionToServer(subscription) {
    try {
      const response = await fetch("/api/push-subscription/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": this.getCSRFToken(),
        },
        body: JSON.stringify(subscription),
      })

      const data = await response.json()

      if (response.ok && data.success) {
        console.log("Push subscription sent to server successfully")
      } else {
        console.error("Failed to send subscription to server:", data.error)
      }
    } catch (error) {
      console.error("Failed to send subscription to server:", error)
    }
  }

  // Get CSRF token
getCSRFToken() {
    const name = "csrftoken"
    let cookieValue = null
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";")
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim()
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        }
      }
    }
    return cookieValue
  }


  // Show update notification
  showUpdateNotification() {
    if (confirm("A new version of NeverForget is available! Would you like to update?")) {
      window.location.reload()
    }
  }

  // Test push notification
  async testPushNotification() {
    try {
      const response = await fetch("/api/send-birthday-notification/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": this.getCSRFToken(),
        },
        body: JSON.stringify({
          title: "Test Notification",
          message: "This is a test push notification!",
          test: true,
        }),
      })

      if (response.ok) {
        console.log("Test notification sent")
      }
    } catch (error) {
      console.error("Failed to send test notification:", error)
    }
  }

  // Add to home screen prompt
  showAddToHomeScreenPrompt() {
    let deferredPrompt

    window.addEventListener("beforeinstallprompt", (e) => {
      e.preventDefault()
      deferredPrompt = e
      window.deferredPrompt = deferredPrompt

      // Show custom install prompt
      this.showCustomInstallPrompt()
    })
  }

  // Custom install prompt
  showCustomInstallPrompt() {
    const installPrompt = document.createElement("div")
    installPrompt.className = "install-prompt"
    installPrompt.innerHTML = `
      <div class="install-prompt-content">
        <h3>Install NeverForget</h3>
        <p>Add NeverForget to your home screen for quick access!</p>
        <div class="install-buttons">
          <button class="btn btn-primary" onclick="pwaManager.installApp()">Install</button>
          <button class="btn btn-secondary" onclick="this.parentElement.parentElement.parentElement.remove()">Not Now</button>
        </div>
      </div>
    `

    document.body.appendChild(installPrompt)
  }

  // Install app
  async installApp() {
    if (window.deferredPrompt) {
      window.deferredPrompt.prompt()
      const { outcome } = await window.deferredPrompt.userChoice
      console.log(`User response to the install prompt: ${outcome}`)
      window.deferredPrompt = null

      // Remove install prompt
      const installPrompt = document.querySelector(".install-prompt")
      if (installPrompt) {
        installPrompt.remove()
      }
    }
  }
}

// Initialize PWA when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  window.pwaManager = new PWAManager()
  window.pwaManager.init()
  window.pwaManager.showAddToHomeScreenPrompt()

  // Hide splash screen immediately
  hideSplashScreen()
})

// Also hide splash screen when page is fully loaded
window.addEventListener("load", () => {
  hideSplashScreen()
})

// Function to hide splash screen
function hideSplashScreen() {
  const splash = document.getElementById("pwa-splash")
  const loading = document.getElementById("pwa-loading")

  if (splash) {
    splash.style.opacity = "0"
    setTimeout(() => {
      splash.style.display = "none"
    }, 300)
  }

  if (loading) {
    loading.style.display = "none"
  }
}

// Hide splash screen after a short delay as fallback
setTimeout(hideSplashScreen, 500)

// Export for use in other scripts
if (typeof module !== "undefined" && module.exports) {
  module.exports = PWAManager
}

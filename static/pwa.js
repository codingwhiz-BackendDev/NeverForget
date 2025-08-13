// PWA Registration and Setup
class PWAManager {
  constructor() {
    this.isSupported = 'serviceWorker' in navigator && 'PushManager' in window;
    this.registration = null;
  }

  // Initialize PWA
  async init() {
    if (!this.isSupported) {
      console.log('PWA features not supported');
      return;
    }

    try {
      // Register service worker
      this.registration = await navigator.serviceWorker.register('/static/sw.js');
      console.log('Service Worker registered successfully:', this.registration);

      // Check for updates
      this.registration.addEventListener('updatefound', () => {
        const newWorker = this.registration.installing;
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            this.showUpdateNotification();
          }
        });
      });

      // Handle service worker updates
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        console.log('New service worker activated');
        window.location.reload();
      });

      // Request notification permission
      await this.requestNotificationPermission();

      // Setup push notifications
      await this.setupPushNotifications();

    } catch (error) {
      console.error('Service Worker registration failed:', error);
    }
  }

  // Request notification permission
  async requestNotificationPermission() {
    if (!('Notification' in window)) {
      console.log('This browser does not support notifications');
      return;
    }

    if (Notification.permission === 'default') {
      const permission = await Notification.requestPermission();
      if (permission === 'granted') {
        console.log('Notification permission granted');
      }
    }
  }

  // Setup push notifications
  async setupPushNotifications() {
    if (!this.registration) return;

    try {
      const subscription = await this.registration.pushManager.getSubscription();
      
      if (!subscription) {
        // Subscribe to push notifications
        const newSubscription = await this.registration.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: this.urlBase64ToUint8Array('YOUR_VAPID_PUBLIC_KEY') // Replace with your VAPID key
        });

        // Send subscription to server
        await this.sendSubscriptionToServer(newSubscription);
      }
    } catch (error) {
      console.error('Push notification setup failed:', error);
    }
  }

  // Convert VAPID key
  urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
      .replace(/-/g, '+')
      .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }

  // Send subscription to server
  async sendSubscriptionToServer(subscription) {
    try {
      const response = await fetch('/api/push-subscription/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken()
        },
        body: JSON.stringify(subscription)
      });

      if (response.ok) {
        console.log('Push subscription sent to server');
      }
    } catch (error) {
      console.error('Failed to send subscription to server:', error);
    }
  }

  // Get CSRF token
  getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Show update notification
  showUpdateNotification() {
    if (confirm('A new version of NeverForget is available! Would you like to update?')) {
      window.location.reload();
    }
  }

  // Send birthday notification
  async sendBirthdayNotification(birthdayData) {
    if (!this.registration) return;

    try {
      const response = await fetch('/api/send-birthday-notification/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken()
        },
        body: JSON.stringify(birthdayData)
      });

      if (response.ok) {
        console.log('Birthday notification sent');
      }
    } catch (error) {
      console.error('Failed to send birthday notification:', error);
    }
  }

  // Add to home screen prompt
  showAddToHomeScreenPrompt() {
    let deferredPrompt;
    
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      deferredPrompt = e;
      
      // Show custom install prompt
      this.showCustomInstallPrompt();
    });
  }

  // Custom install prompt
  showCustomInstallPrompt() {
    const installPrompt = document.createElement('div');
    installPrompt.className = 'install-prompt';
    installPrompt.innerHTML = `
      <div class="install-prompt-content">
        <h3>Install NeverForget</h3>
        <p>Add NeverForget to your home screen for quick access!</p>
        <div class="install-buttons">
          <button class="btn btn-primary" onclick="pwaManager.installApp()">Install</button>
          <button class="btn btn-secondary" onclick="this.parentElement.parentElement.parentElement.remove()">Not Now</button>
        </div>
      </div>
    `;
    
    document.body.appendChild(installPrompt);
  }

  // Install app
  async installApp() {
    if (window.deferredPrompt) {
      window.deferredPrompt.prompt();
      const { outcome } = await window.deferredPrompt.userChoice;
      console.log(`User response to the install prompt: ${outcome}`);
      window.deferredPrompt = null;
      
      // Remove install prompt
      const installPrompt = document.querySelector('.install-prompt');
      if (installPrompt) {
        installPrompt.remove();
      }
    }
  }
}

// Initialize PWA when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.pwaManager = new PWAManager();
  window.pwaManager.init();
  window.pwaManager.showAddToHomeScreenPrompt();
  
  // Hide splash screen immediately
  hideSplashScreen();
});

// Also hide splash screen when page is fully loaded
window.addEventListener('load', () => {
  hideSplashScreen();
});

// Function to hide splash screen
function hideSplashScreen() {
  const splash = document.getElementById('pwa-splash');
  const loading = document.getElementById('pwa-loading');
  
  if (splash) {
    splash.style.opacity = '0';
    setTimeout(() => {
      splash.style.display = 'none';
    }, 300);
  }
  
  if (loading) {
    loading.style.display = 'none';
  }
}

// Hide splash screen after a short delay as fallback
setTimeout(hideSplashScreen, 500);

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PWAManager;
} 
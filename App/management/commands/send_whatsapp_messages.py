from django.core.management.base import BaseCommand
from django.utils import timezone
from App.models import BirthdayInfo
import time
import urllib.parse
import os
import shutil
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, SessionNotCreatedException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

class Command(BaseCommand):
    help = 'Send WhatsApp birthday messages (Persistent Login)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            action='store_true',
            help='Run in test mode (don\'t send actual messages)',
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Enable debug mode with more detailed logging',
        )
        parser.add_argument(
            '--skip-login-check',
            action='store_true',
            help='Skip login detection and proceed directly to sending messages',
        )
        parser.add_argument(
            '--reset-profile',
            action='store_true',
            help='Reset Chrome profile (will require QR scan again)',
        )

    def get_chrome_profile_path(self):
        """Get or create persistent Chrome profile path"""
        # Create a persistent directory in your project folder
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        profile_dir = os.path.join(project_root, 'whatsapp_chrome_profile')
        
        # Create directory if it doesn't exist
        if not os.path.exists(profile_dir):
            os.makedirs(profile_dir)
            self.stdout.write(self.style.WARNING(f"📁 Created Chrome profile directory: {profile_dir}"))
        
        return profile_dir

    def setup_chrome_driver(self, reset_profile=False):
        """Setup Chrome driver with persistent profile"""
        options = Options()
        
        # Get persistent profile path
        profile_path = self.get_chrome_profile_path()
        
        # Reset profile if requested
        if reset_profile:
            if os.path.exists(profile_path):
                shutil.rmtree(profile_path)
                os.makedirs(profile_path)
                self.stdout.write(self.style.WARNING("🔄 Chrome profile reset"))
        
        # Essential options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-features=TranslateUI")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        
        # Suppress GPU errors and logs
        options.add_argument("--disable-logging")
        options.add_argument("--disable-gpu-logging")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        
        # Use persistent profile directory
        options.add_argument(f"--user-data-dir={profile_path}")
        
        # Set debugging port
        options.add_argument("--remote-debugging-port=9222")
        
        # Window options
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
        
        # Anti-detection
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            self.stdout.write(self.style.WARNING("🚀 Initializing Chrome driver with persistent profile..."))
            self.stdout.write(self.style.WARNING(f"📁 Profile path: {profile_path}"))
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            # Configure driver
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.set_page_load_timeout(60)
            driver.implicitly_wait(3)
            
            self.stdout.write(self.style.SUCCESS("✅ Chrome driver initialized successfully"))
            return driver, profile_path
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Chrome driver setup failed: {str(e)}"))
            raise

    def wait_for_whatsapp_login(self, driver, skip_login_check=False, debug=False):
        """Wait for WhatsApp to load and user to login"""
        self.stdout.write(self.style.WARNING("📱 Loading WhatsApp Web..."))
        
        try:
            driver.get("https://web.whatsapp.com")
            time.sleep(8)  # Give more time for initial load
            
            if skip_login_check:
                self.stdout.write(self.style.WARNING("⏭️ Skipping login check as requested"))
                time.sleep(5)
                return True
            
            # Enhanced login detection
            if self.is_logged_in(driver, debug):
                self.stdout.write(self.style.SUCCESS("✅ Already logged in to WhatsApp! (Session restored)"))
                return True
            
            # Check if QR code is present
            if self.has_qr_code(driver, debug):
                self.stdout.write(self.style.WARNING("📱 QR code detected - please scan to login"))
                self.stdout.write(self.style.WARNING("💡 This is a one-time setup. Future runs will remember your login."))
            else:
                self.stdout.write(self.style.WARNING("📱 Please complete login process"))
            
            self.stdout.write(self.style.WARNING("⏳ Waiting up to 120 seconds for login..."))
            
            # Wait for login with more frequent checks
            for i in range(60):  # 60 * 2 = 120 seconds
                if self.is_logged_in(driver, debug):
                    self.stdout.write(self.style.SUCCESS("✅ Successfully logged in to WhatsApp!"))
                    self.stdout.write(self.style.SUCCESS("💾 Login session saved for future use"))
                    time.sleep(3)
                    return True
                time.sleep(2)
                if i % 10 == 0 and i > 0:  # Print every 20 seconds
                    self.stdout.write(self.style.WARNING(f"⏳ Still waiting... ({i*2}s elapsed)"))
                    if debug:
                        self.debug_page_state(driver)
            
            self.stdout.write(self.style.ERROR("❌ Login timeout - please try again"))
            return False
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error loading WhatsApp: {str(e)}"))
            return False

    def has_qr_code(self, driver, debug=False):
        """Check if QR code is present"""
        try:
            qr_selectors = [
                "//canvas[@aria-label='Scan me!']",
                "//div[@data-testid='qr-code']",
                "//canvas[contains(@style, 'qr')]",
                "//div[contains(@class, 'qr')]",
            ]
            
            for selector in qr_selectors:
                try:
                    WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    if debug:
                        self.stdout.write(self.style.WARNING(f"🔍 QR code found: {selector}"))
                    return True
                except TimeoutException:
                    continue
            
            return False
        except Exception:
            return False

    def is_logged_in(self, driver, debug=False):
        """Enhanced login detection"""
        try:
            # Primary login indicators (most reliable)
            primary_indicators = [
                "//div[@data-testid='chat-list']",
                "//div[@title='Search input textbox']",
                "//div[@data-testid='search']",
                "//header[@data-testid='chatlist-header']",
            ]
            
            # Secondary indicators
            secondary_indicators = [
                "//span[@data-testid='default-user']",
                "//div[contains(@class, 'chat-list')]",
                "//div[@role='textbox'][@contenteditable='true']",
                "//div[@data-testid='conversation-compose-box-input']",
            ]
            
            # Text-based indicators
            text_indicators = [
                "//span[contains(text(), 'Search or start new chat')]",
                "//div[contains(text(), 'WhatsApp Web')]",
            ]
            
            all_indicators = primary_indicators + secondary_indicators + text_indicators
            
            for selector in all_indicators:
                try:
                    element = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    if debug:
                        self.stdout.write(self.style.SUCCESS(f"✅ Login indicator found: {selector}"))
                    return True
                except TimeoutException:
                    if debug:
                        self.stdout.write(self.style.WARNING(f"⚠️ Not found: {selector}"))
                    continue
            
            # Check page source for login indicators
            try:
                page_source = driver.page_source.lower()
                login_keywords = ['chat-list', 'search input', 'conversation', 'message']
                found_keywords = [keyword for keyword in login_keywords if keyword in page_source]
                
                if found_keywords and debug:
                    self.stdout.write(self.style.SUCCESS(f"✅ Found keywords in page: {found_keywords}"))
                    return True
                elif debug:
                    self.stdout.write(self.style.WARNING("⚠️ No login keywords found in page source"))
            except Exception as e:
                if debug:
                    self.stdout.write(self.style.WARNING(f"⚠️ Error checking page source: {str(e)}"))
            
            return False
            
        except Exception as e:
            if debug:
                self.stdout.write(self.style.ERROR(f"❌ Error in login detection: {str(e)}"))
            return False

    def debug_page_state(self, driver):
        """Debug current page state"""
        try:
            current_url = driver.current_url
            page_title = driver.title
            self.stdout.write(self.style.WARNING(f"🔍 Current URL: {current_url}"))
            self.stdout.write(self.style.WARNING(f"🔍 Page Title: {page_title}"))
            
            # Check for common elements
            common_elements = [
                "//div[@id='app']",
                "//div[@data-testid='intro']",
                "//canvas",
                "//div[contains(@class, 'landing')]",
            ]
            
            for selector in common_elements:
                try:
                    driver.find_element(By.XPATH, selector)
                    self.stdout.write(self.style.WARNING(f"🔍 Found element: {selector}"))
                except NoSuchElementException:
                    pass
                    
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"🔍 Debug error: {str(e)}"))

    def send_message(self, driver, phone_number, message, debug=False):
        """Send WhatsApp message with improved reliability"""
        try:
            formatted_number = self.format_phone_number(phone_number)
            encoded_message = urllib.parse.quote(message)
            url = f"https://web.whatsapp.com/send?phone={formatted_number}&text={encoded_message}"
            
            self.stdout.write(self.style.WARNING(f"📤 Sending to {formatted_number}..."))
            
            if debug:
                self.stdout.write(self.style.WARNING(f"🔗 URL: {url}"))
            
            driver.get(url)
            time.sleep(10)  # Increased wait time
            
            # Check if chat opened successfully
            if not self.wait_for_chat_to_load(driver, debug):
                self.stdout.write(self.style.ERROR(f"❌ Chat failed to load for {formatted_number}"))
                return False
            
            # Try to send the message
            if self.click_send_button(driver, debug):
                self.stdout.write(self.style.SUCCESS(f"✅ Message sent to {formatted_number}"))
                time.sleep(5)
                return True
            else:
                self.stdout.write(self.style.ERROR(f"❌ Failed to send message to {formatted_number}"))
                return False
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error sending to {phone_number}: {str(e)}"))
            return False

    def wait_for_chat_to_load(self, driver, debug=False):
        """Wait for chat interface to load"""
        try:
            # Wait longer for chat to load
            chat_indicators = [
                "//div[@contenteditable='true'][@data-tab='10']",
                "//div[@contenteditable='true'][@role='textbox']",
                "//span[@data-testid='send']",
                "//button[@aria-label='Send']",
                "//div[@data-testid='conversation-compose-box-input']",
            ]
            
            for selector in chat_indicators:
                try:
                    element = WebDriverWait(driver, 15).until(  # Increased timeout
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    if debug:
                        self.stdout.write(self.style.SUCCESS(f"✅ Found chat element: {selector}"))
                    return True
                except TimeoutException:
                    if debug:
                        self.stdout.write(self.style.WARNING(f"⚠️ Chat element not found: {selector}"))
                    continue
            
            # Check for error messages
            error_selectors = [
                "//div[contains(text(), 'Phone number shared via url is invalid')]",
                "//div[contains(text(), 'This phone number is not on WhatsApp')]",
                "//div[contains(text(), 'Unable to contact phone')]",
            ]
            
            for selector in error_selectors:
                try:
                    WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    self.stdout.write(self.style.ERROR("❌ Invalid phone number or not on WhatsApp"))
                    return False
                except TimeoutException:
                    continue
            
            if debug:
                self.stdout.write(self.style.WARNING("⚠️ No chat indicators found"))
            return False
            
        except Exception as e:
            if debug:
                self.stdout.write(self.style.WARNING(f"⚠️ Error waiting for chat: {str(e)}"))
            return False

    def click_send_button(self, driver, debug=False):
        """Try multiple methods to send the message"""
        try:
            # Method 1: Look for send button with longer wait
            send_selectors = [
                "//span[@data-testid='send']",
                "//button[@aria-label='Send']",
                "//span[@data-icon='send']",
                "//button[contains(@class, 'send')]",
                "//div[@role='button'][@aria-label='Send']",
                "//button[@data-testid='compose-btn-send']",
            ]
            
            for selector in send_selectors:
                try:
                    send_button = WebDriverWait(driver, 8).until(  # Increased timeout
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    # Scroll to element if needed
                    driver.execute_script("arguments[0].scrollIntoView(true);", send_button)
                    time.sleep(1)
                    send_button.click()
                    if debug:
                        self.stdout.write(self.style.SUCCESS(f"✅ Clicked send button: {selector}"))
                    time.sleep(3)
                    return True
                except TimeoutException:
                    if debug:
                        self.stdout.write(self.style.WARNING(f"⚠️ Send button not found: {selector}"))
                    continue
                except Exception as e:
                    if debug:
                        self.stdout.write(self.style.WARNING(f"⚠️ Error clicking {selector}: {str(e)}"))
                    continue
            
            # Method 2: Try Enter key on message input
            message_input_selectors = [
                "//div[@contenteditable='true'][@data-tab='10']",
                "//div[@contenteditable='true'][@role='textbox']",
                "//div[@data-testid='conversation-compose-box-input']",
            ]
            
            for selector in message_input_selectors:
                try:
                    message_input = driver.find_element(By.XPATH, selector)
                    message_input.click()
                    time.sleep(1)
                    message_input.send_keys(Keys.ENTER)
                    if debug:
                        self.stdout.write(self.style.SUCCESS(f"✅ Sent via Enter key: {selector}"))
                    time.sleep(3)
                    return True
                except NoSuchElementException:
                    if debug:
                        self.stdout.write(self.style.WARNING(f"⚠️ Message input not found: {selector}"))
                    continue
                except Exception as e:
                    if debug:
                        self.stdout.write(self.style.WARNING(f"⚠️ Error with Enter key {selector}: {str(e)}"))
                    continue
            
            return False
            
        except Exception as e:
            if debug:
                self.stdout.write(self.style.ERROR(f"❌ All send methods failed: {str(e)}"))
            return False

    def format_phone_number(self, raw_number):
        """Format phone number for WhatsApp"""
        number = str(raw_number).strip().replace(" ", "").replace("-", "").replace("+", "")
        
        if number.startswith("0"):
            return "234" + number[1:]
        elif not number.startswith("234"):
            return "234" + number
        return number

    def handle(self, *args, **options):
        today = timezone.now().date()
        reminders = BirthdayInfo.objects.filter(birthDate=today)
        debug = options.get('debug', False)
        skip_login_check = options.get('skip_login_check', False)
        reset_profile = options.get('reset_profile', False)
        
        if not reminders.exists():
            self.stdout.write(self.style.WARNING('No birthdays today.'))
            return
            
        self.stdout.write(self.style.SUCCESS(f'🎉 Found {reminders.count()} birthday(s).'))
        
        # Test mode
        if options['test']:
            self.stdout.write(self.style.WARNING('🧪 Running in TEST mode - no messages will be sent'))
            for reminder in reminders:
                number = self.format_phone_number(reminder.phoneNumber)
                message = f"Remember to wish {reminder.personName}  Happy Birthday ! 🎉🎂"
                self.stdout.write(self.style.SUCCESS(f"Would send to {number}: {message}"))
            return
        
        driver = None
        profile_path = None
        
        try:
            # Setup Chrome driver with persistent profile
            driver, profile_path = self.setup_chrome_driver(reset_profile)
            
            # Load WhatsApp and wait for login
            if not self.wait_for_whatsapp_login(driver, skip_login_check, debug):
                self.stdout.write(self.style.ERROR("❌ Failed to login to WhatsApp Web"))
                return
            
            # Send messages
            successful = 0
            failed = 0
            
            for reminder in reminders:
                message = f"🎉 Happy Birthday {reminder.personName}! 🎂\n\nHave a wonderful day filled with joy! 🎈"
                
                if self.send_message(driver, reminder.phoneNumber, message, debug):
                    successful += 1
                else:
                    failed += 1
                
                # Wait between messages
                time.sleep(10)
            
            self.stdout.write(self.style.SUCCESS(f"\n📊 Summary: {successful} successful, {failed} failed"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Critical error: {str(e)}"))
            
        finally:
            if driver:
                self.stdout.write(self.style.WARNING("🔚 Closing browser..."))
                try:
                    driver.quit()
                except:
                    pass
            
            # Note: We don't delete the profile_path anymore since it's persistent
            self.stdout.write(self.style.SUCCESS("💾 Chrome profile saved for future use"))

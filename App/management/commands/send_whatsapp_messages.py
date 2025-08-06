from django.core.management.base import BaseCommand
from django.utils import timezone
from App.models import BirthdayInfo  # Replace 'App' if your app is named differently
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        reminders = BirthdayInfo.objects.filter(birthDate=today)

        if not reminders.exists():
            self.stdout.write(self.style.WARNING('No birthdays today.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Found {reminders.count()} birthday(s). Sending messages...'))

        # Setup Selenium with WhatsApp Web
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")
        # options.add_argument("--headless")  # Uncomment if running headless
        options.add_argument("--user-data-dir=selenium")  # Keeps session logged in

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://web.whatsapp.com")

        input("⚠️ Scan the QR code in the browser and press Enter here to continue...")

        for reminder in reminders:
            try:
                # Convert phone number to international format (assumes Nigerian numbers)
                raw_number = str(reminder.phoneNumber).strip()
                if raw_number.startswith("8"):
                    number = "234" + raw_number[1:]
                elif not raw_number.startswith("234"):
                    number = "234" + raw_number  # default fallback
                else:
                    number = raw_number

                # WhatsApp message
                message = f"{reminder.personName}: 🎉 Happy Birthday! {reminder.email}"

                url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
                driver.get(url)
                time.sleep(10)  # Wait for page to load

                # Click the send button
                send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
                send_button.click()

                self.stdout.write(self.style.SUCCESS(f'✅ Message sent to {number}'))
                time.sleep(5)  # Wait before sending next message

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error sending to {raw_number}: {str(e)}'))

        driver.quit()

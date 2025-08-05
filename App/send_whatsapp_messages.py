# notifications/management/commands/send_whatsapp.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from .models import Reminder  # Replace with your actual app name
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class Command(BaseCommand):
    help = 'Send WhatsApp messages on matching dates'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        reminders = Reminder.objects.filter(send_date=today)

        if not reminders.exists():
            self.stdout.write(self.style.WARNING('No reminders for today'))
            return

        self.stdout.write(self.style.SUCCESS(f'Found {reminders.count()} reminders. Sending...'))

        # Setup Selenium with WhatsApp Web
        options = Options()
        options.add_argument("--user-data-dir=selenium")  # Keeps you logged in
        driver = webdriver.Chrome(options=options)
        driver.get("https://web.whatsapp.com")

        # Wait for WhatsApp to load
        input("Scan the QR code and press Enter to continue...")

        for reminder in reminders:
            try:
                number = reminder.phone_number
                message = reminder.message

                url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
                driver.get(url)
                time.sleep(10)  # Wait for page to load

                # Click the send button
                send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
                send_button.click()

                self.stdout.write(self.style.SUCCESS(f'Message sent to {number}'))

                time.sleep(5)  # Delay between messages

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error sending to {reminder.phone_number}: {str(e)}'))

        driver.quit()

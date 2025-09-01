#!/usr/bin/env bash
# Exit if any command fails
set -o errexit  

# Install Python deps
pip install -r requirements.txt

# Install Google Chrome
apt-get update
apt-get install -y wget gnupg unzip
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
apt-get update
apt-get install -y google-chrome-stable

# Install ChromeDriver (latest compatible)
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1)
LATEST_DRIVER=$(wget -q -O - "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}")
wget -q "https://chromedriver.storage.googleapis.com/${LATEST_DRIVER}/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

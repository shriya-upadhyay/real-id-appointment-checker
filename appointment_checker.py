import os
import time
import requests
from bs4 import BeautifulSoup
import schedule
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Load environment variables
load_dotenv()

# Configuration
URL = "https://telegov.njportal.com/njmvcmobileunit/AppointmentWizard/265"
CHECK_INTERVAL = 12 # hours

# Email configuration
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def check_appointments():
    print(f"[{datetime.now()}] Checking for appointments...", flush=True)
    try:
        # Send a GET request to the website
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Parse the HTML content
        cards = soup.find_all("div", class_="locationCardContainer")
        available = []

        for card in cards:
            name_span = card.find("span", class_="AppointcardHeader")
            date_div = card.find("div", id=lambda x: x and x.startswith("dateText"))
            if name_span and date_div:
                location = name_span.get_text(separator=" ").strip()
                status = date_div.text.strip()

                if "no appointments available" not in status.lower():
                    available.append(f"{location} - {status}")

        if available:
            message = "Appointments are available at the following locations:\n\n" + "\n".join(available)
            print(message, flush=True)
            send_notification(message)
        else:
            print("No appointments available at any location.", flush=True)
        
        
    except Exception as e:
        print(f"Error checking appointments: {str(e)}", flush=True)

def send_notification(message):
    try:
        msg = MIMEText(message)
        msg['Subject'] = 'NJ MVC Appointment Available!'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email notification sent successfully!", flush=True)
    except Exception as e:
        print(f"Error sending email: {str(e)}")

def main():
    print("Starting NJ MVC appointment checker...", flush=True)
    print(f"Checking every {CHECK_INTERVAL} hours", flush=True)
    
    # Schedule the job
    schedule.every(CHECK_INTERVAL).hours.do(check_appointments)
    
    # Run immediately on startup
    check_appointments()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main() 
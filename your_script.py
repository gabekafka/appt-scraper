import requests
from bs4 import BeautifulSoup
import json
import os
import smtplib
from email.mime.text import MIMEText

URL = "https://example.com/apartments"  # <- Replace with your real URL
SEEN_FILE = "seen.json"

def fetch_listings():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    # Replace with how your site structures listings
    return [item.text.strip() for item in soup.find_all("h2")]

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_seen(listings):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(listings), f)

def send_email(message):
    msg = MIMEText(message)
    msg["Subject"] = "New Apartment Found"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = os.getenv("EMAIL_TO")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        smtp.send_message(msg)

def main():
    listings = set(fetch_listings())
    seen = load_seen()
    new_listings = listings - seen

    if new_listings:
        message = "\n".join(new_listings)
        send_email("New listings:\n" + message)
        save_seen(listings)

if __name__ == "__main__":
    main()
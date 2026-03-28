import requests
from bs4 import BeautifulSoup
import schedule
import time
import csv
import sqlite3
from datetime import datetime

print("Script started...")

# Database setup
conn = sqlite3.connect("quotes.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT,
    scraped_at TEXT
)
""")
conn.commit()

def scrape_website():
    print("Scraping started...")
    url = "https://quotes.toscrape.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("span", class_="text")

    csv_data = []

    for quote in quotes:
        text = quote.text
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert into database
        cursor.execute(
            "INSERT INTO quotes (quote, scraped_at) VALUES (?, ?)",
            (text, timestamp)
        )

        csv_data.append([text, timestamp])

    conn.commit()

    # Append to CSV
    with open("quotes.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

    print("Scraping completed and data stored.")

# Run every 10 seconds (testing)
schedule.every(10).seconds.do(scrape_website)

while True:
    schedule.run_pending()
    time.sleep(1)
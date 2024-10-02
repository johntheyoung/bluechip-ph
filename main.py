import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Get credentials file path and sheet name from environment variables
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
GOOGLE_SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME')

# Define the scope for the Sheets and Drive APIs
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Function to scrape the table data
def scrape_blue_chips_data():
    url = "https://www.pesobility.com/stock/blue-chips"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Add a retry mechanism
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find the table
            table = soup.find('table')
            if table is None:
                print(f"Table not found on attempt {attempt + 1}. Retrying...")
                time.sleep(2)  # Wait for 2 seconds before retrying
                continue
            
            rows = table.find_all('tr')
            
            data = []
            headers = [th.text.strip() for th in rows[0].find_all('th')]
            data.append(headers)
            
            current_date = datetime.now().strftime('%Y-%m-%d')
            for row in rows[1:]:
                cols = row.find_all('td')
                row_data = [current_date] + [col.text.strip() for col in cols]
                data.append(row_data)
            
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error occurred on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2)  # Wait for 2 seconds before retrying

    raise Exception("Failed to scrape data after multiple attempts")

# Function to upload data to Google Sheets
def upload_to_google_sheets(data):
    # Authorize the credentials and initialize the client
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)

    # Open the Google Sheet by its name
    spreadsheet = client.open(GOOGLE_SHEET_NAME)

    # Select the first sheet (or specify the sheet by name)
    worksheet = spreadsheet.sheet1

    # Get the current data in the sheet
    existing_data = worksheet.get_all_values()

    # If the sheet is empty or doesn't have headers, add them
    if not existing_data or existing_data[0] != ['Date Scraped', 'Symbol', 'Name', 'Current Price (%)', 'Previous Close', '52-Week High (%)', '52-Week Low', 'PE', '2023 Cash Div (%)']:
        worksheet.update('A1:I1', [['Date Scraped', 'Symbol', 'Name', 'Current Price (%)', 'Previous Close', '52-Week High (%)', '52-Week Low', 'PE', '2023 Cash Div (%)']])

    # Append the new data, skipping the header row
    worksheet.append_rows(data[1:])

    print("Data appended successfully.")

# Main execution
if __name__ == "__main__":
    # Scrape the data
    blue_chips_data = scrape_blue_chips_data()
    
    # Upload the data to Google Sheets
    upload_to_google_sheets(blue_chips_data)
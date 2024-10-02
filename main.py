import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

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

# Authorize the credentials and initialize the client
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Open the Google Sheet by its name
spreadsheet = client.open(GOOGLE_SHEET_NAME)

# Select the first sheet (or specify the sheet by name)
worksheet = spreadsheet.sheet1

# Data you want to upload (as a list of lists)
data = [
    ['Name', 'Age', 'City'],
    ['John Doe', 28, 'New York'],
    ['Jane Smith', 34, 'San Francisco'],
]

# Check if the sheet is empty
if worksheet.row_count == 0:
    # If empty, insert all data including headers
    worksheet.append_rows(data)
else:
    # If not empty, check if headers exist
    existing_headers = worksheet.row_values(1)
    if not existing_headers or existing_headers != data[0]:
        # If headers don't exist or are different, insert headers
        worksheet.insert_row(data[0], 1)
        # Then append the rest of the data
        worksheet.append_rows(data[1:])
    else:
        # If headers already exist, just append the new data
        worksheet.append_rows(data[1:])

print("Data uploaded successfully.")
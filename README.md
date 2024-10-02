# bluechip-ph

## Context
This project scrapes the "Blue Chips of the Philippines" table from the website [Pesobility](https://www.pesobility.com/stock/blue-chips). The goal is to collect daily data on blue chip stocks in the Philippines and store it in a Google Sheet for further analysis.

## Technologies Used
- Python 3.x
- BeautifulSoup4 for web scraping
- Requests library for making HTTP requests
- Google Sheets API for data storage
- gspread library for interacting with Google Sheets
- python-dotenv for managing environment variables

## General Approach
1. Web Scraping: We use BeautifulSoup to parse the HTML of the Pesobility website and extract the blue chip stocks data.
2. Data Processing: The scraped data is formatted and prepared for storage.
3. Google Sheets Integration: We use the Google Sheets API to append the daily data to a specific sheet named "Daily Data" within our Google Spreadsheet.
4. Automation: The script is designed to be run daily to collect and store the latest stock information.

## Google Sheets and Drive API Setup
To use this script, you need to set up Google Sheets and Drive API access:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the Google Sheets API and Google Drive API for your project.
4. Create a service account and download the JSON key file.
5. Rename the JSON key file to something like `bluechip-ph-xxxxx.json` and place it in the project directory.
6. Share your Google Sheet with the service account email. The email will look like: `googlesheetsuploader@bluechip-ph.iam.gserviceaccount.com`
7. Give the service account "Editor" access to the Google Sheet.

For detailed instructions on setting up the Google Sheets API, you can refer to the [gspread documentation](https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account).

## Environment Setup
Create a `.env` file in the project root with the following content:

```
SERVICE_ACCOUNT_FILE='path/to/bluechip-ph-xxxxx.json'
SCOPES=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
GOOGLE_SHEET_NAME='Blue Chips PH'
```

## Running the Script
To run the script, use the following command:

```
python main.py
```

## Notes

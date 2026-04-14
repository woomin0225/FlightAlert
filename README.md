# FlightAlert

FlightAlert is a lightweight desktop app for monitoring flight prices.
It is built with Python, `customtkinter`, `matplotlib`, and `numpy`.

## What It Does

- Tracks saved flight routes in a simple desktop dashboard
- Shows outbound, inbound, and total price for round trips
- Supports dark/light theme switching
- Uses mock pricing by default and can connect to Amadeus for live data
- Lets users create price alerts from the UI
- Supports optional Windows startup with minimized launch

## Tech Stack

- Python
- customtkinter
- matplotlib
- numpy
- sqlite3
- Amadeus Python SDK

## Run Locally

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the app:

```powershell
python app.py
```

## Environment Variables

Create a local `.env` file if you want live API access or email alerts.

Example values:

```env
AMADEUS_CLIENT_ID=your_client_id
AMADEUS_CLIENT_SECRET=your_client_secret
AMADEUS_HOSTNAME=test

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password

CHECK_INTERVAL_HOURS=6
```

## Portable Build

This project can also be packaged into a single Windows executable with PyInstaller.

```powershell
python -m PyInstaller --onefile --windowed --name FlightAlert_Portable app.py
```

## Notes

- `.env`, `alerts.db`, build outputs, and local route data are excluded from version control.
- If no live API credentials are configured, the app falls back to mock pricing.

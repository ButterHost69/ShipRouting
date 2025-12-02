# ShipRouting

## What this project does

This project automates the collection of wave and swell forecast data from the INCOIS/SARAT website. It queries forecasts over a latitude/longitude grid and saves them as CSV files.

## How it works

* **Account setup:** The user must first create an INCOIS/SARAT account manually. The script logs in using those credentials.
* **Session handling:** Selenium is used to perform the login flow and extract the `JSESSIONID` session token.
* **Data requests:** Using the session cookie, the script sends HTTP POST requests directly to SARAT endpoints.
* **Grid-based collection:** The script iterates over a predefined lat/lon grid and requests forecast data for each coordinate.
* **Parallel execution:** Multiple accounts can be used to run requests in parallel using `ThreadPoolExecutor`.
* **Output:** Forecast data for multiple days is stored in CSV files.

## Repository files

* **get_waves.py** — Main script for login, session retrieval, data download, and CSV output.
* **create_new_INCOIS_users.py** — Utility for bulk account creation.
* **credentials.py** — List of emails and password.
* **testplot.py** — Simple script to visualize the collected data (visualizes data on a map).

## What is implemented

* Automated login via Selenium
* Session token extraction (`JSESSIONID`)
* Parallel wave-data requests across a geospatial grid
* Multi-account load distribution
* CSV generation for day-wise forecasts
* Basic plotting example

## How to run

1. Create an INCOIS/SARAT account manually before running the script.
2. Install required Python dependencies (Selenium, Requests, NumPy, Matplotlib).
3. Ensure ChromeDriver is installed and matches your Chrome version.
4. Add your credentials to `credentials.py`.
5. Run:

```bash
python get_waves.py
```

CSV files will be generated in the project directory.

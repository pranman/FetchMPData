# FetchMPData

FetchMPData is a Python script designed to fetch and store the names, constituencies, and contact details of current Members of Parliament (MPs) in the UK.

The data is fetched from the [UK Parliament's Members API](https://members.parliament.uk/help/api).

## Features

- Fetches the names, constituencies, and contact details of current MPs.
- Stores the data locally as JSON.
- Handles pagination of API results.

## Dependencies
- Python 3.11 but should be compatible with Python 3.6+

## Usage

1. Run the script using the command `python GetMPs_optimized.py`
2. The script will create a JSON file named `HoC_active.json` in the same directory, containing the fetched data.

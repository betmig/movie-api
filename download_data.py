#!/usr/bin/env python
"""
Download IMDB Top 1000 Movies dataset from GitHub.
"""
import urllib.request
import sys

def download_imdb_data():
    """Download the IMDB dataset CSV file."""
    url = "https://raw.githubusercontent.com/peetck/IMDB-Top1000-Movies/master/IMDB-Movie-Data.csv"
    output_file = "imdb_full.csv"

    print(f"Downloading IMDB dataset from GitHub...")
    print(f"URL: {url}")

    try:
        urllib.request.urlretrieve(url, output_file)
        print(f"✓ Downloaded successfully to {output_file}")
        print(f"\nNext step: Run 'python import_imdb_data.py' to load the data into the database.")
        return True
    except Exception as e:
        print(f"Error downloading file: {e}")
        print(f"\nYou can manually download from:")
        print(f"  {url}")
        print(f"And save it as: {output_file}")
        return False

if __name__ == '__main__':
    success = download_imdb_data()
    sys.exit(0 if success else 1)

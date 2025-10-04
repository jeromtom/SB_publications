#!/usr/bin/env python3
"""
Script to find duplicate entries in the SB_publication_PMC.csv file.
Based on the GitHub issue: https://github.com/jgalazka/SB_publications/issues/1
"""

import pandas as pd
import sys

def find_duplicates(csv_file):
    """Find and display duplicate entries in the CSV file."""
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        print(f"Total rows in CSV: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        print()
        
        # Find duplicates based on both Title and Link columns
        duplicates = df[df.duplicated(subset=['Title', 'Link'], keep=False)]
        
        if len(duplicates) > 0:
            print(f"Found {len(duplicates)} duplicate rows:")
            print(duplicates[['Title', 'Link']].to_string(index=True))
            print()
            
            # Group by title and link to see pairs
            grouped = duplicates.groupby(['Title', 'Link']).size()
            print(f"Duplicate groups: {len(grouped)}")
            for (title, link), count in grouped.items():
                print(f"  - '{title[:50]}...' appears {count} times")
        else:
            print("No duplicates found.")
            
        # Also check for duplicates by title only
        title_duplicates = df[df.duplicated(subset=['Title'], keep=False)]
        if len(title_duplicates) > 0:
            print(f"\nFound {len(title_duplicates)} rows with duplicate titles:")
            print(title_duplicates[['Title', 'Link']].to_string(index=True))
            
        # Check for duplicates by link only
        link_duplicates = df[df.duplicated(subset=['Link'], keep=False)]
        if len(link_duplicates) > 0:
            print(f"\nFound {len(link_duplicates)} rows with duplicate links:")
            print(link_duplicates[['Title', 'Link']].to_string(index=True))
            
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    csv_file = "SB_publication_PMC.csv"
    find_duplicates(csv_file)

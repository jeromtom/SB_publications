#!/usr/bin/env python3
"""
Script to remove duplicate entries from the SB_publication_PMC.csv file.
Based on the GitHub issue: https://github.com/jgalazka/SB_publications/issues/1
"""

import pandas as pd
import sys
import os

def remove_duplicates(csv_file, backup=True):
    """Remove duplicate entries from the CSV file."""
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        print(f"Original number of rows: {len(df)}")
        
        # Create backup if requested
        if backup:
            backup_file = csv_file.replace('.csv', '_backup.csv')
            df.to_csv(backup_file, index=False)
            print(f"Backup created: {backup_file}")
        
        # Remove duplicates based on both Title and Link columns
        # Keep the first occurrence of each duplicate
        df_cleaned = df.drop_duplicates(subset=['Title', 'Link'], keep='first')
        
        print(f"Number of rows after removing duplicates: {len(df_cleaned)}")
        print(f"Removed {len(df) - len(df_cleaned)} duplicate rows")
        
        # Show which duplicates were removed
        duplicates = df[df.duplicated(subset=['Title', 'Link'], keep=False)]
        if len(duplicates) > 0:
            print("\nDuplicates that were removed:")
            for idx, row in duplicates.iterrows():
                print(f"  Row {idx}: {row['Title'][:60]}...")
        
        # Write the cleaned data back to the file
        df_cleaned.to_csv(csv_file, index=False)
        print(f"\nCleaned data written to {csv_file}")
        
        return True
        
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        return False

if __name__ == "__main__":
    csv_file = "SB_publication_PMC.csv"
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found")
        sys.exit(1)
    
    success = remove_duplicates(csv_file)
    if success:
        print("Duplicate removal completed successfully!")
    else:
        print("Duplicate removal failed!")
        sys.exit(1)

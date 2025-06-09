"""
Main script for running GCS file volume analysis.

This script defines the target GCS bucket and list of prefixes to process.
It calls the controller to process each prefix in sequence.

Execution flow:
1. For each prefix in PREFIX_LIST:
    - Fetch file records
    - Display statistics
    - Generate plots
    - Save CSV

To run:
    python main.py

Author: Your Name (optional)
"""

import controller

if __name__ == '__main__':
    # Target GCS bucket name
    BUCKET_NAME = 'shinise-dev-stockmiddleware-import'

    # List of prefixes to process
    PREFIX_LIST = [
        'init-stock',
        'stock-adjust', 
        'centerstock', 
        'purchase', 
        'stocktaking', 
        'asn', 
        'order', 
        'lomos', 
        'fresh-plan', 
        'fresh-label', 
        'sales', 
        'ec-sales'
    ]

    # Process each prefix
    for prefix in PREFIX_LIST:
        controller.process_prefix(bucket_name=BUCKET_NAME, prefix=prefix)

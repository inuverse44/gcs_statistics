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
from config_loader import load_config

if __name__ == '__main__':
    config = load_config()

    BUCKET_NAME = config['bucket_name']
    PREFIX_LIST = config['prefix_list']

    for prefix in PREFIX_LIST:
        controller.process_prefix(bucket_name=BUCKET_NAME, prefix=prefix)

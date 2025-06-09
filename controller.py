"""
Controller module for processing GCS file volume analysis.

This module defines the controller function `process_prefix` which manages the 
workflow of retrieving file data from GCS and generating outputs (statistics, plots, CSV).

Author: Your Name (optional)
"""

from typing import Optional

import pandas as pd

from model import GCSFileFetcher
import view


def process_prefix(bucket_name: str, prefix: str) -> None:
    """
    Process a single prefix in the given GCS bucket.

    This function orchestrates the following steps:
    1. Fetch file metadata from GCS under the specified prefix.
    2. Display statistics in the terminal and save to log.
    3. Generate time series and histogram plots.
    4. Save the file list summary as CSV.

    Args:
        bucket_name (str): The name of the GCS bucket.
        prefix (str): The prefix (path) within the bucket to process.

    Returns:
        None
    """
    print(f"\n=== Processing started: PREFIX = {prefix} ===")

    # Initialize data fetcher
    fetcher: GCSFileFetcher = GCSFileFetcher(bucket_name=bucket_name)
    df: pd.DataFrame = fetcher.fetch_file_records(prefix)

    # If no files found, skip processing
    if df.empty:
        print(f"⚠️ No files found under prefix: {prefix}")
        return

    # Execute view components (statistics, plots, CSV)
    view.show_statistics(df, prefix)
    view.show_file_list(df, prefix)
    view.plot_time_series(df, bucket_name, prefix)
    view.plot_histogram(df, bucket_name, prefix)
    view.plot_daily_file_counts(df, bucket_name, prefix)
    view.save_csv(df, prefix)

    print(f"\n✅ Completed: PREFIX = {prefix}")

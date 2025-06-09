"""
Model module for fetching file metadata from Google Cloud Storage (GCS).

This module provides:
- A utility function `human_readable_size` to convert bytes to human-readable format.
- A class `GCSFileFetcher` to retrieve file records from a specified GCS bucket and prefix.

Author: Your Name (optional)
"""

from typing import List, Dict
from google.cloud import storage
import pandas as pd
import numpy as np


def human_readable_size(size_bytes: int) -> str:
    """
    Convert a file size in bytes to a human-readable string with units.

    Args:
        size_bytes (int): File size in bytes.

    Returns:
        str: Human-readable size string (e.g., "10.5 MB").
    """
    if size_bytes == 0:
        return "0 B"
    size_name: tuple = ("B", "KB", "MB", "GB", "TB", "PB")
    i: int = int(np.floor(np.log(size_bytes) / np.log(1024)))
    p: float = np.power(1024, i)
    s: float = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


class GCSFileFetcher:
    """
    A class to fetch file metadata from a Google Cloud Storage bucket.

    Attributes:
        client (storage.Client): GCS client instance.
        bucket (storage.Bucket): Target GCS bucket object.
        max_results (int): Maximum number of blobs to retrieve.
    """

    def __init__(self, bucket_name: str, max_results: int = 10000) -> None:
        """
        Initialize the GCSFileFetcher.

        Args:
            bucket_name (str): Name of the GCS bucket.
            max_results (int, optional): Maximum number of blobs to fetch. Default is 10,000.
        """
        self.client: storage.Client = storage.Client()
        self.bucket: storage.Bucket = self.client.get_bucket(bucket_name)
        self.max_results: int = max_results

    def fetch_file_records(self, prefix: str) -> pd.DataFrame:
        """
        Fetch file records (metadata) from the specified prefix in the GCS bucket.

        The returned DataFrame contains the following columns:
        - file_name (str)
        - file_size_bytes (int)
        - created_time (datetime64[ns])
        - file_size_hr (str)  # human-readable size

        Args:
            prefix (str): Prefix (path) to search within the GCS bucket.

        Returns:
            pd.DataFrame: DataFrame containing file metadata.
        """
        blobs: storage.iterator = self.bucket.list_blobs(prefix=prefix, max_results=self.max_results)

        file_records: List[Dict[str, object]] = []
        counter: int = 0

        # Iterate over blobs and collect metadata
        for blob in blobs:
            if blob.name.endswith('/'):
                continue  # Skip "directory" entries

            counter += 1
            if counter % 100 == 0:
                print(f"Processed {counter} files... [{prefix}]")

            file_records.append({
                'file_name': blob.name,
                'file_size_bytes': blob.size,
                'created_time': blob.time_created
            })

        print(f"\n✅ Finished processing [{prefix}]. Total files: {counter}")

        # Convert to DataFrame
        df: pd.DataFrame = pd.DataFrame(file_records)
        if not df.empty:
            # Add human-readable size column
            df['file_size_hr'] = df['file_size_bytes'].apply(human_readable_size)
            # Ensure created_time is datetime type and sort
            df['created_time'] = pd.to_datetime(df['created_time'])
            df = df.sort_values('created_time')

        return df

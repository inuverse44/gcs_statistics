"""
View module for displaying and saving GCS file volume analysis results.

This module provides:
- Terminal display of file statistics and file lists.
- Generation of time series and histogram plots.
- Saving of summary CSV files.
- Logging of statistics to a log file.

Author: Your Name (optional)
"""

import os
import logging
from typing import Any

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from model import human_readable_size  # Utility function from model

# Ensure the output directory exists
os.makedirs('output', exist_ok=True)

# Configure logger
logger: logging.Logger = logging.getLogger('file_volume_logger')
logger.setLevel(logging.INFO)

# Create file handler for logging
file_handler: logging.Handler = logging.FileHandler('output/file_volume.log')
file_handler.setLevel(logging.INFO)

# Set formatter for the file handler
formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handler to logger if no handlers exist
if not logger.hasHandlers():
    logger.addHandler(file_handler)


def show_statistics(df: pd.DataFrame, prefix: str) -> None:
    """
    Display and log file size statistics for a given prefix.

    Statistics include:
    - Number of files
    - Mean file size
    - Standard deviation
    - Maximum file size
    - Minimum file size

    Args:
        df (pd.DataFrame): DataFrame containing file metadata.
        prefix (str): The prefix being analyzed.

    Returns:
        None
    """
    # Calculate statistical values
    mean_size: float = df['file_size_bytes'].mean()
    std_size: float = df['file_size_bytes'].std()
    max_size: int = df['file_size_bytes'].max()
    min_size: int = df['file_size_bytes'].min()

    # Print statistics to console
    print("\n===== File Size Statistics =====")
    print(f"PREFIX: {prefix}")
    print(f"Number of files: {len(df)}")
    print(f"Mean: {human_readable_size(mean_size)}")
    print(f"Standard Deviation: {human_readable_size(std_size)}")
    print(f"Maximum: {human_readable_size(max_size)}")
    print(f"Minimum: {human_readable_size(min_size)}")

    # Write statistics to log
    logger.info(f"PREFIX: {prefix}")
    logger.info(f"Number of files: {len(df)}")
    logger.info(f"Mean: {human_readable_size(mean_size)}")
    logger.info(f"Standard Deviation: {human_readable_size(std_size)}")
    logger.info(f"Maximum: {human_readable_size(max_size)}")
    logger.info(f"Minimum: {human_readable_size(min_size)}")


def show_file_list(df: pd.DataFrame, prefix: str) -> None:
    """
    Display the first 10 file records in the terminal.

    Args:
        df (pd.DataFrame): DataFrame containing file metadata.
        prefix (str): The prefix being analyzed.

    Returns:
        None
    """
    print("\n===== First 10 Files =====")
    for idx, row in df.head(10).iterrows():
        print(f"{row['file_name']}  ->  {row['file_size_hr']}   Created: {row['created_time']}")


def plot_time_series(df: pd.DataFrame, bucket_name: str, prefix: str) -> None:
    """
    Generate and save a time series plot of file sizes.

    Args:
        df (pd.DataFrame): DataFrame containing file metadata.
        bucket_name (str): The GCS bucket name.
        prefix (str): The prefix being analyzed.

    Returns:
        None
    """
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)

    # Create a figure and plot file sizes over time (converted to MB)
    plt.figure(figsize=(12, 6))
    plt.plot(df['created_time'], df['file_size_bytes'] / (1024 * 1024), marker='o', linestyle='-')

    # Label axes and set title
    plt.xlabel('Created Time')
    plt.ylabel('File Size (MB)')
    plt.title(f'File Size Time Series: gs://{bucket_name}/{prefix}')

    # Enable grid and format x-axis dates
    plt.grid(True)
    plt.tight_layout()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gcf().autofmt_xdate()

    # Save plot to output directory
    filename: str = f'output/file_size_timeseries_{prefix}.png'
    plt.savefig(filename)
    plt.close()

    print(f"\n✅ Saved: {filename}")


def plot_file_numbers(df: pd.DataFrame, bucket_name: str, prefix: str) -> None:
    """
    Generate and save a time series plot of file count per timestamp.

    Args:
        df (pd.DataFrame): DataFrame containing file metadata.
        bucket_name (str): The GCS bucket name.
        prefix (str): The prefix being analyzed.

    Returns:
        None
    """
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)

    # Create a figure and plot file sizes over time (placeholder for file count)
    plt.figure(figsize=(12, 6))
    plt.plot(df['created_time'], df['file_size_bytes'] / (1024 * 1024), marker='o', linestyle='-')

    # Label axes and set title
    plt.xlabel('Created Time')
    plt.ylabel('File numbers')
    plt.title(f'File Numbers Series: gs://{bucket_name}/{prefix}')

    # Enable grid and format x-axis dates
    plt.grid(True)
    plt.tight_layout()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gcf().autofmt_xdate()

    # Save plot to output directory
    filename: str = f'output/file_numbers_{prefix}.png'
    plt.savefig(filename)
    plt.close()

    print(f"\n✅ Saved: {filename}")


def plot_histogram(df: pd.DataFrame, bucket_name: str, prefix: str) -> None:
    """
    Generate and save a histogram of file sizes using the Freedman–Diaconis rule.

    Args:
        df (pd.DataFrame): DataFrame containing file metadata.
        bucket_name (str): The GCS bucket name.
        prefix (str): The prefix being analyzed.

    Returns:
        None
    """
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)

    # Convert file sizes to megabytes
    file_sizes_mb: np.ndarray = df['file_size_bytes'] / (1024 * 1024)

    # Calculate IQR and number of bins using Freedman–Diaconis rule
    q25, q75 = np.percentile(file_sizes_mb, [25, 75])
    iqr: float = q75 - q25
    n: int = len(file_sizes_mb)
    bin_width: float = 2 * iqr / (n ** (1 / 3)) if n > 0 else 1.0
    bin_count: int = max(int(np.ceil((file_sizes_mb.max() - file_sizes_mb.min()) / bin_width)), 1)

    # Print Freedman–Diaconis rule details
    print(f"\n===== Freedman–Diaconis Rule =====")
    print(f"IQR: {iqr}")
    print(f"Bin width: {bin_width}")
    print(f"Number of bins: {bin_count}")

    # Create a histogram plot
    plt.figure(figsize=(10, 6))
    plt.hist(file_sizes_mb, bins=bin_count, edgecolor='black')

    # Label axes and set title
    plt.xlabel('File Size (MB)')
    plt.ylabel('Number of Files')
    plt.title(f'File Size Distribution: gs://{bucket_name}/{prefix}')
    plt.grid(axis='y')
    plt.tight_layout()

    # Save plot to output directory
    filename: str = f'output/file_size_distribution_{prefix}.png'
    plt.savefig(filename)
    plt.close()

    print(f"✅ Saved: {filename}")


def plot_daily_file_counts(df: pd.DataFrame, bucket_name: str, prefix: str) -> None:
    """
    Aggregate files stored in GCS by date and save a time series plot of file counts.

    Args:
        df (pd.DataFrame): DataFrame returned by GCSFileFetcher.fetch_file_records,
                           where 'created_time' column is of datetime64 dtype.
        bucket_name (str): GCS bucket name (e.g., 'my-gcs-bucket').
        prefix (str): Prefix path (e.g., 'logs/2025/'), used in output filename.

    Returns:
        None
    """
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)

    # 1) Extract date-only (convert datetime64 to Python date object)
    df['date_only'] = df['created_time'].dt.date  # type: ignore

    # 2) Group by date and count number of files per day
    daily_counts: pd.DataFrame = df.groupby('date_only').size().reset_index(name='file_count')

    # 3) Create a time series plot for daily file counts
    plt.figure(figsize=(12, 6))
    plt.plot(daily_counts['date_only'], daily_counts['file_count'], marker='o', linestyle='-')

    # Label axes and set title
    plt.xlabel('Date')
    plt.ylabel('Number of Files')
    plt.title(f'Daily File Count: gs://{bucket_name}/{prefix}')
    plt.grid(True)

    # Format x-axis dates as YYYY-MM-DD and rotate labels
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()

    # 4) Save plot to output directory
    safe_bucket: str = bucket_name.replace("/", "_")
    safe_prefix: str = prefix.replace("/", "_")
    filename: str = f'output/daily_file_count_{safe_bucket}_{safe_prefix}.png'
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

    print(f"\n✅ Saved Daily File Count Plot: {filename}")


def save_csv(df: pd.DataFrame, prefix: str) -> None:
    """
    Save the file metadata DataFrame as a CSV file.

    Args:
        df (pd.DataFrame): DataFrame containing file metadata.
        prefix (str): The prefix being analyzed.

    Returns:
        None
    """
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)

    # Save DataFrame to CSV without index column
    filename: str = f'output/file_list_summary_{prefix}.csv'
    df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")

import os
import csv

def read_log_file(file_path):
    """Read and return the content of a log file."""
    with open(file_path, 'r') as file:
        return file.readlines()

def write_to_csv(file_path, fieldnames, data):
    """Write data to a CSV file."""
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
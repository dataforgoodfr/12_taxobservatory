import os
import hashlib
import argparse
import glob
import csv

def get_file_checksum(file_path):
    """Calculate SHA-256 checksum for a file"""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def compare_folders(folder_a, folder_b, output_file):
    """Compare contents of two folders based on file checksums"""
    pdfs_a = glob.glob(os.path.join(folder_a, '**/*.pdf'), recursive=True)
    pdfs_b = glob.glob(os.path.join(folder_b, '**/*.pdf'), recursive=True)

    checksums_a = {get_file_checksum(file): file for file in pdfs_a}
    checksums_b = {get_file_checksum(file): file for file in pdfs_b}

    common_checksums = set(checksums_a) & set(checksums_b)
    unique_checksums_a = set(checksums_a) - common_checksums
    unique_checksums_b = set(checksums_b) - common_checksums

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['PDF File', 'Checksum', 'Status'])

        for checksum in unique_checksums_a:
            file_path = checksums_a[checksum]
            writer.writerow([os.path.basename(file_path), checksum, f'Only in {folder_a}'])

        for checksum in unique_checksums_b:
            file_path = checksums_b[checksum]
            writer.writerow([os.path.basename(file_path), checksum, f'Only in {folder_b}'])

        for checksum in common_checksums:
            file_path_a = checksums_a[checksum]
            file_path_b = checksums_b[checksum]
            writer.writerow([os.path.basename(file_path_a), checksum, 'In both folders'])
            writer.writerow([os.path.basename(file_path_b), checksum, 'In both folders'])
            
    print(f"Results saved to {output_file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare contents of two folders based on file checksums')
    parser.add_argument(
        'folder_a',
        type=str,
        help='Path to folder A'
        )
    parser.add_argument(
        'folder_b',
        type=str,
        help='Path to folder B'
        )
    parser.add_argument(
        'output_file',
        type=str,
        help='Path to output CSV file'
        )
    args = parser.parse_args()

    compare_folders(args.folder_a, args.folder_b, args.output_file)


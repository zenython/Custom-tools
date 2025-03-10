import argparse
import csv
import math
import os

# Function to read data from a text file
def read_data_from_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            # Strip any leading/trailing whitespace
            domain = line.strip()
            if domain:  # Ensure the line is not empty
                data.append(domain)
    return data

def write_csv(filename, domains, start_index):
    """
    Write a CSV file with a header and domain-description pairs.
    The description is generated as "scan{n}" based on the domain's global position.
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Address', 'Description'])  # Write header row
        for i, domain in enumerate(domains):
            writer.writerow([domain, f"scan{start_index + i + 1}"])

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process a text file into partitioned CSV files.')
    parser.add_argument('-i', '--input', required=True,
                        help='Path to the input text file containing domain names')
    parser.add_argument('-o', '--output', required=True,
                        help='Base path to the output CSV file(s)')
    parser.add_argument('-p', '--partition',
                        help='Partition option: either a positive integer to split equally into that many parts, or "A" for automatic partitioning with up to 500 domains per file',
                        default=None)

    # Parse the arguments
    args = parser.parse_args()

    # Read domains from the input file
    domains = read_data_from_file(args.input)
    total = len(domains)

    if total == 0:
        print("No domains found in the input file.")
        return

    # Partitioning option provided
    if args.partition:
        # Automatic partitioning: -p A (or a/A)
        if args.partition.upper() == 'A':
            max_domains_per_file = 500
            num_parts = math.ceil(total / max_domains_per_file)
            for part in range(num_parts):
                start = part * max_domains_per_file
                end = min(total, (part + 1) * max_domains_per_file)
                base, ext = os.path.splitext(args.output)
                filename = f"{base}_part{part + 1}{ext}"
                write_csv(filename, domains[start:end], start)
            print(f"CSV files created successfully: {num_parts} part(s) with up to 500 domains each.")
        else:
            try:
                parts = int(args.partition)
                if parts <= 0:
                    raise ValueError
            except ValueError:
                print("Invalid partition argument. Provide a positive integer or 'A'.")
                return

            chunk_size = math.ceil(total / parts)
            for part in range(parts):
                start = part * chunk_size
                end = min(total, (part + 1) * chunk_size)
                base, ext = os.path.splitext(args.output)
                filename = f"{base}_part{part + 1}{ext}"
                write_csv(filename, domains[start:end], start)
            print(f"CSV files created successfully: {parts} part(s) created by splitting equally.")
    else:
        # No partition option, write to a single CSV file.
        write_csv(args.output, domains, 0)
        print(f"CSV file created successfully at {args.output}!")

if __name__ == '__main__':
    main()

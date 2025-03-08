import argparse
import csv

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

def generate_descriptions(num_items):
    # Generate descriptions in the format "scan1", "scan2", etc.
    return [f"scan{i + 1}" for i in range(num_items)]

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process a text file into a CSV file.')
    parser.add_argument('-i', '--input', required=True, help='Path to the input text file containing domain names')
    parser.add_argument('-o', '--output', required=True, help='Path to the output CSV file')

    # Parse the arguments
    args = parser.parse_args()

    # Read domains from the input file
    domains = read_data_from_file(args.input)
    
    # Generate descriptions based on the number of domains
    descriptions = generate_descriptions(len(domains))

    # Prepare data for CSV
    data = list(zip(domains, descriptions))

    # Write data to the CSV file
    with open(args.output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Address', 'Description'])  # Write header row
        writer.writerows(data)

    print(f"CSV file created successfully at {args.output}!")

if __name__ == '__main__':
    main()

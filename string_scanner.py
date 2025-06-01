import re
import sys
import requests
import argparse
import jsbeautifier

from termcolor import colored

def fetch_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for 4xx/5xx status codes
        return response.text
    except requests.RequestException as e:
        print(f"[!] Error fetching URL: {e}")
        sys.exit(1)

def beautify_content(content):
    # Beautify JavaScript/HTML content
    opts = jsbeautifier.default_options()
    opts.indent_size = 2
    return jsbeautifier.beautify(content, opts)

def find_js_strings(content, url):
    # Match single, double, and backtick-quoted JS strings (with escapes)
    pattern = re.compile(r"""(['"])(?:\\.|(?!\1)[^\\\r\n])*\1|`(?:\\.|[^\\`])*`""")

    for line_number, line in enumerate(content.splitlines(), start=1):
        if pattern.search(line):
            print(colored("URL: ", "red") + url + " at " + colored("line ", "red") + str(line_number))
            print(colored(">> ", "blue") + line.strip())
            print()

def main():
    parser = argparse.ArgumentParser(description="String_scanner with beautification")
    parser.add_argument('-l', '--list', type=str, help='Path to targets file')
    parser.add_argument('-t', '--target', type=str, help='Target URL')

    args = parser.parse_args()

    if args.list:
        with open(args.list, 'r') as f:
            urls = f.read().splitlines()
            for url in urls:
                content = fetch_url_content(url)
                beautified = beautify_content(content)
                find_js_strings(beautified, url)
    elif args.target:
        url = args.target
        content = fetch_url_content(url)
        beautified = beautify_content(content)
        find_js_strings(beautified, url)
    else:
        print(f"Usage: python {sys.argv[0]} OPTIONS")
        print("OPTIONS")
        print("--target, -t <URL> = Specify target URL")
        print("--list, -l <PATH> = Path to file containing URLs, one on a line")
        sys.exit(1)

if __name__ == "__main__":
    main()

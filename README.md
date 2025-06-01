# Strings but for web
This is a very basic tool for finding api endpoints on a URL. It only extracts double-quoted, single-quoted, backticked strings from a source. Combine this with katana for web crawling and grep patterns to find api endpoints.

## Example workflow
1) Install katana by projectdiscovery
2) Run the following command for api discovery<br>
   ```katana -u <URL> -o targets.txt --depth 2 | python string_scanner.py -l targets.txt | grep "/api"```
   It's advisable to increase depth in katana to discover more files and then run the tool

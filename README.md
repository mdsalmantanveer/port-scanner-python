# Port Scanner

A simple Python port scanner that checks common network ports on a website or IP address.

## Features

- Scans common ports such as `21`, `22`, `80`, `443`, and `8080`
- Accepts either a domain name or an IP address
- Detects and displays the target IP address
- Shows service names such as `HTTP`, `SSH`, `FTP`, and `DNS`
- Measures and displays the total scan time
- Attempts basic banner grabbing for open services
- Uses multithreading for faster scanning
- Supports command-line usage such as `python port_scanner.py google.com --fast`
- Saves scan output to `scan_results.txt`
- Handles invalid targets cleanly
- Uses a socket timeout to avoid waiting too long

## Requirements

- Python 3

No external Python packages are required.

## How to Run

Open a terminal in this folder and run:

```bash
python port_scanner.py
```

Then enter a website or IP address when prompted:

```text
Enter website or IP, e.g. google.com: google.com
```

You can also pass the target directly from the command line:

```bash
python port_scanner.py google.com
```

Fast scan mode checks a smaller list of high-value ports:

```bash
python port_scanner.py google.com --fast
```

You can also change timeout, thread count, and output file:

```bash
python port_scanner.py google.com --timeout 2 --workers 30 --output scan_results.txt
```

Example output:

```text
Scanning google.com (142.250.190.14)
---------------------------------------------
Port 21    (FTP) is CLOSED
Port 22    (SSH) is CLOSED
Port 80    (HTTP) is OPEN
  Server info: HTTP/1.1 301 Moved Permanently Location: http://www.google.com/
Port 443   (HTTPS) is OPEN
  Server info: No banner received
Port 8080  (HTTP Alternate) is CLOSED
---------------------------------------------
Scan completed in 2.30 seconds
Results saved to scan_results.txt
```

## Common Ports Scanned

```python
[21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 8080]
```

## Fast Mode Ports

When `--fast` is used, the scanner checks:

```python
[21, 22, 25, 53, 80, 443, 8080]
```

## Saved Results

Every scan is saved to:

```text
scan_results.txt
```

To save to a different file:

```bash
python port_scanner.py google.com --output my_scan.txt
```

## Service Names

The scanner displays common service names beside each port:

```text
Port 80 (HTTP) is OPEN
Port 22 (SSH) is CLOSED
Port 443 (HTTPS) is OPEN
```

## Banner Grabbing

When a port is open, the scanner tries to collect basic service information:

```text
Server info: SSH-2.0-OpenSSH_9.2
```

Some services do not send banners automatically, so the output may show:

```text
Server info: No banner received
```

## Important Note

Only scan websites, servers, or networks that you own or have permission to test.

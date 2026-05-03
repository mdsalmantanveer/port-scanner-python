import argparse
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 8080]
FAST_PORTS = [21, 22, 25, 53, 80, 443, 8080]
RESULTS_FILE = Path("scan_results.txt")

SERVICE_NAMES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    8080: "HTTP Alternate",
}

HTTP_PORTS = {80, 8080}


def get_service_name(port):
    """Return a readable service name for a port."""
    return SERVICE_NAMES.get(port, "Unknown")


def grab_banner(sock, target, port):
    """Try to collect a short service banner from an open socket."""
    try:
        if port in HTTP_PORTS:
            request = f"HEAD / HTTP/1.1\r\nHost: {target}\r\nConnection: close\r\n\r\n"
            sock.sendall(request.encode("ascii"))

        banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        return " ".join(banner.splitlines()) if banner else "No banner received"
    except socket.timeout:
        return "No banner received"
    except socket.error:
        return "Banner unavailable"


def scan_port(target, target_ip, port, timeout=1):
    """Scan one port and return its status, service name, and banner."""
    result = {
        "port": port,
        "service": get_service_name(port),
        "is_open": False,
        "banner": "",
    }

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result["is_open"] = sock.connect_ex((target_ip, port)) == 0

            if result["is_open"]:
                result["banner"] = grab_banner(sock, target, port)
    except socket.error:
        result["banner"] = "Connection error"

    return result


def build_report(target, target_ip, results, elapsed_time):
    """Build a printable scan report."""
    lines = [
        f"Scanning {target} ({target_ip})",
        "-" * 45,
    ]

    for result in sorted(results, key=lambda item: item["port"]):
        status = "OPEN" if result["is_open"] else "CLOSED"
        lines.append(f"Port {result['port']:<5} ({result['service']}) is {status}")

        if result["is_open"]:
            lines.append(f"  Server info: {result['banner']}")

    lines.extend([
        "-" * 45,
        f"Scan completed in {elapsed_time:.2f} seconds",
    ])

    return "\n".join(lines)


def save_report(report, output_file=RESULTS_FILE):
    """Save the scan report to a text file."""
    output_file.write_text(report + "\n", encoding="utf-8")


def scan_ports(target, ports, timeout=1, max_workers=20, output_file=RESULTS_FILE):
    """Scan multiple ports on a target."""
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("Invalid website or IP address.")
        return None

    start_time = time.perf_counter()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {
            executor.submit(scan_port, target, target_ip, port, timeout): port
            for port in ports
        }

        results = [future.result() for future in as_completed(future_to_port)]

    elapsed_time = time.perf_counter() - start_time
    report = build_report(target, target_ip, results, elapsed_time)
    print(f"\n{report}")
    save_report(report, output_file)
    print(f"Results saved to {output_file}")

    return results


def parse_args():
    """Parse command-line options."""
    parser = argparse.ArgumentParser(description="Scan common ports on a website or IP address.")
    parser.add_argument("target", nargs="?", help="Website or IP address to scan")
    parser.add_argument("--fast", action="store_true", help="Scan a smaller set of high-value ports")
    parser.add_argument("--timeout", type=float, default=1, help="Socket timeout in seconds")
    parser.add_argument("--workers", type=int, default=20, help="Number of scanner threads")
    parser.add_argument("--output", default=str(RESULTS_FILE), help="File to save scan results")
    return parser.parse_args()


def main():
    args = parse_args()
    target = args.target or input("Enter website or IP, e.g. google.com: ").strip()

    if not target:
        print("Target cannot be empty.")
        return

    ports = FAST_PORTS if args.fast else COMMON_PORTS
    scan_ports(
        target,
        ports,
        timeout=args.timeout,
        max_workers=args.workers,
        output_file=Path(args.output),
    )


if __name__ == "__main__":
    main()

import socket
import sys
import time
import threading
import concurrent.futures
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init()

# --- CONFIGURATION ---
COMMON_PORTS = {
    20: "FTP (Data)", 21: "FTP (Control)", 22: "SSH", 23: "Telnet",
    25: "SMTP (Email)", 53: "DNS", 80: "HTTP (Web)", 110: "POP3",
    135: "Windows RPC", 139: "NetBIOS", 143: "IMAP", 443: "HTTPS",
    445: "SMB (File Sharing)", 3306: "MySQL DB", 3389: "RDP",
    5357: "WSDAPI", 8080: "HTTP-Proxy"
}

scanning = True


def print_legal_disclaimer():
    """Forces the user to agree to terms before running"""
    print(f"\n{Fore.RED}" + "=" * 70)
    print(f"🛑  LEGAL WARNING & DISCLAIMER")
    print("=" * 70)
    print(
        f"{Fore.WHITE}1. This tool is for {Fore.YELLOW}EDUCATIONAL PURPOSES{Fore.WHITE} and {Fore.YELLOW}AUTHORIZED TESTING{Fore.WHITE} only.")
    print("2. Scanning targets without prior mutual consent is ILLEGAL.")
    print("3. The author is NOT responsible for any misuse or damage caused.")
    print(f"4. By using this tool, you accept full responsibility for your actions.")
    print(f"{Fore.RED}" + "=" * 70 + f"{Style.RESET_ALL}")

    agreement = input(f"\n{Fore.YELLOW}Type 'AGREE' to accept these terms and continue: {Style.RESET_ALL}")

    if agreement.strip().upper() != "AGREE":
        print(f"\n{Fore.RED}[!] You did not accept the terms. Exiting program...{Style.RESET_ALL}")
        sys.exit()
    else:
        print(f"\n{Fore.GREEN}[*] Terms accepted. Launching Ghost Hunter...{Style.RESET_ALL}")
        time.sleep(1)  # Dramatic pause


def spinner_animation():
    chars = ["|", "/", "-", "\\"]
    i = 0
    while scanning:
        sys.stdout.write(f"\r{Fore.CYAN}[*] Scanning target... {chars[i % len(chars)]}   {Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1


def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.8)

        result = s.connect_ex((ip, port))

        if result == 0:
            service_name = "Unknown"
            try:
                s.send(b'HEAD / HTTP/1.0\r\n\r\n')
                banner = s.recv(1024).decode().strip()
                if banner:
                    service_name = ''.join([c for c in banner if c.isprintable()])[:30]
            except:
                pass

            if service_name == "Unknown":
                service_name = COMMON_PORTS.get(port, "Unknown Service")

            s.close()
            return port, service_name
        s.close()
    except:
        pass
    return None


def run_master_scan(target, start_port, end_port):
    global scanning
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"\n{Fore.RED}[!] Error: Hostname could not be resolved.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.GREEN}" + "=" * 60)
    print(f"   🚀 NETWORK GHOST HUNTER v3.0")
    print(f"   🎯 Target: {Fore.WHITE}{target_ip}")
    print(f"   ⏰ Time:   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Fore.GREEN}" + "=" * 60 + f"{Style.RESET_ALL}\n")

    print(f"{Fore.YELLOW}{'PORT':<10} {'STATUS':<10} {'SERVICE'}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'-' * 4:<10} {'-' * 6:<10} {'-' * 7}{Style.RESET_ALL}")

    open_ports = []
    scanning = True
    spinner_thread = threading.Thread(target=spinner_animation)
    spinner_thread.start()

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            future_to_port = {executor.submit(scan_port, target_ip, port): port for port in
                              range(start_port, end_port + 1)}

            for future in concurrent.futures.as_completed(future_to_port):
                result = future.result()
                if result:
                    port_num, service = result
                    sys.stdout.write("\r" + " " * 50 + "\r")
                    print(f"{Fore.GREEN}{str(port_num):<10} {'OPEN':<10} {service}{Style.RESET_ALL}")
                    open_ports.append(port_num)

    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Scan aborted by user.{Style.RESET_ALL}")

    finally:
        scanning = False
        spinner_thread.join()

    print(f"\n{Fore.GREEN}" + "=" * 60)
    print(f"✅ SCAN COMPLETE. Found {len(open_ports)} open ports.")
    print(f"{Fore.GREEN}" + "=" * 60 + f"{Style.RESET_ALL}")


# --- MAIN MENU ---
if __name__ == "__main__":
    try:
        # STEP 1: FORCE THE LEGAL CHECK
        print_legal_disclaimer()

        # STEP 2: GET INPUTS
        t_in = input(f"\n{Fore.CYAN}Target IP (default 127.0.0.1): {Style.RESET_ALL}") or "127.0.0.1"
        s_in = input(f"{Fore.CYAN}Start Port (default 1): {Style.RESET_ALL}") or "1"
        e_in = input(f"{Fore.CYAN}End Port (default 1024): {Style.RESET_ALL}") or "1024"

        run_master_scan(t_in, int(s_in), int(e_in))

        input(f"\n{Fore.CYAN}Press Enter to exit...{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print("\nExiting.")
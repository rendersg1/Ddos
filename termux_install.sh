#!/bin/bash

echo -e "\e[1;36m"
cat << "EOF"

    ███████╗ ██████╗ ████████╗ ██████╗  ██████╗ ██╗     
    ██╔════╝██╔════╝ ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
    ███████╗██║  ███╗   ██║   ██║   ██║██║   ██║██║     
    ╚════██║██║   ██║   ██║   ██║   ██║██║   ██║██║     
    ███████║╚██████╔╝   ██║   ╚██████╔╝╚██████╔╝███████╗
    ╚══════╝ ╚═════╝    ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝

EOF
echo -e "\e[1;33m    ⚡ Next-Gen DDoS Tool - Termux Installer ⚡\e[0m\n"

# Check if running as root (optional for Termux)
if [ "$(id -u)" != "0" ]; then
    echo -e "\e[1;33m[!] Notice: Not running as root. Some features may be limited.\e[0m"
fi

echo -e "\e[1;36m[*] Updating package repositories...\e[0m"
pkg update -y && pkg upgrade -y

echo -e "\e[1;36m[*] Installing required packages...\e[0m"
pkg install -y python git openssl curl libpcap-dev

echo -e "\e[1;36m[*] Installing Python packages...\e[0m"
pip install --upgrade pip
pip install requests aiohttp asyncio colorama pysocks dnspython scapy

echo -e "\e[1;36m[*] Creating tool directory...\e[0m"
mkdir -p ~/SGTOOL

echo -e "\e[1;36m[*] Downloading SGTOOL source code...\e[0m"
cd ~/SGTOOL

# Download Python scripts directly
echo -e "\e[1;36m[*] Downloading main script...\e[0m"
curl -O https://raw.githubusercontent.com/yourusername/SGTOOL/main/start.py
curl -O https://raw.githubusercontent.com/yourusername/SGTOOL/main/easy_run.py

# Make scripts executable
chmod +x start.py easy_run.py

# Create a symbolic link (optional)
if [ -d "$PREFIX/bin" ]; then
    echo -e "\e[1;36m[*] Creating system-wide command...\e[0m"
    ln -sf ~/SGTOOL/easy_run.py $PREFIX/bin/sgtool
    chmod +x $PREFIX/bin/sgtool
fi

echo -e "\e[1;32m[+] Installation completed successfully!\e[0m"
echo -e "\e[1;32m[+] You can now use SGTOOL by running:\e[0m"
echo -e "\e[1;37m    cd ~/SGTOOL\e[0m"
echo -e "\e[1;37m    python easy_run.py <target> [options]\e[0m"

if [ -L "$PREFIX/bin/sgtool" ]; then
    echo -e "\e[1;32m[+] Or simply type:\e[0m"
    echo -e "\e[1;37m    sgtool <target> [options]\e[0m"
fi

echo -e "\e[1;33m[!] Example:\e[0m"
echo -e "\e[1;37m    python easy_run.py example.com --time 120 --threads 200\e[0m"
echo -e "\e[1;33m[!] Use responsibly and legally!\e[0m"

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
echo -e "\e[1;33m    ⚡ Next-Gen DDoS Tool - Cloud Installer ⚡\e[0m\n"

# Check if running as root
if [ "$(id -u)" != "0" ]; then
    echo -e "\e[1;33m[!] Not running as root. Some features may be limited.\e[0m"
fi

echo -e "\e[1;36m[*] Updating system packages...\e[0m"
sudo apt-get update -y 2>/dev/null || apt-get update -y 2>/dev/null

echo -e "\e[1;36m[*] Installing required dependencies...\e[0m"
sudo apt-get install -y python3 python3-pip git curl libpcap-dev 2>/dev/null || \
apt-get install -y python3 python3-pip git curl libpcap-dev 2>/dev/null

echo -e "\e[1;36m[*] Installing Python packages...\e[0m"
pip3 install --upgrade pip
pip3 install requests aiohttp asyncio colorama pysocks dnspython scapy

echo -e "\e[1;36m[*] Creating tool directory...\e[0m"
mkdir -p ~/Ddos

echo -e "\e[1;36m[*] Downloading DDoS tool source code...\e[0m"
cd ~/Ddos

# Download Python scripts directly
echo -e "\e[1;36m[*] Downloading main script...\e[0m"
curl -O https://raw.githubusercontent.com/rendersg1/Ddos/main/start.py
curl -O https://raw.githubusercontent.com/rendersg1/Ddos/main/easy_run.py

# Make scripts executable
chmod +x start.py easy_run.py

# Create a symbolic link (if possible)
if [ -d "/usr/local/bin" ] && [ "$(id -u)" = "0" ]; then
    echo -e "\e[1;36m[*] Creating system-wide command...\e[0m"
    ln -sf ~/Ddos/easy_run.py /usr/local/bin/ddostool
    chmod +x /usr/local/bin/ddostool
fi

echo -e "\e[1;32m[+] Installation completed successfully!\e[0m"
echo -e "\e[1;32m[+] You can now use the DDoS tool by running:\e[0m"
echo -e "\e[1;37m    cd ~/Ddos\e[0m"
echo -e "\e[1;37m    python3 easy_run.py <target> [options]\e[0m"

if [ -L "/usr/local/bin/ddostool" ]; then
    echo -e "\e[1;32m[+] Or simply type:\e[0m"
    echo -e "\e[1;37m    ddostool <target> [options]\e[0m"
fi

echo -e "\e[1;33m[!] Example:\e[0m"
echo -e "\e[1;37m    python3 easy_run.py example.com --time 120 --threads 200\e[0m"
echo -e "\e[1;33m[!] Use responsibly and legally!\e[0m"

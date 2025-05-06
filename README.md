# SGTOOL - Advanced DDoS Attack Tool

> **⚠️ DISCLAIMER: This tool is provided for security testing and educational purposes ONLY. Using this tool against websites or networks without explicit permission is illegal and unethical. The developers assume no liability for misuse or damage caused by this program.**

## 🚀 Features

- Multiple powerful attack methods targeting different network layers
- Asynchronous design for maximum performance
- Advanced socket and HTTP flood capabilities
- Auto-detection of the best attack method based on target
- Simple command-line interface with detailed statistics
- Easy installation on Termux and Google Cloud Terminal
- Progress tracking and real-time attack statistics
- Customizable thread count and attack duration

## 🔧 Installation

### Termux (Android)

```bash
# Download the installer script
curl -O https://raw.githubusercontent.com/yourusername/SGTOOL/main/termux_install.sh

# Make executable
chmod +x termux_install.sh

# Run installer
./termux_install.sh
```

### Google Cloud Terminal

```bash
# Download the installer script
curl -O https://raw.githubusercontent.com/yourusername/SGTOOL/main/cloud_install.sh

# Make executable
chmod +x cloud_install.sh

# Run installer
./cloud_install.sh
```

### Manual Installation (Any Linux/Unix System)

```bash
# Clone repository or download scripts
git clone https://github.com/yourusername/SGTOOL.git
cd SGTOOL

# Install dependencies
pip install requests aiohttp asyncio colorama pysocks dnspython scapy

# Make scripts executable
chmod +x start.py easy_run.py
```

## 📖 Usage

### Easy Mode (Recommended)

Use the simplified `easy_run.py` script for most cases:

```bash
python easy_run.py example.com --time 120 --threads 200
```

This will automatically detect the best attack method and launch an attack for 120 seconds using 200 threads.

### Advanced Mode

For more control, use the main script directly:

```bash
python start.py -m HTTP example.com -t 200 -d 60
```

### Command-line Arguments

**Easy Runner**:
- `target`: Target website URL (example.com)
- `--time`, `-t`: Attack duration in seconds (default: 60)
- `--threads`, `-n`: Number of threads (default: 100)
- `--method`, `-m`: Force specific attack method (HTTP, POST, SOCKET)
- `--help-methods`: Show information about attack methods

**Advanced Mode**:
- `method`: Attack method (HTTP, POST, SOCKET, AUTO)
- `target`: Target URL/IP address
- `-t`, `--threads`: Number of threads
- `-d`, `--duration`: Attack duration in seconds
- `--help-methods`: Show information about attack methods

## 💥 Attack Methods

- **HTTP**: HTTP Flood attack using GET requests, effective against web servers
- **POST**: HTTP Flood with large POST payloads, more resource-intensive on the target
- **SOCKET**: Raw socket flood attack, effective against TCP services
- **AUTO**: Automatically selects the best attack method based on the target

## 📊 Understanding Results

The tool shows real-time statistics during the attack:

- **Requests**: Total number of requests sent
- **RPS**: Requests per second (higher is better)
- **Success**: Percentage of successful requests (higher means target is handling the load)
- **Elapsed**: Time elapsed since the attack started

Example output interpretation:
- High success rate (90%+) with high RPS: Target is handling the load efficiently
- Low success rate (<50%) with any RPS: Target may be struggling or has protection
- Consistent RPS with dropping success rate: Target may be failing gradually

## ⚠️ Legal Warning

Improper use of this tool may violate local, state, and federal laws. Users are responsible for ensuring they have proper authorization before using this tool against any system or network.

## 📜 License

This project is licensed under MIT License - see the LICENSE file for details.

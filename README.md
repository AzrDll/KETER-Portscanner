# KETER Port Scanner

KETER Port Scanner is a robust, multithreaded port scanner written in Python. It allows you to scan specific ports or a range of ports on a host. 

## Features
- Multithreaded scanning for fast performance.
- Three scan modes: scan ports 1-1024, scan all ports (1-65535), or scan a custom range.
- Progress bar to monitor the scan in real-time.
- Gracefully handles interruptions and socket errors.

## Installation

Clone this repository using git:

```bash
git clone https://github.com/AzrDll/KETER-Portscanner.git
cd python-port-scanner
```

This script requires Python 3.6 or later. No additional packages are required.

## Usage

Run the script with the `-H` or `--host` option to specify the host (either a domain name or IP address) that you want to scan, and the `-m` or `--mode` option to specify the scanning mode.

```bash
python Robust_Portscanner.py -H www.example.com -m 1
```

For a custom range of ports, specify the `-s` or `--start` and `-e` or `--end` options:

```bash
python Robust_Portscanner.py -H www.example.com -m 3 -s 5000 -e 6000
```

## Modes

- Mode 1: Scan ports 1-1024
- Mode 2: Scan ports 1-65535
- Mode 3: Custom port range (specified with `-s` and `-e`)

## Contribution
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

---


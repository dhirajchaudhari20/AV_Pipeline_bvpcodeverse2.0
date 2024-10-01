import os
import time
import subprocess
import shutil
from datetime import datetime

# Constants for paths
TARGET_FOLDER = 'target_folder/'
INFECTED_FOLDER = 'infected_folder/'
LOG_FILE = 'logs/scanning_log.txt'

# Ensure folders exist
os.makedirs(INFECTED_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log(message):
    """Log messages to a file with a timestamp."""
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{datetime.now()}: {message}\n")

def scan_with_windows_defender(file_path):
    """Scan file using Windows Defender and return the result."""
    try:
        # Use PowerShell command to scan the file
        result = subprocess.run(
            ['powershell.exe', 'Start-MpScan', '-ScanType', 'QuickScan', '-File', file_path],
            capture_output=True,
            text=True
        )
        # Log the output from the scan
        log(result.stdout)
        return result.returncode  # 0 = no threats found, 1 = threats found
    except Exception as e:
        log(f"Error scanning {file_path}: {e}")
        return -1

def scan_files():
    """Scan files in the target folder continuously."""
    log("Scanning process started.")
    
    while True:
        for file_name in os.listdir(TARGET_FOLDER):
            file_path = os.path.join(TARGET_FOLDER, file_name)

            if os.path.isfile(file_path):
                log(f"Scanning {file_name}...")
                scan_result = scan_with_windows_defender(file_path)

                if scan_result == 1:
                    log(f"Threat detected in {file_name}. Moving to infected folder.")
                    shutil.move(file_path, os.path.join(INFECTED_FOLDER, file_name))
                elif scan_result == 0:
                    log(f"{file_name} is clean.")
                else:
                    log(f"Scan failed for {file_name}.")

        time.sleep(60)  # Wait for a minute before scanning again

if __name__ == '__main__':
    scan_files()

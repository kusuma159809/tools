import os
import platform
import subprocess

def get_system_uptime():
    system = platform.system()
    try:
        if system == "Windows":
            # Use 'net stats srv' and parse the output
            output = subprocess.check_output("net stats srv", shell=True, text=True)
            for line in output.splitlines():
                if "Statistics since" in line:
                    print("System uptime (Windows):", line)
                    return
            print("Could not determine uptime on Windows.")
        elif system == "Linux":
            # Use /proc/uptime
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                hours = int(uptime_seconds // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                seconds = int(uptime_seconds % 60)
                print(f"System uptime (Linux): {hours}h {minutes}m {seconds}s")
        elif system == "Darwin":
            # Use sysctl on macOS
            output = subprocess.check_output("sysctl -n kern.boottime", shell=True, text=True)
            import re
            import time
            match = re.search(r'sec = (\d+)', output)
            if match:
                boot_time = int(match.group(1))
                uptime_seconds = int(time.time()) - boot_time
                hours = uptime_seconds // 3600
                minutes = (uptime_seconds % 3600) // 60
                seconds = uptime_seconds % 60
                print(f"System uptime (macOS): {hours}h {minutes}m {seconds}s")
            else:
                print("Could not determine uptime on macOS.")
        else:
            print(f"Unsupported OS: {system}")
    except Exception as e:
        print("Error getting system uptime:", e)

if __name__ == "__main__":
    get_system_uptime()

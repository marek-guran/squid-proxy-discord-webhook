import requests
import os
import time

# Discord webhook URL
webhook_url = 'YOUR_WEBHOOK'

# Path to Squid access log
log_file = '/var/log/squid/access.log'

def send_to_discord(data):
    payload = {
        'content': data
    }
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("Data sent to Discord successfully.")
    except Exception as e:
        print(f"Error sending data to Discord: {str(e)}")

def tail_log(file):
    with open(file, 'r') as f:
        # Seek to the end of the file
        f.seek(0, os.SEEK_END)
        
        # Start tailing the log file
        while True:
            line = f.readline()
            if line:
                parts = line.strip().split()
                timestamp = int(float(parts[0]))  # Convert the timestamp to an integer
                ip = parts[2]
                destination = parts[6]
                send_to_discord(f"<t:{timestamp}:t> IP: {ip}, Destination: {destination}")
            else:
                time.sleep(1)

if __name__ == "__main__":
    tail_log(log_file)

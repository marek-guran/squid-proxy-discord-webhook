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
        f.seek(0, os.SEEK_END)
        
        while True:
            curr_position = f.tell()
            line = f.readline()
            if line:
                parts = line.strip().split()
                timestamp = int(float(parts[0]))
                ip = parts[2]
                destination = parts[6]
                send_to_discord(f"<t:{timestamp}:t> IP: {ip}, Destination: {destination}")
            else:
                # Sleep for a short time before checking for new lines
                time.sleep(1)
                # Check if the file was rotated
                if os.path.exists(file):
                    new_size = os.path.getsize(file)
                    if new_size < curr_position:
                        print("Log file rotated. Reopening...")
                        f.close()
                        f = open(file, 'r')
                        f.seek(0, os.SEEK_END)
                else:
                    print("Log file does not exist. Waiting for it to reappear...")
                    time.sleep(5)

if __name__ == "__main__":
    tail_log(log_file)
import socket
import binascii
import time
import re

SERVER_IP = "54.37.225.65"      # ← change to your server IP
SERVER_PORT = 2017           # ← change to your server port

DELAY = 0.5                  # delay between messages (seconds)

HEX_PATTERN = re.compile(r":([0-9A-Fa-f]+)$")

def extract_hex(line):
    """Extract the hex payload after the last colon."""
    match = HEX_PATTERN.search(line.strip())
    if match:
        return match.group(1)
    return None

def load_messages(filename):
    messages = []
    with open(filename, "r") as f:
        for line in f:
            hex_data = extract_hex(line)
            if hex_data:
                messages.append(hex_data)
    return messages

def simulate():
    msgs = load_messages("logs.txt")

    print(f"Loaded {len(msgs)} messages to replay")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))

    for i, msg in enumerate(msgs):
        data = binascii.unhexlify(msg)
        sock.sendall(data)
        print(f"[{i+1}] Sent: {msg}")
        time.sleep(DELAY)

    sock.close()
    print("Simulation finished.")

if __name__ == "__main__":
    simulate()

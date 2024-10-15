import csv
import random
from datetime import datetime, timedelta

# Define constants
PROTOCOLS = ["TCP", "UDP", "ICMP"]
QOS_CLASSES = ["eMBB", "uRLLC", "mMTC"]
SOURCE_IP_PREFIX = "192.168.1."
DEST_IP_PREFIX = "10.0.0."

# Function to generate random IP addresses
def generate_ip(prefix):
    return f"{prefix}{random.randint(1, 254)}"

# Function to generate a random packet size (in bytes)
def generate_packet_size():
    return random.randint(100, 1500)  # Typical packet sizes

# Function to generate random timestamps
def generate_timestamps(start, count):
    current_time = start
    timestamps = []
    for _ in range(count):
        timestamps.append(current_time)
        # Increment by random seconds
        current_time += timedelta(seconds=random.randint(1, 5))
    return timestamps

# Function to create a 5G traffic dataset
def create_5g_traffic_dataset(filename, num_entries):
    # Start time for the dataset
    start_time = datetime.now()

    # Generate random timestamps
    timestamps = generate_timestamps(start_time, num_entries)

    # Open CSV file for writing
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["Timestamp", "Source IP", "Destination IP", "Protocol", "Packet Size (Bytes)", "QoS Class"])

        # Write random data entries
        for i in range(num_entries):
            timestamp = timestamps[i].strftime("%Y-%m-%d %H:%M:%S")
            source_ip = generate_ip(SOURCE_IP_PREFIX)
            destination_ip = generate_ip(DEST_IP_PREFIX)
            protocol = random.choice(PROTOCOLS)
            packet_size = generate_packet_size()
            qos_class = random.choice(QOS_CLASSES)

            # Write row to CSV
            writer.writerow([timestamp, source_ip, destination_ip, protocol, packet_size, qos_class])

    print(f"Dataset '{filename}' created successfully with {num_entries} entries.")

# Example usage: Adjust the number of entries as needed
num_entries = int(input("Enter the number of entries for the dataset: "))
create_5g_traffic_dataset("5g_network_traffic.csv", num_entries)

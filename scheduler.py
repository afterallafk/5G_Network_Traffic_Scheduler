import csv
import queue
import random
import time
from datetime import datetime, timedelta

# Constants
LATENCY_THRESHOLD_URLLC = 0.005  # 5 ms threshold for uRLLC packets
TIME_SLOT = 0.1  # Scheduler time slot (100 ms)
OUTPUT_FILE = "scheduler_output.txt"  # File to store output

# Class to represent a packet
class Packet:
    def __init__(self, timestamp, source_ip, destination_ip, protocol, packet_size, qos_class):
        self.timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.protocol = protocol
        self.packet_size = int(packet_size)
        self.qos_class = qos_class
        self.arrival_time = datetime.now()
        self.deadline = self.calculate_deadline()

    def calculate_deadline(self):
        # Set a larger deadline for non-uRLLC packets
        if self.qos_class == "uRLLC":
            # No deadline check for uRLLC; all packets will be processed
            return None
        else:
            # Use a larger deadline for eMBB and mMTC packets
            return self.arrival_time + timedelta(seconds=0.2)  # 200 ms for eMBB

# Scheduler class
class Scheduler:
    def __init__(self):
        self.urllc_queue = queue.Queue()  # uRLLC packets queue (no priority)
        self.embb_queue = queue.Queue()    # eMBB packets queue
        self.mmtc_queue = queue.Queue()    # mMTC packets queue
        self.output_log = []  # List to store output for logging

    def add_packet(self, packet):
        if packet.qos_class == "uRLLC":
            self.urllc_queue.put(packet)  # All uRLLC packets are processed without deadlines
        elif packet.qos_class == "eMBB":
            self.embb_queue.put(packet)
        else:
            self.mmtc_queue.put(packet)

    def log_output(self, message):
        print(message)  # Print to console
        self.output_log.append(message)  # Store in output log

    def process_packets(self):
        while not self.urllc_queue.empty() or not self.embb_queue.empty() or not self.mmtc_queue.empty():
            # Process uRLLC packets first (all will be processed)
            while not self.urllc_queue.empty():
                packet = self.urllc_queue.get()
                self.log_output(f"Processing uRLLC Packet: {packet.source_ip} -> {packet.destination_ip}")

            # Then process eMBB packets
            while not self.embb_queue.empty():
                packet = self.embb_queue.get()
                # Check deadline
                if datetime.now() <= packet.deadline:
                    self.log_output(f"Processing eMBB Packet: {packet.source_ip} -> {packet.destination_ip}")
                else:
                    self.log_output(f"eMBB Packet dropped due to deadline miss: {packet.source_ip} -> {packet.destination_ip}")

            # Then process mMTC packets
            while not self.mmtc_queue.empty():
                packet = self.mmtc_queue.get()
                # Check deadline
                if datetime.now() <= packet.deadline:
                    self.log_output(f"Processing mMTC Packet: {packet.source_ip} -> {packet.destination_ip}")
                else:
                    self.log_output(f"mMTC Packet dropped due to deadline miss: {packet.source_ip} -> {packet.destination_ip}")

            # Wait for the next time slot
            time.sleep(TIME_SLOT)

        # After processing, write log to file
        self.write_output_to_file()

    def write_output_to_file(self):
        with open(OUTPUT_FILE, "w") as f:
            for line in self.output_log:
                f.write(f"{line}\n")  # Write each log entry on a new line
        print(f"Output written to {OUTPUT_FILE}")

# Function to load packets from CSV file
def load_packets_from_csv(filename):
    packets = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            packet = Packet(
                row["Timestamp"],
                row["Source IP"],
                row["Destination IP"],
                row["Protocol"],
                row["Packet Size (Bytes)"],
                row["QoS Class"]
            )
            packets.append(packet)
    return packets

# Example Usage
def main():
    scheduler = Scheduler()

    # Load packets from the CSV file
    packets = load_packets_from_csv("/home/aditya/UpgradScheduler/Dataset/5g_network_traffic.csv")

    # Add packets to the scheduler
    for packet in packets:
        scheduler.add_packet(packet)

    # Start processing the packets
    scheduler.process_packets()

if __name__ == "__main__":
    main()

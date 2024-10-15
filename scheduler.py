import csv
import queue
import random
import time
from datetime import datetime, timedelta

# Constants
LATENCY_THRESHOLD_URLLC = 0.001  # 1 ms threshold for uRLLC packets
TIME_SLOT = 0.1  # Scheduler time slot (100 ms)

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
        if self.qos_class == "uRLLC":
            return self.arrival_time + timedelta(seconds=LATENCY_THRESHOLD_URLLC)
        else:
            # Use a larger deadline for non-uRLLC packets
            return self.arrival_time + timedelta(seconds=TIME_SLOT)

# Priority queue comparator for Packet based on deadline
def packet_priority(packet):
    if packet.qos_class == "uRLLC":
        return 1  # High priority
    elif packet.qos_class == "eMBB":
        return 2  # Medium priority
    else:
        return 3  # Low priority

# Scheduler class
class Scheduler:
    def __init__(self):
        self.urllc_queue = queue.PriorityQueue()
        self.embb_queue = queue.Queue()
        self.mmtc_queue = queue.Queue()

    def add_packet(self, packet):
        if packet.qos_class == "uRLLC":
            # Add uRLLC packet to Priority Queue with deadlines
            self.urllc_queue.put((packet.deadline, packet))
        elif packet.qos_class == "eMBB":
            self.embb_queue.put(packet)
        else:
            self.mmtc_queue.put(packet)

    def process_packets(self):
        # Open a text file to store the output
        with open("scheduler_output.txt", "w") as output_file:
            while not self.urllc_queue.empty() or not self.embb_queue.empty() or not self.mmtc_queue.empty():
                # Process uRLLC packets first
                if not self.urllc_queue.empty():
                    deadline, packet = self.urllc_queue.get()
                    if datetime.now() <= deadline:
                        output_message = f"Processing uRLLC Packet: {packet.source_ip} -> {packet.destination_ip}\n"
                    else:
                        output_message = f"uRLLC Packet dropped due to deadline miss: {packet.source_ip} -> {packet.destination_ip}\n"
                # Process eMBB packets next
                elif not self.embb_queue.empty():
                    packet = self.embb_queue.get()
                    output_message = f"Processing eMBB Packet: {packet.source_ip} -> {packet.destination_ip}\n"
                # Process mMTC packets last
                elif not self.mmtc_queue.empty():
                    packet = self.mmtc_queue.get()
                    output_message = f"Processing mMTC Packet: {packet.source_ip} -> {packet.destination_ip}\n"

                # Print the output to console and write to file
                print(output_message.strip())
                output_file.write(output_message)

                # Wait for the next time slot
                time.sleep(TIME_SLOT)

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

import threading
import queue
import random
import time
import logging
from datetime import datetime, timedelta

# Constants
LATENCY_THRESHOLD_URLLC = 0.005  # 5 ms threshold for uRLLC packets
TIME_SLOT = 0.1  # Scheduler time slot (100 ms)

# Setup logging to file
logging.basicConfig(
    filename='scheduler_output.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

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
            return None
        else:
            return self.arrival_time + timedelta(seconds=0.2)  # 200 ms for eMBB

# Scheduler class
class Scheduler:
    def __init__(self):
        self.urllc_queue = queue.Queue()  # uRLLC packets queue
        self.embb_queue = queue.Queue()   # eMBB packets queue
        self.mmtc_queue = queue.Queue()   # mMTC packets queue
        self.lock = threading.Lock()  # To prevent race conditions

    def add_packet(self, packet):
        with self.lock:
            if packet.qos_class == "uRLLC":
                self.urllc_queue.put(packet)
            elif packet.qos_class == "eMBB":
                self.embb_queue.put(packet)
            else:
                self.mmtc_queue.put(packet)

    def process_packets(self):
        while True:
            with self.lock:
                # Process uRLLC packets first
                while not self.urllc_queue.empty():
                    packet = self.urllc_queue.get()
                    msg = f"Processing uRLLC Packet: {packet.source_ip} -> {packet.destination_ip}"
                    print(msg)
                    logging.info(msg)

                # Then process eMBB packets
                while not self.embb_queue.empty():
                    packet = self.embb_queue.get()
                    if datetime.now() <= packet.deadline:
                        msg = f"Processing eMBB Packet: {packet.source_ip} -> {packet.destination_ip}"
                    else:
                        msg = f"eMBB Packet dropped: {packet.source_ip} -> {packet.destination_ip}"
                    print(msg)
                    logging.info(msg)

                # Then process mMTC packets
                while not self.mmtc_queue.empty():
                    packet = self.mmtc_queue.get()
                    if datetime.now() <= packet.deadline:
                        msg = f"Processing mMTC Packet: {packet.source_ip} -> {packet.destination_ip}"
                    else:
                        msg = f"mMTC Packet dropped: {packet.source_ip} -> {packet.destination_ip}"
                    print(msg)
                    logging.info(msg)

            time.sleep(TIME_SLOT)

# Function to generate random IP addresses
def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

# Function to simulate real-time packet generation
def packet_generator(scheduler):
    protocols = ["TCP", "UDP"]
    qos_classes = ["uRLLC", "eMBB", "mMTC"]

    while True:
        # Simulate packet generation
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        source_ip = generate_random_ip()
        destination_ip = generate_random_ip()
        protocol = random.choice(protocols)
        packet_size = random.randint(50, 1500)  # Bytes
        qos_class = random.choice(qos_classes)

        # Create a packet and add it to the scheduler
        packet = Packet(timestamp, source_ip, destination_ip, protocol, packet_size, qos_class)
        scheduler.add_packet(packet)

        # Log and print the generated packet details
        msg = f"Generated Packet: {packet.source_ip} -> {packet.destination_ip}, Size: {packet.packet_size} bytes, QoS: {packet.qos_class}"
        print(msg)
        logging.info(msg)

        # Generate a new packet every 50ms
        time.sleep(0.05)

# Main function to start the scheduler and packet generator
def main():
    scheduler = Scheduler()

    # Start the packet generator thread
    generator_thread = threading.Thread(target=packet_generator, args=(scheduler,))
    generator_thread.daemon = True  # Daemonize thread so it exits when main program exits
    generator_thread.start()

    try:
        # Start processing packets in the main thread
        scheduler.process_packets()
    except KeyboardInterrupt:
        print("Stopping scheduler...")
        logging.info("Scheduler stopped.")

if __name__ == "__main__":
    main()

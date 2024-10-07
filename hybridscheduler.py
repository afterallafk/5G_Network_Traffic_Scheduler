import pandas as pd
import heapq

# Packet class definition
class Packet:
    def __init__(self, time, packet_size, qos_class):
        self.time = time
        self.packet_size = packet_size
        self.qos_class = qos_class

    def __lt__(self, other):
        # Prioritize based on QoS class and time
        qos_priority = {'uRLLC': 0, 'eMBB': 1, 'mMTC': 2}
        if qos_priority[self.qos_class] != qos_priority[other.qos_class]:
            return qos_priority[self.qos_class] < qos_priority[other.qos_class]
        return self.time < other.time  # Tie-breaker: prioritize earlier packets

    def __repr__(self):
        return f"Packet(time={self.time}, size={self.packet_size}, qos={self.qos_class})"

# Scheduler class definition
class Scheduler:
    def __init__(self, max_latency=1.0):
        self.queue = []  # Priority queue
        self.max_latency = max_latency  # Maximum allowable latency for uRLLC

    def add_packet(self, packet):
        heapq.heappush(self.queue, packet)

    def schedule(self, current_time):
        while self.queue:
            packet = self.queue[0]
            if packet.qos_class == 'uRLLC' and (current_time - packet.time) > self.max_latency:
                print(f"Scheduling uRLLC packet immediately: {packet}")
                heapq.heappop(self.queue)
            else:
                print(f"Scheduling packet: {packet}")
                heapq.heappop(self.queue)

# Load the dataset from CSV
def load_dataset(file_path):
    data = pd.read_csv(file_path)
    packets = []
    for index, row in data.iterrows():
        packet = Packet(row['time'], row['packet_size'], row['qos_class'])
        packets.append(packet)
    return packets

# Main function to run the scheduler
def run_scheduler(file_path):
    packets = load_dataset(file_path)
    scheduler = Scheduler()

    # Add packets to the scheduler
    for pkt in packets:
        scheduler.add_packet(pkt)

    # Simulate scheduling at a given time (e.g., t = 0.5 seconds)
    scheduler.schedule(0.5)

# Example usage
file_path = '/home/aditya/5Gscheduler/Dataset/5g_qos_traffic_data.csv'
run_scheduler(file_path)

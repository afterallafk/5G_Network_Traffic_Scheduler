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
    def __init__(self, max_latency=1.0, output_file="scheduler_output.txt"):
        self.queue = []  # Priority queue
        self.max_latency = max_latency  # Maximum allowable latency for uRLLC
        self.output_file = output_file  # Output file to store the results

    def add_packet(self, packet):
        heapq.heappush(self.queue, packet)

    def schedule(self, current_time):
        with open(self.output_file, 'w') as file:
            while self.queue:
                packet = self.queue[0]
                if packet.qos_class == 'uRLLC' and (current_time - packet.time) > self.max_latency:
                    print(f"Scheduling uRLLC packet immediately: {packet}")
                    file.write(f"Scheduling uRLLC packet immediately: {packet}\n")
                    heapq.heappop(self.queue)
                else:
                    print(f"Scheduling packet: {packet}")
                    file.write(f"Scheduling packet: {packet}\n")
                    heapq.heappop(self.queue)
        print(f"Scheduling complete. Output stored in {self.output_file}")

# Load the dataset from CSV
def load_dataset(file_path):
    data = pd.read_csv(file_path)
    packets = []
    for index, row in data.iterrows():
        packet = Packet(row['time'], row['packet_size'], row['qos_class'])
        packets.append(packet)
    return packets

# Main function to run the scheduler
def run_scheduler(file_path, output_file="scheduler_output.txt"):
    packets = load_dataset(file_path)
    scheduler = Scheduler(output_file=output_file)

    # Add packets to the scheduler
    for pkt in packets:
        scheduler.add_packet(pkt)

    # Simulate scheduling at a given time (e.g., t = 0.5 seconds)
    scheduler.schedule(0.5)

# Example usage
file_path = '/home/aditya/5Gscheduler/Dataset/5g_qos_traffic_data.csv'
run_scheduler(file_path, "scheduler_output.txt")

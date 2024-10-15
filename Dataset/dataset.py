import csv
import random
from datetime import datetime, timedelta

# Function to generate random timestamps
def generate_random_timestamp(start_time, end_time):
    return start_time + timedelta(seconds=random.randint(0, int((end_time - start_time).total_seconds())))

# Function to generate random network traffic data
def generate_random_traffic_data(num_entries):
    # Define the QoS classes
    qos_classes = ["uRLLC", "eMBB", "mMTC"]
    
    # Define the time range for the timestamps
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)  # Random timestamps within the next hour

    data = []
    for _ in range(num_entries):
        # Generate a random timestamp
        timestamp = generate_random_timestamp(start_time, end_time)

        # Generate random IP addresses
        source_ip = f"192.168.1.{random.randint(1, 254)}"
        destination_ip = f"192.168.1.{random.randint(1, 254)}"

        # Randomly choose a protocol and packet size
        protocol = random.choice(["TCP", "UDP"])
        packet_size = random.randint(64, 1500)  # Typical packet sizes

        # Randomly select a QoS class
        qos_class = random.choice(qos_classes)

        # Append the data as a dictionary
        data.append({
            "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "Source IP": source_ip,
            "Destination IP": destination_ip,
            "Protocol": protocol,
            "Packet Size (Bytes)": packet_size,
            "QoS Class": qos_class
        })

    return data

# Function to save the generated data to a CSV file
def save_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        fieldnames = ["Timestamp", "Source IP", "Destination IP", "Protocol", "Packet Size (Bytes)", "QoS Class"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Main function to generate and save the dataset
def main():
    num_entries = int(input("Enter the number of entries to generate: "))
    traffic_data = generate_random_traffic_data(num_entries)
    save_to_csv(traffic_data, "5g_network_traffic.csv")
    print(f"Generated {num_entries} entries and saved to 5g_network_traffic.csv.")

if __name__ == "__main__":
    main()

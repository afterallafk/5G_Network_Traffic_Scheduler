import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Load the data from the scheduler output file
with open("/home/aditya/Projects/MCN/UpgradScheduler/Automated/scheduler_output.log", "r") as file:
    data = file.readlines()

# Inspect the first few lines
print("Initial DataFrame Structure:")
for line in data[:5]:  # Print the first 5 lines
    print(line.strip())

# Extract relevant information from the log messages
timestamps = []
messages = []
source_ips = []
destination_ips = []
packet_sizes = []
qos_types = []

# Regular expression patterns for extracting information
pattern = re.compile(r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<action>.+?): (?P<value>.+)')

for line in data:
    match = pattern.match(line.strip())
    if match:
        timestamps.append(match.group('timestamp'))
        messages.append(match.group('action'))
        value = match.group('value')

        # Extract source IP, destination IP, packet size, and QoS from the value
        ip_pattern = re.compile(r'(?P<source_ip>[\d.]+) -> (?P<dest_ip>[\d.]+), Size: (?P<size>\d+) bytes, QoS: (?P<qos>\w+)')
        ip_match = ip_pattern.search(value)

        if ip_match:
            source_ips.append(ip_match.group('source_ip'))
            destination_ips.append(ip_match.group('dest_ip'))
            packet_sizes.append(int(ip_match.group('size')))  # Convert size to int
            qos_types.append(ip_match.group('qos'))
        else:
            source_ips.append(None)
            destination_ips.append(None)
            packet_sizes.append(None)
            qos_types.append(None)

# Create a DataFrame with the extracted information
output_data = pd.DataFrame({
    'Timestamp': pd.to_datetime(timestamps),
    'Message': messages,
    'Source IP': source_ips,
    'Destination IP': destination_ips,
    'Packet Size': packet_sizes,
    'QoS Type': qos_types
})

# Print out the new DataFrame
print("\nExtracted DataFrame:")
print(output_data.head())

# Example analysis: Count messages over time
message_counts = output_data['Message'].value_counts()

# Print out the message counts
print("\nMessage Counts:")
print(message_counts)

# Plotting the message counts
plt.figure(figsize=(10, 6))
sns.barplot(x=message_counts.index, y=message_counts.values, palette='viridis')
plt.title('Message Counts from Scheduler Output')
plt.xlabel('Message Type')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Additional analysis: Count of packets by QoS type
qos_counts = output_data['QoS Type'].value_counts()

# Plotting the QoS type counts
plt.figure(figsize=(10, 6))
sns.barplot(x=qos_counts.index, y=qos_counts.values, palette='plasma')
plt.title('Packet Counts by QoS Type')
plt.xlabel('QoS Type')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

# Additional analysis: Count of packets by source IP
source_ip_counts = output_data['Source IP'].value_counts()

# Plotting the source IP counts
plt.figure(figsize=(10, 6))
sns.barplot(x=source_ip_counts.index, y=source_ip_counts.values, palette='magma')
plt.title('Packet Counts by Source IP')
plt.xlabel('Source IP')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

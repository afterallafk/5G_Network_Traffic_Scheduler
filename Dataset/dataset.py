import numpy as np
import pandas as pd

# uRLLC parameters
packet_size_mean = 200  # Bytes
inter_arrival_time_mean = 0.001  # 1 ms

# Generate 100000 packets with exponential distribution
urrlc_packet_sizes = np.random.exponential(packet_size_mean, 100000)
urrlc_inter_arrival_times = np.random.exponential(inter_arrival_time_mean, 100000)

# eMBB parameters
packet_size_mean = 1500  # Bytes
inter_arrival_time_mean = 0.05  # 50 ms

# Generate 100000 packets
embb_packet_sizes = np.random.exponential(packet_size_mean, 100000)
embb_inter_arrival_times = np.random.exponential(inter_arrival_time_mean, 100000)

# mMTC parameters
packet_size_mean = 50  # Bytes
inter_arrival_time_mean = 1  # 1 second

# Generate 100000 packets
mmtc_packet_sizes = np.random.exponential(packet_size_mean, 100000)
mmtc_inter_arrival_times = np.random.exponential(inter_arrival_time_mean, 100000)

# Combine all data into one dataframe
data = {
    "time": np.cumsum(np.concatenate([urrlc_inter_arrival_times, embb_inter_arrival_times, mmtc_inter_arrival_times])),
    "packet_size": np.concatenate([urrlc_packet_sizes, embb_packet_sizes, mmtc_packet_sizes]),
    "qos_class": ['uRLLC'] * 100000 + ['eMBB'] * 100000 + ['mMTC'] * 100000
}

df = pd.DataFrame(data)
df.to_csv("5g_qos_traffic_data.csv", index=False)

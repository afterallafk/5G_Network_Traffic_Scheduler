# Automated Scheduler Simulation

## Overview
This project simulates a network packet scheduler designed to handle different Quality of Service (QoS) types, including uRLLC, eMBB, and mMTC. The simulation generates packets, processes them based on their QoS requirements, and logs the results. The logs can then be analyzed to gain insights into the performance and behavior of the scheduler.

## Features
- **Packet Generation**: Generates packets with random source and destination IPs, sizes, and QoS types.
- **Packet Processing**: Processes packets based on their QoS requirements, ensuring timely handling.
- **Logging**: Records all generated and processed packets to a log file for later analysis.
- **Data Extraction**: Parses log files to extract timestamps, messages, source and destination IPs, packet sizes, and QoS types.
- **Data Visualization**: Creates visual representations of:
  - Message counts from the scheduler output.
  - Packet counts categorized by QoS type.
  - Packet counts by source IP.

## Prerequisites
- MATLAB (for the simulation)
- Python 3.x (for the analysis script)
- Required Python libraries:
  - pandas
  - matplotlib
  - seaborn

You can install the required Python libraries using pip:

```
pip install pandas matplotlib seaborn
```

## Input
- The input for this analysis is a log file named scheduler_output.log. The log entries follow a specific format:
```
YYYY-MM-DD HH:MM:SS - Generated Packet: <source_ip> -> <destination_ip>, Size: <size> bytes, QoS: <qos_type>
```

## Example Log Entries
```
2024-10-16 17:49:31 - Generated Packet: 237.160.127.227 -> 204.81.25.39, Size: 1115 bytes, QoS: uRLLC
2024-10-16 17:49:31 - Processing uRLLC Packet: 237.160.127.227 -> 204.81.25.39
```

## Usage

1. Ensure your log file (scheduler_output.log) is in the same directory as the script.
2. Run the analysis script:
   ```
   python3 analyze_scheduler_output.py
   ```
3. The script will output the extracted DataFrame and display visualizations for message counts, QoS type distributions, and source IP counts.

## Code Explanation
The main tasks performed in the script include:

- **Loading Data**: The log file is read line by line to extract relevant details.
- **Regex Parsing**: Regular expressions are used to identify and extract the necessary information from each log entry.
- **DataFrame Creation**: A Pandas DataFrame is created to hold the extracted data for further analysis and visualization.
- **Visualization**: The data is visualized using Matplotlib and Seaborn for easy interpretation.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## Acknowledgments
- Thanks to the Python community for the invaluable libraries that made this project possible.
- Special thanks to Seaborn for beautiful data visualizations.

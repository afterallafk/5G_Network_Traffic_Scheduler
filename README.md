# 5G Network Traffic Scheduler Simulation

This project simulates a scheduler for processing 5G network traffic, focusing on different QoS (Quality of Service) classes: uRLLC (ultra-Reliable Low Latency Communication), eMBB (enhanced Mobile Broadband), and mMTC (massive Machine Type Communication). The simulation reads packet data from a CSV file, processes the packets based on their QoS classes, and logs the output in real-time.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Output](#output)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- Load network traffic packets from a CSV file.
- Process packets based on QoS classes: uRLLC, eMBB, and mMTC.
- Real-time output of processing status in the console.
- Log output to a text file for further analysis.
- Customizable time slots for scheduling.

## Requirements

- MATLAB R2020a or later.
- Basic knowledge of MATLAB programming.

## Getting Started

1. **Clone the Repository**
   ```bash
   git clone https://github.com/afterallafk/5G_QoS_Scheduler.git -b main schduler
   cd scheduler
   ```
2. **Prepare the CSV File**
   Ensure you have a CSV file named 5g_network_traffic.csv in the project directory. The CSV should contain the following columns:

  - timestamp
  - source_ip
  - destination_ip
  - protocol
  - packet_size
  - qos_class

3. **Open MATLAB Launch MATLAB and navigate to the project directory.**

## Usage

1. **Run the Simulation Script**
   Open the scheduler_simulation.m file in the MATLAB editor and click the Run button, or execute the following command in the MATLAB command window:
   ```
   scheduler
   ```

2. **View Output**
   The processing messages will be displayed in the console as the simulation runs. The output will also be saved in scheduler_output.txt.

## Output

- **Console Output**:
  Messages indicating the processing status of each packet.
- **Log File**: 
  scheduler_output.txt contains a log of all processed packets and any dropped packets due to deadline misses.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Acknowledgments
- Thanks to MATLAB for providing the platform to simulate and analyze network traffic.
- Special thanks to contributors and the community for their support.

### Instructions to Customize
- Replace `yourusername` in the clone command with your GitHub username.

Feel free to ask if you need any further modifications or additional content!

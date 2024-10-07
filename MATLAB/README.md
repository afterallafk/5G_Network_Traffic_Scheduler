# MATLAB simulation

- Load and Preprocess: 
  We load the dataset and extract columns like time, packet size, and QoS class.

- Scheduling Algorithm: 
  We sort packets based on priority (QoS class) and process them based on their size and arrival time.

- Transmission Simulation: 
  For each packet, the transmission is simulated by calculating the processing time (based on packet size) and logging the results.

- Save Results: 
  The output is stored in a text file.

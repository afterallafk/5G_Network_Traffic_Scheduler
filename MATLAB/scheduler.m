% 1. Load the dataset from the CSV file
data = readtable('5g_qos_traffic_data.csv');

% Extract the relevant columns
time = data.time;                % Packet arrival times
packet_size = data.packet_size;   % Packet sizes
qos_class = data.qos_class;       % QoS classes (uRLLC, eMBB, mMTC)

% 2. Define the Scheduling Algorithm
% Define a mapping for QoS priority (uRLLC > eMBB > mMTC)
qos_priority = containers.Map({'uRLLC', 'eMBB', 'mMTC'}, [1, 2, 3]);

% Convert the QoS class into priority values
priority = cell2mat(values(qos_priority, qos_class));

% Combine time and priority into a matrix to sort
packet_info = [priority, time];

% Sort packets based on priority first and then by time
[~, sorted_idx] = sortrows(packet_info, [1 2]);

% Get sorted packet information
sorted_time = time(sorted_idx);
sorted_packet_size = packet_size(sorted_idx);
sorted_qos_class = qos_class(sorted_idx);

% Display the sorted data
disp('Sorted packet schedule:');
for i = 1:length(sorted_time)
    fprintf('Time: %.2f, Packet Size: %d, QoS: %s\n', sorted_time(i), sorted_packet_size(i), sorted_qos_class{i});
end

% 3. Simulate Packet Transmission
% Define processing rate (in bits per second)
processing_rate = 1e6;  % 1 Mbps

% Initialize simulation variables
current_time = 0;   % The time in the simulation
processed_packets = {};  % Store results

% Process each packet
for i = 1:length(sorted_time)
    % Wait until the packet arrives
    if sorted_time(i) > current_time
        current_time = sorted_time(i);
    end
    
    % Calculate the processing time for the packet (size / rate)
    processing_time = sorted_packet_size(i) * 8 / processing_rate;  % Convert bytes to bits
    
    % Process the packet
    fprintf('Processing packet: Time %.2f, Size %d, QoS %s\n', ...
        current_time, sorted_packet_size(i), sorted_qos_class{i});
    
    % Log the result
    processed_packets{end+1} = sprintf('Packet processed: Start Time %.2f, End Time %.2f, Size %d, QoS %s', ...
        current_time, current_time + processing_time, sorted_packet_size(i), sorted_qos_class{i});
    
    % Update current time after processing
    current_time = current_time + processing_time;
end

% 4. Save Simulation Results to a File
output_file = 'simulation_results.txt';
fileID = fopen(output_file, 'w');

% Write the simulation results to the file
for i = 1:length(processed_packets)
    fprintf(fileID, '%s\n', processed_packets{i});
end

% Close the file
fclose(fileID);

disp(['Simulation complete. Results saved to ', output_file]);

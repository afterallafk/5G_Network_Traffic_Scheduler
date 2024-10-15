% Load packets from CSV file
function packets = load_packets_from_csv(filename)
    packets = {};
    fid = fopen(filename, 'r');
    if fid == -1
        error('File cannot be opened: %s', filename);
    end
    header = fgetl(fid);  % Read header line
    while ~feof(fid)
        line = fgetl(fid);
        data = strsplit(line, ',');
        packet = struct();
        packet.timestamp = datetime(data{1}, 'InputFormat', 'yyyy-MM-dd HH:mm:ss');
        packet.source_ip = data{2};
        packet.destination_ip = data{3};
        packet.protocol = data{4};
        packet.packet_size = str2double(data{5});
        packet.qos_class = data{6};
        packets{end+1} = packet;  % Append packet struct to the list
    end
    fclose(fid);
end

% Function to process packets
function process_packets(packets, TIME_SLOT)
    urllc_queue = {};  % uRLLC packets queue
    embb_queue = {};   % eMBB packets queue
    mmtc_queue = {};   % mMTC packets queue
    output_log = {};   % List to store output for logging

    % Add packets to respective queues
    for i = 1:length(packets)
        packet = packets{i};
        if strcmp(packet.qos_class, 'uRLLC')
            urllc_queue{end+1} = packet;  % All uRLLC packets processed
        elseif strcmp(packet.qos_class, 'eMBB')
            embb_queue{end+1} = packet;
        else
            mmtc_queue{end+1} = packet;
        end
    end

    % Process packets
    while ~isempty(urllc_queue) || ~isempty(embb_queue) || ~isempty(mmtc_queue)
        % Process uRLLC packets first
        while ~isempty(urllc_queue)
            packet = urllc_queue{1};  % Get first packet
            urllc_queue(1) = [];       % Remove it from the queue
            message = sprintf('Processing uRLLC Packet: %s -> %s', packet.source_ip, packet.destination_ip);
            disp(message);              % Display to console
            output_log{end+1} = message;  % Store in output log
        end

        % Process eMBB packets
        while ~isempty(embb_queue)
            packet = embb_queue{1};  % Get first packet
            embb_queue(1) = [];       % Remove it from the queue
            deadline = datetime('now') + seconds(0.2);  % 200 ms for eMBB
            if datetime('now') <= deadline
                message = sprintf('Processing eMBB Packet: %s -> %s', packet.source_ip, packet.destination_ip);
                disp(message);              % Display to console
                output_log{end+1} = message;  % Store in output log
            else
                message = sprintf('eMBB Packet dropped due to deadline miss: %s -> %s', packet.source_ip, packet.destination_ip);
                disp(message);              % Display to console
                output_log{end+1} = message;  % Store in output log
            end
        end

        % Process mMTC packets
        while ~isempty(mmtc_queue)
            packet = mmtc_queue{1};  % Get first packet
            mmtc_queue(1) = [];       % Remove it from the queue
            deadline = datetime('now') + seconds(0.2);  % 200 ms for mMTC
            if datetime('now') <= deadline
                message = sprintf('Processing mMTC Packet: %s -> %s', packet.source_ip, packet.destination_ip);
                disp(message);              % Display to console
                output_log{end+1} = message;  % Store in output log
            else
                message = sprintf('mMTC Packet dropped due to deadline miss: %s -> %s', packet.source_ip, packet.destination_ip);
                disp(message);              % Display to console
                output_log{end+1} = message;  % Store in output log
            end
        end

        % Wait for the next time slot
        pause(TIME_SLOT);
    end

    % Write log to file
    write_output_to_file(output_log);
end

% Function to write output to file
function write_output_to_file(output_log)
    fid = fopen('scheduler_output.txt', 'w');
    if fid == -1
        error('Cannot open file for writing.');
    end
    for i = 1:length(output_log)
        fprintf(fid, '%s\n', output_log{i});
    end
    fclose(fid);
    fprintf('Simulation complete. Results saved to scheduler_output.txt\n');
end

% Main function
function main()
    % Constants
    LATENCY_THRESHOLD_URLLC = 0.005;  % 5 ms threshold for uRLLC packets
    TIME_SLOT = 0.1;                   % Scheduler time slot (100 ms)
    OUTPUT_FILE = "scheduler_output.txt";  % File to store output

    % Load packets from the CSV file
    packets = load_packets_from_csv('/home/aditya/UpgradScheduler/Dataset/5g_network_traffic.csv');
    
    % Start processing the packets
    process_packets(packets, TIME_SLOT);  % Pass TIME_SLOT as an argument
end

% Call the main function
main();

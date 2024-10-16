% scheduler_simulation.m
% Constants
TIME_SLOT = 0.1; % Scheduler time slot (100 ms)
logFile = fopen('scheduler_output.txt', 'a');

% Function to generate random IP addresses
function ip = generate_random_ip()
    ip = sprintf('%d.%d.%d.%d', randi([1, 255]), randi([0, 255]), randi([0, 255]), randi([1, 255]));
end

% Function to create a packet
function packet = create_packet()
    protocols = ["TCP", "UDP"];
    qos_classes = ["uRLLC", "eMBB", "mMTC"];

    packet.timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
    packet.source_ip = generate_random_ip();
    packet.destination_ip = generate_random_ip();
    packet.protocol = protocols(randi([1, numel(protocols)]));
    packet.packet_size = randi([50, 1500]); % Bytes
    packet.qos_class = qos_classes(randi([1, numel(qos_classes)]));
    packet.arrival_time = datetime('now');
    packet.deadline = calculate_deadline(packet);
end

% Function to calculate packet deadline
function deadline = calculate_deadline(packet)
    if strcmp(packet.qos_class, "uRLLC")
        deadline = []; % No specific deadline for uRLLC
    else
        deadline = packet.arrival_time + seconds(0.2); % 200 ms for eMBB
    end
end

% Function to process the queues
function process_packets(scheduler, logFile)
    % Process uRLLC packets first
    for i = 1:length(scheduler.urllc_queue)
        packet = scheduler.urllc_queue{i};
        msg = sprintf("Processing uRLLC Packet: %s -> %s", packet.source_ip, packet.destination_ip);
        disp(msg);
        fprintf(logFile, "%s - %s\n", datestr(now, 'yyyy-mm-dd HH:MM:SS'), msg);
    end
    scheduler.urllc_queue = {};

    % Process eMBB packets
    for i = 1:length(scheduler.embb_queue)
        packet = scheduler.embb_queue{i};
        if datetime('now') <= packet.deadline
            msg = sprintf("Processing eMBB Packet: %s -> %s", packet.source_ip, packet.destination_ip);
        else
            msg = sprintf("eMBB Packet dropped: %s -> %s", packet.source_ip, packet.destination_ip);
        end
        disp(msg);
        fprintf(logFile, "%s - %s\n", datestr(now, 'yyyy-mm-dd HH:MM:SS'), msg);
    end
    scheduler.embb_queue = {};

    % Process mMTC packets
    for i = 1:length(scheduler.mmtc_queue)
        packet = scheduler.mmtc_queue{i};
        if datetime('now') <= packet.deadline
            msg = sprintf("Processing mMTC Packet: %s -> %s", packet.source_ip, packet.destination_ip);
        else
            msg = sprintf("mMTC Packet dropped: %s -> %s", packet.source_ip, packet.destination_ip);
        end
        disp(msg);
        fprintf(logFile, "%s - %s\n", datestr(now, 'yyyy-mm-dd HH:MM:SS'), msg);
    end
    scheduler.mmtc_queue = {};
end

% Function to add packets to the scheduler
function scheduler = add_packet(scheduler, packet)
    switch packet.qos_class
        case 'uRLLC'
            scheduler.urllc_queue{end + 1} = packet;
        case 'eMBB'
            scheduler.embb_queue{end + 1} = packet;
        case 'mMTC'
            scheduler.mmtc_queue{end + 1} = packet;
    end
end

% Main Scheduler Simulation
function run_scheduler_simulation(TIME_SLOT)
    % Create a struct to hold packet queues
    scheduler.urllc_queue = {};
    scheduler.embb_queue = {};
    scheduler.mmtc_queue = {};

    % Open the log file
    logFile = fopen('scheduler_output.txt', 'a');

    % Start the packet generation and processing loop
    tic; % Start timing
    while true
        % Generate a new packet every 50 ms
        if toc >= 0.05
            packet = create_packet();
            scheduler = add_packet(scheduler, packet);
            % Print the generated packet details
            msg = sprintf("Generated Packet: %s -> %s, Size: %d bytes, QoS: %s", ...
                packet.source_ip, packet.destination_ip, packet.packet_size, packet.qos_class);
            disp(msg);
            fprintf(logFile, "%s - %s\n", datestr(now, 'yyyy-mm-dd HH:MM:SS'), msg);
            tic; % Reset the timer after generating a packet
        end
        
        % Process packets from the queues
        if ~isempty(scheduler.urllc_queue) || ~isempty(scheduler.embb_queue) || ~isempty(scheduler.mmtc_queue)
            process_packets(scheduler, logFile);
        end

        % Pause for the scheduler time slot
        pause(TIME_SLOT);
    end
end

% Call the main function to run the simulation
run_scheduler_simulation(TIME_SLOT);

% Close the log file when done
fclose(logFile);

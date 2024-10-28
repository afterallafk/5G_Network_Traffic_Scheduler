import pandas as pd
from datetime import datetime, timedelta

class CPScheduler:
    def __init__(self, slots_per_frame, latency_constraint, alpha, gamma, dataset_path, frame_duration_minutes=5):
        self.slots_per_frame = slots_per_frame  # Total slots in a frame
        self.latency_constraint = latency_constraint  # Maximum allowed latency (L)
        self.alpha = alpha  # Target unreliability rate for URLLC
        self.gamma = gamma  # Update step for the reliability adjustment
        self.theta = self.alpha  # Initial threshold
        self.frame_duration = timedelta(minutes=frame_duration_minutes)  # Frame duration in minutes
        self.dataset = self.load_dataset(dataset_path)

    def load_dataset(self, dataset_path):
        """
        Load the dataset containing network traffic data.
        Assume dataset has columns: 'Timestamp', 'Source IP', 'Destination IP', 
        'Protocol', 'Packet Size (Bytes)', 'QoS Class'.
        """
        try:
            data = pd.read_csv(dataset_path, parse_dates=['Timestamp'])
            return data
        except FileNotFoundError:
            print(f"Dataset not found at {dataset_path}. Ensure the file path is correct.")
            return None

    def predict_slots(self, frame_start, frame_end, qos_class):
        """
        Use actual traffic from the dataset based on the frame time interval.
        qos_class can be 'uRLLC', 'eMBB', or 'mMTC'.
        """
        if self.dataset is None:
            return 0  # No data, so no packets to schedule

        # Filter packets by QoS class that fall within the frame time window
        packets = self.dataset[(self.dataset['Timestamp'] >= frame_start) & 
                               (self.dataset['Timestamp'] < frame_end) &
                               (self.dataset['QoS Class'] == qos_class)]

        return len(packets)

    def allocate_slots(self, urllc_packets, embb_packets, mmtc_packets):
        """
        Dynamic allocation strategy based on predicted slots for URLLC, eMBB, and mMTC.
        Prioritize URLLC, then allocate remaining slots to eMBB and mMTC.
        If URLLC requires more than its allocation, borrow from eMBB and mMTC.
        """
        max_urllc_slots = int(0.6 * self.slots_per_frame)  # Allow URLLC to use up to 60% of total slots if needed
        urllc_allocated = min(urllc_packets, max_urllc_slots)
        remaining_slots = self.slots_per_frame - urllc_allocated

        # Allocate eMBB next, dynamically adjusting if URLLC under-utilizes
        max_embb_slots = int(0.3 * self.slots_per_frame)
        embb_allocated = min(embb_packets, max(remaining_slots, max_embb_slots))
        remaining_slots -= embb_allocated

        # Allocate any remaining slots to mMTC
        mmtc_allocated = min(mmtc_packets, remaining_slots)

        return urllc_allocated, embb_allocated, mmtc_allocated

    def cp_based_scheduler(self):
        """
        CP-based dynamic adjustment of URLLC, eMBB, and mMTC allocation.
        """
        start_time = self.dataset['Timestamp'].min() if self.dataset is not None else datetime.now()
        frame_count = 100  # Total frames to simulate
        reliability_target = 1 - self.alpha
        success_count = 0

        for frame in range(frame_count):
            # Step 1: Define frame time interval
            frame_start = start_time + frame * self.frame_duration
            frame_end = frame_start + self.frame_duration

            # Step 2: Predict slots needed based on dataset for each class
            predicted_urllc = self.predict_slots(frame_start, frame_end, 'uRLLC')
            predicted_embb = self.predict_slots(frame_start, frame_end, 'eMBB')
            predicted_mmtc = self.predict_slots(frame_start, frame_end, 'mMTC')

            # Step 3: Allocate slots based on predictions
            urllc_allocated, embb_allocated, mmtc_allocated = self.allocate_slots(
                predicted_urllc, predicted_embb, predicted_mmtc
            )

            # Check if all URLLC packets are within latency
            if predicted_urllc <= urllc_allocated:
                success_count += 1
                feedback = 1  # Successful URLLC transmission
            else:
                feedback = 0  # Unsuccessful URLLC transmission

            # Step 4: Update theta using the feedback
            self.theta += self.gamma * (feedback - reliability_target)
            adjusted_alpha = max(0, min(1, self.theta))

            # Step 5: Print performance for the frame
            print(f"Frame {frame + 1}: Predicted URLLC = {predicted_urllc}, "
                  f"eMBB = {predicted_embb}, mMTC = {predicted_mmtc}, "
                  f"Allocated (URLLC, eMBB, mMTC) = ({urllc_allocated}, {embb_allocated}, {mmtc_allocated}), "
                  f"Success Rate: {success_count / (frame + 1):.2f}")

        print(f"\nFinal Success Rate over {frame_count} frames: {success_count / frame_count:.2f}")

if __name__ == "__main__":
    slots_per_frame = 50  # Increased slots per frame to handle higher demand
    latency_constraint = 2  # Example: Max latency allowed is 2 slots
    alpha = 0.1  # Example: Target unreliability rate (90% reliability)
    gamma = 0.05  # Adjustment step size
    dataset_path = "5g_network_traffic.csv"  # Replace with your dataset path

    scheduler = CPScheduler(slots_per_frame, latency_constraint, alpha, gamma, dataset_path)
    scheduler.cp_based_scheduler()

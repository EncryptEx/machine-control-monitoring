import datetime
import json
import logging
from azure.iot.device import IoTHubDeviceClient, Message
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration parameters
EQUIPMENT_ID = "lauzhack-pi2"
DATASOURCE = "10.0.4.60:8000"
IOT_HUB_CONNECTION_STRING="HostName=ra-develop-bobstconnect-01.azure-devices.net;DeviceId=LAUZHACKPI2;SharedAccessKey=2qKMAcYo0MmWoz93EG5x7hAYC5yUwckuCAIoTKv6utQ="

# Initialize the IoT Hub Device Client
device_client = IoTHubDeviceClient.create_from_connection_string(IOT_HUB_CONNECTION_STRING)

# Function to create a machine event message with custom timestamp
def create_machine_event(event_type, job_id, job_output_count, total_output_count, production_time, timestamp):
    return {
        "timestamp": timestamp.isoformat(),
        "equipmentId": EQUIPMENT_ID,
        "datasource": DATASOURCE,
        "type": event_type,
        "jobId": job_id,
        "jobOutputUnitCount": job_output_count,
        "totalOutputUnitCount": total_output_count,
        "totalProductionTime": production_time
    }

# Function to send a message to IoT Hub
def send_message_to_iot_hub(event_data):
    try:
        # Convert the dictionary to a JSON string
        json_data = json.dumps([event_data])

        # Create a message with the JSON data
        machine_event_message = Message(json_data)
        machine_event_message.content_type = "application/json"
        machine_event_message.content_encoding = "utf-8"
        machine_event_message.custom_properties["messageType"] = "MachineEvent"

        # Send the message
        logging.info(f"Sending JSON message to IoT Hub...")
        logging.info(f"Message content: {json_data}")
        device_client.send_message(machine_event_message)
        logging.info("Message sent successfully!")

    except Exception as e:
        logging.error(f"Failed to send message to IoT Hub: {e}")

# Main production scenario
def main():
    try:
        # Connect to IoT Hub
        logging.info("Connecting to IoT Hub...")
        device_client.connect()
        logging.info("Connected successfully!")

        # Set initial timestamp for the day before, at midnight
        start_timestamp = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
        start_timestamp = start_timestamp.replace(hour=0, minute=0, second=0, microsecond=0)

        # Simulation loop for the entire day, incrementing by 10 minutes
        job_id = "CerealBox-1"
        job_output_count = 0
        total_output_count = 0
        production_time = 0

        while start_timestamp.hour < 24:
            # Create a start production event
            start_event = create_machine_event(
                event_type="startProducing",
                job_id=job_id,
                job_output_count=job_output_count,
                total_output_count=total_output_count,
                production_time=production_time,
                timestamp=start_timestamp
            )
            send_message_to_iot_hub(start_event)

            # Simulate production for 10 minutes
            production_duration = 600  # 600 seconds = 10 minutes
            production_time += production_duration
            job_output_count += 10  # Increment job output count by 10 units (as an example)
            total_output_count += 10  # Increment total output count by 10 units

            # Move timestamp forward by 10 minutes
            start_timestamp += datetime.timedelta(minutes=10)

            # Create a stop production event after 10 minutes of production
            stop_event = create_machine_event(
                event_type="stopProducing",
                job_id=job_id,
                job_output_count=job_output_count,
                total_output_count=total_output_count,
                production_time=production_time,
                timestamp=start_timestamp
            )
            send_message_to_iot_hub(stop_event)

            # Move timestamp forward by another 10 minutes for the next cycle
            start_timestamp += datetime.timedelta(minutes=10)

            # Wait a short time to simulate processing delay (to avoid flooding)
            time.sleep(1)

    finally:
        # Disconnect from IoT Hub
        device_client.shutdown()
        logging.info("Disconnected from IoT Hub.")

if __name__ == "__main__":
    main()

import threading
import time
import json
import datetime
import logging
from fastapi import FastAPI
import RPi.GPIO as GPIO
from ina219 import INA219
from starlette.background import BackgroundTasks
from azure.iot.device import IoTHubDeviceClient, Message
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

WANTS_TO_SEND_TELEMETRY = True
app = FastAPI()

BOXES_FILE = 'boxes.txt'

def read_total_boxes():
    with open(BOXES_FILE, 'r') as file:
        return int(file.read().strip())
    

def write_total_boxes(total_boxes):
    try: 
        with open(BOXES_FILE, 'w') as file:
            file.write(str(total_boxes))
        return total_boxes
    except FileNotFoundError:
        with open(BOXES_FILE, 'x') as file:
            file.write(str(total_boxes))
        return total_boxes


def increment_total_boxes():
    global totalBoxesCount, deltaBox
    totalBoxesCount += 1
    deltaBox += 1
    write_total_boxes(totalBoxesCount)

totalBoxesCount = read_total_boxes()

@app.get("/total_boxes")
def get_total_boxes():
    return {"total_boxes": totalBoxesCount}

load_dotenv()
# Replace with your IoT Hub device connection string
CONNECTION_STRING = os.getenv("CONNECTION_STRING")



# configure Swagger
app.title = "Machine Control Monitoring API"
app.description = "API for controlling motors on a Raspberry Pi"
app.version = "0.1.0"
EQUIPMENT_ID = "lauzhack-pi2"
DATASOURCE = "10.0.4.60:8000"

# GPIO Setup
deltaBox = 0
timeProducting = 0
servoPIN = 17
IR_LED = 14
DEBOUNCE_DELAY = 0.01
TRIG_PIN = 23  # GPIO pin connected to the TRIG pin of the sensor
ECHO_PIN = 24  # GPIO pin connected to the ECHO pin of the sensor
KILLSWITCH_THRESHOLD_CM = 8
MARGIN_KILLSWITCH_PREVENT_SECONDS = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.output(TRIG_PIN, False)
GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setup(IR_LED, GPIO.IN)

p = GPIO.PWM(servoPIN, 50)
areMotorsEnabled = False
servoSpeed = 0
real_velocity = 0.0
periodBetweenBoxes = 0.0
theorical_velocity = 0.0
errno_glbl = 0

start_motor_time = 0

ina = INA219(shunt_ohms=0.1,
             max_expected_amps=0.6,
             address=0x40,
             busnum=1)  # Specify the I2C bus number

ina.configure(voltage_range=ina.RANGE_16V,
              gain=ina.GAIN_AUTO,
              bus_adc=ina.ADC_128SAMP,
              shunt_adc=ina.ADC_128SAMP)

# execute once "i'm up!"
@app.on_event("startup")
async def startup_event():  
    # send telemetry of performance
    global WANTS_TO_SEND_TELEMETRY
    if(WANTS_TO_SEND_TELEMETRY == True):
        send_message_to_iot_hub(create_machine_event("startProducing", "BobMachine", 0, 0, 0, datetime.datetime.now(datetime.timezone.utc)))
        
        

def throw_erno_glbl(errn):
    global errno_glbl, timeProducting
    if(errno_glbl != 0): return
    errno_glbl = errn
    if(timeProducting == 0): timeProducting = time.time()
    old = timeProducting
    deltaTime = time.time() - old
    send_message_to_iot_hub(create_machine_event("stopProducing", "BobMachine", deltaBox, totalBoxesCount, deltaTime, datetime.datetime.now(datetime.timezone.utc)))
    deltaBox = 0
    disable_motors()
    logger.error(f"[ERRNO] Error {errn} occured, motors disabled")

def get_distance():
    """Calculate and return the distance measured by the ultrasonic sensor."""
    # Trigger a pulse
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)  # 10 microseconds pulse
    GPIO.output(TRIG_PIN, False)

    # Wait for the echo to start
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    # Wait for the echo to stop
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # Calculate pulse duration
    pulse_duration = pulse_end - pulse_start

    # Calculate distance (speed of sound is 34300 cm/s)
    distance = pulse_duration * 34300 / 2  # Divide by 2 for the round trip

    return round(distance, 2)

def get_voltage():
    return ina.voltage()

def get_current():
    return ina.current() / 1000.0

def get_power():
    return ina.power() / 1000.0


client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

def send_telemetry():
    global client, areMotorsEnabled, servoSpeed, real_velocity, periodBetweenBoxes, totalBoxesCount
    if(WANTS_TO_SEND_TELEMETRY == False): return
    # Create an instance of the IoTHubDeviceClient
    total_working_energy = 0.0  # Simulate total energy consumption

    try:
        while True:
            # Simulate machine speed (1 to 5 boxes per 10 seconds)
            # machine_speed = random.randint(1, 5)
            # 
            
            total_working_energy = get_power() # W
            

            # Create telemetry data with the current UTC timestamp
            telemetry_data = {
                "telemetry": {
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "datasource": DATASOURCE,
                    "machineid": EQUIPMENT_ID,
                    "machinespeed": real_velocity * 1000, # mms
                    "totaloutputunitcount": totalBoxesCount,
                    "totalworkingenergy": total_working_energy
                }
            }

            # Convert the telemetry data to JSON format
            telemetry_json = json.dumps(telemetry_data)

            # Create an IoT Hub Message from the JSON telemetry data
            message = Message(telemetry_json)
            message.content_type = "application/json"
            message.content_encoding = "utf-8"
            message.custom_properties["messageType"] = "Telemetry"

            # Send the message to Azure IoT Hub
            print("Sending message: {}".format(telemetry_json))
            client.send_message(message)
            print("Message successfully sent!")

            # Wait for 10 seconds before sending the next message
            time.sleep(1)
    except Exception as e:
        print("Error sending message: {}".format(e))
    finally:
        # Ensure to close the client after sending
        client.shutdown()


def create_machine_event(event_type, job_id, job_output_count, total_output_count, production_time, timestamp):
    global EQUIPMENT_ID, DATASOURCE
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
    
def send_message_to_iot_hub(event_data):
    global client
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
        client.send_message(machine_event_message)
        logging.info("Message sent successfully!")

    except Exception as e:
        logging.error(f"Failed to send message to IoT Hub: {e}")

# Helper function to normalize values
def normalize_to_duty_cycle(value: float) -> float:
    if value < -5 or value > 5:
        return {'success': False, 'message': 'Value must be between -5 and 5'}
        
    
    neutral_duty = 7.5
    # Mapping the range -5 to 5 such that -5 maps to 2%, 0 to 7.5%, and 5 to 12%
    if value < 0:
        # Scale value from [-5, 0] to [2, 7.5]
        duty_cycle = 2 + (neutral_duty - 2) * (value + 5) / 5
    else:
        # Scale value from [0, 5] to [7.5, 12]
        duty_cycle = neutral_duty + (12 - neutral_duty) * value / 5
    
    return duty_cycle

# @app.get("/read/ir")
def compute_velocity():
    global real_velocity, DEBOUNCE_DELAY, periodBetweenBoxes, totalBoxesCount, errno_glbl, start_motor_time
    lastTime = time.time()
    sspeed = 0
    waiting_for_rise = True
    while True:
        if(errno_glbl != 0): 
            continue
        ir_state = GPIO.input(IR_LED)
        currentTime = time.time()
        delta = currentTime - lastTime
        if waiting_for_rise and ir_state == 1:  # Rising edge detected
            time.sleep(DEBOUNCE_DELAY)  # Wait for debounce delay
            if GPIO.input(IR_LED) == 1:  # Verify signal stability
                waiting_for_rise = False  # Now wait for the falling edge
                # RAISING EDGE
                #Count boxes
                logger.debug("Box detected")
                increment_total_boxes()

                #Calc velocity

                if lastTime != None:
                    periodBetweenBoxes = delta
                    real_velocity = 0.073 / float(delta)
                else:
                    real_velocity = -1

                lastTime = currentTime
        # logger.debug(f"IR state: {ir_state}, waiting_for_rise: {waiting_for_rise}, delta: {delta}")
        if not waiting_for_rise and ir_state == 0:  # Falling edge detected
            waiting_for_rise = True  # Now wait for the next rising edge
            sspeed = abs(servoSpeed)

        #v1 = 13
        #v2 = 9
        #v3 = 6
        #v4 = 4.5
        #v5 = 4.2
        velRef = [1000, 13, 9, 6, 4.5, 4.2]

        if (sspeed > 0.01 and areMotorsEnabled and delta > 1.6*velRef[int(sspeed)]):
            #wait and see 
            deltaSeconds = time.time() - start_motor_time
            if(deltaSeconds < MARGIN_KILLSWITCH_PREVENT_SECONDS):
                pass # false alarm
            else:#too much time has passed, 
                real_velocity = 0
                throw_erno_glbl(2)
        if(sspeed == 0): real_velocity = 0
        
    


# Start the frequency computation in a separate thread
frequency_thread = threading.Thread(target=compute_velocity)
frequency_thread.daemon = True
frequency_thread.start()

iot = threading.Thread(target=send_telemetry)
iot.daemon = True
iot.start()


def check_killswitch():
    global errno_glbl
    while True:
        distance = get_distance()
        if distance < KILLSWITCH_THRESHOLD_CM:
            throw_erno_glbl(1)
            print("Killswitch activated! Motors disabled.")
        time.sleep(0.5)

# Start the killswitch checking in a separate thread
killswitch_thread = threading.Thread(target=check_killswitch)
killswitch_thread.daemon = True
killswitch_thread.start()


@app.get("/motors/enable/")
def enable_motors_default():
    """
    Enable motors with a normalized speed value of 5. (Full forward)
    """
    return enable_motors(5)

@app.get("/motors/rearm")
def rearm():
    """
    Rearm the machine, allowing motors to be enabled.
    """
    global errno_glbl
    if(errno_glbl == 0): return {'success': False, 'message': 'Machine is already armed and ready'}
    errno_glbl = 0
    send_message_to_iot_hub(create_machine_event("startProducing", "BobMachine", 0, 0, 0, datetime.datetime.now(datetime.timezone.utc)))
    return {'success': True, 'message': 'Machine rearmed'}

@app.get("/motors/enable/{value}")
def enable_motors(value: float):
    """
    Enable motors with a normalized speed value.
    -5: Full reverse
    0: Stopped
    5: Full forward
    """
    global p, areMotorsEnabled, servoSpeed, errno_glbl, start_motor_time, timeProducting
    if(errno_glbl != 0): return {'success': False, 'message': f'Machine unarmed! Error {errno_glbl}. Send /motors/rearm to rearm.'}
    if value < -5 or value > 5:
        return {'success': False, 'message': 'Value must be between -5 and 5'}
    if(timeProducting == 0): timeProducting = time.time()
    old = timeProducting
    deltaTime = time.time() - old
    deltaBox = 0
    send_message_to_iot_hub(create_machine_event("newJob", "BobMachine", 0, 0, deltaTime, datetime.datetime.now(datetime.timezone.utc)))
    start_motor_time = time.time()
    servoSpeed = value
    duty_cycle = normalize_to_duty_cycle(value)
    if not areMotorsEnabled:
        areMotorsEnabled = True
        p.start(duty_cycle)
    else:
        p.ChangeDutyCycle(duty_cycle)
    
    return {'success': True, 'message': f'Motors enabled at normalized value {value} (Duty cycle: {duty_cycle})'}


def readNormalizedIR():
    return 1 if GPIO.input(IR_LED) == 0 else 0

@app.get("/motors/disable")
def disable_motors():
    """
    Disable motors and clean up GPIO.
    """
    global p, areMotorsEnabled, servoSpeed, timeProducting
    if areMotorsEnabled:
        areMotorsEnabled = False
        p.stop()
        import atexit
        atexit.register(GPIO.cleanup)
        servoSpeed = 0
        if(timeProducting == 0): timeProducting = time.time()
        old = timeProducting
        deltaTime = time.time() - old
        send_message_to_iot_hub(create_machine_event("stopJob", "BobMachine", totalBoxesCount, totalBoxesCount, deltaTime, datetime.datetime.now(datetime.timezone.utc)))
        return {'success': True, 'message': 'Motors disabled'}
    else:
        return {'success': False, 'message': 'Motors are already disabled'}


# read pin 14 and return its value
@app.get("/read/all")
def read():
    """
    Read the value of all pins and useful variables.
    """
    # prepare the response of all the pins
    response = {
        'IR_LED': readNormalizedIR(),
        'isServoRunning': areMotorsEnabled,
        'normalizedServoSpeed': servoSpeed,
        'realServoDutyCycle': normalize_to_duty_cycle(servoSpeed),
        'realVelocity': real_velocity,
        'errno': errno_glbl,
        'totalBoxesCount': totalBoxesCount,
        'periodBetweenBoxes': periodBetweenBoxes,
        'absoluteServoVelocity': abs(servoSpeed),
        'isForward': "f" if servoSpeed > 0 else "b",
        'voltage': get_voltage(),
        'current': get_current(),
        'power': get_power(),
        'timestamp': (int)(time.time())
    }

    return response

# compute frequency between 1 rising edge and 1 falling edge
@app.get("/velocity")
def get_velocity():
    """
    Get the velocity of the machine in m/s and mm/s respectively.
    """
    return {"velocity": real_velocity, 'velocitymms': real_velocity * 1000}

@app.get("/vitals")
def get_vitals():
    """
    Get the voltage, current, and power consumption of the machine
    """
    return {"voltage": get_voltage(), "current": get_current(), "power": get_power()}

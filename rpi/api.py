import threading
import time
import logging
from fastapi import FastAPI
import RPi.GPIO as GPIO


app = FastAPI()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# configure Swagger
app.title = "Machine Control Monitoring API"
app.description = "API for controlling motors on a Raspberry Pi"
app.version = "0.1.0"


# GPIO Setup
servoPIN = 17
IR_LED = 14
DEBOUNCE_DELAY = 0.01

GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setup(IR_LED, GPIO.IN)

p = GPIO.PWM(servoPIN, 50)
areMotorsEnabled = False
servoSpeed = 0
realvelocity_value = 0.0
periodBetweenBoxes = 0.0
totalBoxesCount = 0


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

def compute_velocity():
    global realvelocity_value, DEBOUNCE_DELAY, periodBetweenBoxes, totalBoxesCount
    while True:
        start, end = None, None
        waiting_for_rise = True  # Start by waiting for a rising edge

        while end is None:  # Keep running until we get two edges
            ir_state = GPIO.input(IR_LED)

            if waiting_for_rise and ir_state == 1:  # Rising edge detected
                time.sleep(DEBOUNCE_DELAY)  # Wait for debounce delay
                if GPIO.input(IR_LED) == 1:  # Verify signal stability
                    if start is None:  # First rising edge
                        start = time.perf_counter()
                        waiting_for_rise = False  # Now wait for the falling edge
                    elif start is not None:  # Second rising edge
                        end = time.perf_counter()

            elif not waiting_for_rise and ir_state == 0:  # Falling edge detected
                time.sleep(DEBOUNCE_DELAY)  # Wait for debounce delay
                if GPIO.input(IR_LED) == 0:  # Verify signal stability
                    waiting_for_rise = True  # Now wait for the next rising edge

        # Calculate velocity
        if start is not None and end is not None:
            duration = end - start
            if duration > 0:  # Ensure valid duration
                realvelocity_value = 0.073 / duration  # m/s
                periodBetweenBoxes = duration
            else:
                realvelocity_value = -1    
        else:
            realvelocity_value = -1    
    
    

# Start the frequency computation in a separate thread
frequency_thread = threading.Thread(target=compute_velocity)
frequency_thread.daemon = True
frequency_thread.start()

# iot = threading.Thread(target=send_telemetry)
# iot.daemon = True
# iot.start()

@app.get("/helloworld")
def helloworld():
    logger.debug("Handling root endpoint request")
    return {"Hello": "World"}

@app.get("/motors/enable/")
def enable_motors_default():
    return enable_motors(5)

@app.get("/motors/enable/{value}")
def enable_motors(value: float):
    """
    Enable motors with a normalized speed value.
    -5: Full reverse
    0: Stopped
    5: Full forward
    """
    global p, areMotorsEnabled, servoSpeed
    if value < -5 or value > 5:
        return {'success': False, 'message': 'Value must be between -5 and 5'}

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
    global p, areMotorsEnabled, servoSpeed
    if areMotorsEnabled:
        areMotorsEnabled = False
        p.stop()
        import atexit
        atexit.register(GPIO.cleanup)
        servoSpeed = 0

        return {'success': True, 'message': 'Motors disabled'}
    else:
        return {'success': False, 'message': 'Motors are already disabled'}

@app.get("/read/")
def readIR():
    return GPIO.input(IR_LED)


# read pin 14 and return its value
@app.get("/read/all")
def read():
    # prepare the response of all the pins
    response = {
        'IR_LED': readNormalizedIR(),
        'isServoRunning': areMotorsEnabled,
        'normalizedServoSpeed': servoSpeed,
        'realServoDutyCycle': normalize_to_duty_cycle(servoSpeed),
        'realVelocity': realvelocity_value,
        'totalBoxesCount': totalBoxesCount,
        'periodBetweenBoxes': periodBetweenBoxes,
        'timestamp': (int)(time.time())
    }

    return response

# compute frequency between 1 rising edge and 1 falling edge
@app.get("/velocity")
def get_velocity():
    return {"velocity": realvelocity_value, 'velocitymms': realvelocity_value * 1000}
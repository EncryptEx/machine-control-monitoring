from fastapi import FastAPI
import RPi.GPIO as GPIO

app = FastAPI()

# GPIO Setup
servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)
areMotorsEnabled = False

# Helper function to normalize values
def normalize_to_duty_cycle(value: float) -> float:
    """
    Normalize a value from -5 to 5 to the appropriate duty cycle range.
    -5 -> minimum reverse duty cycle (e.g., 5.0)
    0  -> stopped (e.g., 7.5)
    5  -> maximum forward duty cycle (e.g., 10.0)
    """
    # Scale -5 to 5 into the PWM duty cycle range (5.0 to 10.0)
    min_duty_cycle = 5.0  # Full reverse
    max_duty_cycle = 10.0  # Full forward
    mid_duty_cycle = 7.5  # Stopped
    
    # Linear mapping of -5 to 5 range to duty cycle range
    return mid_duty_cycle + ((value / 5.0) * (max_duty_cycle - mid_duty_cycle))

@app.get("/helloworld")
def helloworld():
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
    global p, areMotorsEnabled
    if value < -5 or value > 5:
        return {'success': False, 'message': 'Value must be between -5 and 5'}

    duty_cycle = normalize_to_duty_cycle(value)
    if not areMotorsEnabled:
        areMotorsEnabled = True
        p.start(duty_cycle)
    else:
        p.ChangeDutyCycle(duty_cycle)
    
    return {'success': True, 'message': f'Motors enabled at normalized value {value} (Duty cycle: {duty_cycle})'}


@app.get("/motors/disable")
def disable_motors():
    """
    Disable motors and clean up GPIO.
    """
    global p, areMotorsEnabled
    if areMotorsEnabled:
        areMotorsEnabled = False
        p.stop()
        import atexit
        atexit.register(GPIO.cleanup)

        return {'success': True, 'message': 'Motors disabled'}
    else:
        return {'success': False, 'message': 'Motors are already disabled'}

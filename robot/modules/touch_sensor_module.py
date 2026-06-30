# modules/touch_sensor_module.py

import time

try:
    import RPi.GPIO as GPIO
except Exception:
    GPIO = None

SIG_PIN = 17  # BCM pin for sensor (physical pin 33)

# will store the "idle" level read at startup (0 or 1)
_IDLE_LEVEL = 1


def setup_touch_sensor(pin=SIG_PIN):
    """
    Initialize GPIO and auto-calibrate idle level.
    Assume you are NOT touching the sensor during startup.
    """
    global _IDLE_LEVEL

    if GPIO is None:
        print("[Touch] RPi.GPIO not available. Running in stub mode.")
        return

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)
    print(f"[Touch] Initialized on GPIO {pin}")

    # measure idle level a few times (no touch)
    samples = []
    for _ in range(10):
        samples.append(GPIO.input(pin))
        time.sleep(0.02)

    # majority vote: 0 or 1
    _IDLE_LEVEL = int(round(sum(samples) / len(samples)))
    print(f"[Touch] Calibrated idle level = {_IDLE_LEVEL} (0=LOW, 1=HIGH)")


def is_touched(pin=SIG_PIN):
    """
    Returns True if the current pin value differs from the idle level.
    """
    if GPIO is None:
        return False
    val = GPIO.input(pin)
    return val != _IDLE_LEVEL


def cleanup():
    if GPIO is None:
        return
    GPIO.cleanup()
    print("[Touch] GPIO cleaned up")

import RPi.GPIO as GPIO
import time

PIN = 17  # BCM 13 (physical pin 33)

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Touch sensor test running... Touch the sensor! (Ctrl+C to stop)")

try:
    while True:
        if GPIO.input(PIN) == GPIO.HIGH:
            print("TOUCHED")
        else:
            print("not touched")
        time.sleep(0.2)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    print("Clean exit.")

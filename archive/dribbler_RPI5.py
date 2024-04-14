from gpiozero import Servo
from time import sleep

# Define the GPIO pin connected to the servo
servo = Servo(18)

def dribble_on():
    # Move the servo to the position that turns it on
    servo.value = 0.6  # This value is typically around 0.6 for a 50Hz servo PWM

def dribble_off():
    # Move the servo to the position that turns it off
    servo.value = 0.4  # Adjust this value as needed for your specific servo

def main():
    try:
        dribble_on()
        sleep(1)  # Keep the dribble on for 1 second
        dribble_off()
        sleep(1)  # Keep the dribble off for 1 second
    finally:
        # Clean up servo GPIO resources
        servo.close()

if __name__ == '__main__':
    main()


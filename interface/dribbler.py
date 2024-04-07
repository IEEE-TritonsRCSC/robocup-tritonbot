import time
import pigpio
import subprocess

def setup_gpio():
    subprocess.run(["sudo", "pigpiod"])

def dribble_on():
    pi = pigpio.pi()
    pi.set_servo_pulsewidth(18, 1100)

def dribble_off():
    pi = pigpio.pi()
    pi.set_servo_pulsewidth(18, 0)

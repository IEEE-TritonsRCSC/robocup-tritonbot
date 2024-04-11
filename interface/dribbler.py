import time
import pigpio
import subprocess

pi = pigpio.pi()

def setup_gpio():
    subprocess.run(["sudo", "pigpiod"])

def dribble_on(pi):
    pi.set_servo_pulsewidth(18, 1200)

def dribble_off(pi):
    pi.set_servo_pulsewidth(18, 1000)




pi = pigpio.pi()
setup_gpio()
#time.sleep(1)
dribble_on(pi)
time.sleep(5)
dribble_off(pi)

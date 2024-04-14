import os
import time

def setup_dribbler_pwm():
        # enable pwm on gpio pin 18.
        # will say "I/O error" after the first call. not an issue
        os.system("echo 2 > /sys/class/pwm/pwmchip2/export")
        time.sleep(1)
        # set frequency to 50 hz
        os.system("echo 20000000 > /sys/class/pwm/pwmchip2/pwm2/period")
        # start min pulsewidths
        os.system("echo 1000000 > /sys/class/pwm/pwmchip2/pwm2/duty_cycle")
        time.sleep(1)
        # with proper frequency and zero signal, enable PWM
        os.system("echo 1 > /sys/class/pwm/pwmchip2/pwm2/enable")

def dribble_on():
        os.system("echo 1100000 > /sys/class/pwm/pwmchip2/pwm2/duty_cycle")

def dribble_off():
        os.system("echo 1000000 > /sys/class/pwm/pwmchip2/pwm2/duty_cycle")

print("starting")
setup_dribbler_pwm()
time.sleep(1)
print("on")
dribble_on()
time.sleep(1)
print("off")
dribble_off()
time.sleep(1)
print("done")


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
	curr = int(os.popen("cat /sys/class/pwm/pwmchip2/pwm2/duty_cycle").read())
	if curr < 1200000:
		new = curr + 50
		print(f"Increasing dribbler pulsewidth: {new}")
		os.system("echo " + str(new) + " > /sys/class/pwm/pwmchip2/pwm2/duty_cycle")
	else:
		print("Dribbler at pulsewidth: " + str(curr))
		os.system("echo 1200000 > /sys/class/pwm/pwmchip2/pwm2/duty_cycle")

def dribble_off():
	curr = int(os.popen("cat /sys/class/pwm/pwmchip2/pwm2/duty_cycle").read())
	if curr > 1000000:
		new = curr - 50
		print(f"Decreasing dribbler pulsewidth: {new}")
		os.system("echo " + str(new) + " > /sys/class/pwm/pwmchip2/pwm2/duty_cycle")
	else:
		print("Dribbler at min pulsewidth: " + str(curr))
		os.system("echo 1000000 > /sys/class/pwm/pwmchip2/pwm2/duty_cycle")

setup_dribbler_pwm()

for i in range(10000):
    dribble_on()

for i in range(10000):
    dribble_off()
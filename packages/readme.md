Run the following command on a new raspberry pi to setup relevant packages
```bash
sudo apt-get install $(awk '{print $1}' filtered_packages.txt)
```
Next, run
```bash
sudo raspi-config
```
Select `3 Interface Options` from the menu. Then select `I5 Serial Port`.
Select <No> to Disable the serial login shell if it's enabled.
 <Yes> to all the following prompt, <Finish> and select <Yes> when prompted to reboot.

PWM requires kernel 6.6.22 or higher.
```bash
sudo rpi-update
```

A reboot is required afterwards using
```bash
sudo reboot
```

We need to change the boot config file to enable PWM on GPIO 18.
```bash
sudo nano /boot/firmware/config.txt
```

At the BOTTOM of this file, put this on a new line:
```
dtoverlay=pwm-2chan
```

Do not change anything else.

Reboot again with 
```bash
sudo reboot
```

After that, check if PWM has been configured on GPIO 18 with
```bash
pinctrl get 18
```

You should see this
```
tritonbot@node1:~ $ pinctrl get 18
18: a3    pd | lo // GPIO18 = PWM0_CHAN2
```

Controlling PWM with commands
```bash
echo 2 > /sys/class/pwm/pwmchip2/export
echo 20000000 > /sys/class/pwm/pwmchip2/pwm2/period # set frequency 50 hz
echo 1000000 > /sys/class/pwm/pwmchip2/pwm2/duty_cycle # set 1000us pulsewidth
echo 1 > /sys/class/pwm/pwmchip2/pwm2/enable # enable PWM on pin 18. you need to set frequency and dutycycle first
```

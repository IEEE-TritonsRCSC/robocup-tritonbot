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

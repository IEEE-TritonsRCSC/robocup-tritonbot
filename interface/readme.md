The `interface` directory contains modules that facilitate communication between various systems within the TritonBot setup:

- **ai_interface.py**: This module implements UDP multicast for data transmission between the Raspberry Pi and the AI server. It is responsible for establishing a UDP socket to send and receive data efficiently.

- **reg_ai_interface.py**: This file is deprecated and was previously used for regular UDP communication. It likely handled basic UDP socket operations for data exchange but has been superseded by `ai_interface.py` for improved functionality.

- **embedded_systems_interface.py**: This module manages UART (Universal Asynchronous Receiver-Transmitter) communication between the Raspberry Pi and the STM32 embedded system on the robot. It handles sending and receiving data over UART, enabling control and data exchange between these components.

These modules collectively form the communication interface layer of TritonBot, facilitating efficient and reliable data exchange between different components such as the AI server, Raspberry Pi, and embedded systems, specifically the STM32 microcontroller.



# Documentation for `ai_communication.py`

## Overview:
This module facilitates communication with an AI simulation by initializing and utilizing a socket.

## Functions:

### `empty_socket(sock)`
Function to clear input buffer of a socket (AI).

This function continuously clears the input buffer of a socket until there is no more data to receive.

- **Parameters**:
  - `sock`: The socket object to clear the input buffer for.

- **Returns**:
  - None

### `init_socket(address, port)`
Initialize a socket connection with the AI simulation.

This function creates and binds a UDP socket to the specified address and port.

- **Parameters**:
  - `address`: The IP address to bind the socket to.
  - `port`: The port on the IP address to bind the socket to.

- **Returns**:
  - `udp_socket`: The newly created and bound UDP socket.

## Notes:
- This module is designed for communication with an AI simulation via UDP socket.
- Use the provided functions (`init_socket` and `empty_socket`) to establish and manage the socket connection effectively.




# Documentation for `embedded_communication.py`

## Overview:
This module facilitates communication with an embedded system (STM32 on the robot) using UART (Universal Asynchronous Receiver-Transmitter).

This class assumes a baud rate of 115200 and implements a timeout of 0.1 seconds for reading/writing operations. Additionally, it assumes that the header byte of received data is `0x010101` to filter out potential garbage data.

## Functions:

### `sendToEmbedded(message)`
Sends the provided message to the robot's embedded system via UART.

- **Parameters**:
  - `message`: An array of bytes representing the message to be sent to the robot.

- **Returns**:
  - `True`: Indicates successful transmission.

### `readFromEmbedded()`
Receives a message from the robot's embedded system.

- **Returns**:
  - `rx_data.hex()`: Hexadecimal representation of the received message if the header byte matches `0x010101`, otherwise `None`.

### `stopAll()`
Sends a stop message to the robot's embedded system and closes the serial connection.

### `replace_zero_with_one(byte_array)`
Helper function to replace `0x00` bytes in a byte array with `0x01`.

- **Parameters**:
  - `byte_array`: The input byte array.

- **Returns**:
  - `modified_array`: A new byte array with `0x00` replaced by `0x01`.

## Testing Function:

### `test()`
Function to test sending and receiving data from the robot's embedded system.

- **Operation**:
  - Sends a stop message to the robot.
  - Waits for a response from the embedded system.
  - Prints the received response.

## Example Usage:

```python
import embedded_communication

# Define a message to be sent
message = bytes([0x01, 0x0a, 0xbc, 0x02, 0xbc, 0x02, 0xbc, 0x02, 0xbc])

# Send the message to the robot
embedded_communication.sendToEmbedded(message)

# Receive a response from the robot
response = embedded_communication.readFromEmbedded()
if response:
    print(f"Received response: {response}")

# Stop all operations and close the serial connection
embedded_communication.stopAll()
```

## Notes:
- Ensure the correct serial port ('/dev/ttyAMA0') and baud rate (115200) are configured for the serial connection (ser) in the module.
- Use the provided functions (sendToEmbedded, readFromEmbedded, stopAll) to interact with the robot's embedded system effectively.


# Documentation for `dribbler.py`

## Overview:
This module provides functions to control the dribbler on the robot by interfacing with PWM (Pulse Width Modulation) signals via the Linux sysfs interface.

## Functions:

### `setup_dribbler_pwm()`
Initializes the PWM settings for the dribbler control.

- **Description**:
  - Enables PWM on GPIO pin 18 by exporting it (`echo 2 > /sys/class/pwm/pwmchip2/export`).
  - Sets the frequency to 50 Hz (`echo 20000000 > /sys/class/pwm/pwmchip2/pwm2/period`).
  - Starts with a minimum pulse width (`echo 1000000 > /sys/class/pwm/pwmchip2/pwm2/duty_cycle`).
  - Enables PWM by setting the enable flag to `1` (`echo 1 > /sys/class/pwm/pwmchip2/pwm2/enable`).

### `dribble_on()`
Increases the pulse width of the dribbler to turn it on.

- **Operation**:
  - Reads the current pulse width of the dribbler.
  - If the current pulse width is less than `1130000`, increments it by `25` and sets the new pulse width.
  - Prints the updated pulse width.

### `dribble_off()`
Decreases the pulse width of the dribbler to turn it off.

- **Operation**:
  - Reads the current pulse width of the dribbler.
  - If the current pulse width is greater than `1000000`, decrements it by `25` and sets the new pulse width.
  - Prints the updated pulse width.

## Notes:
- Ensure proper GPIO pin (`/sys/class/pwm/pwmchip2/pwm2`) and PWM settings are configured for the dribbler control.
- Use the provided functions (`setup_dribbler_pwm`, `dribble_on`, `dribble_off`) to manage the dribbler operation effectively.

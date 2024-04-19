# Documentation for `velocityConversions.py`

## Purpose:
The `velocityConversions.py` module is designed to process actions received from an external source, typically an AI server, and convert these actions into specific wheel velocities suitable for controlling a robotic system. The primary goal is to interpret desired local velocities (forward, left, and angular) and translate them into individual wheel velocities that can be understood and executed by the robot's motion control system.

## Functionality and Workflow:

### `action_to_byte_array(action)`
- **Description**:
  - This function serves as an entry point for processing actions received from an external source.
  - It utilizes the `getWheelVelocities` function to calculate the desired wheel velocities based on the provided `action`.
  - The resulting wheel velocities are converted into a byte array format using the `valuesToBytes` function, making them suitable for transmission and interpretation by embedded systems.

### `getWheelVelocities(action)`
- **Description**:
  - This function extracts relevant velocity components (`forward`, `left`, and `angular`) from the `action` object.
  - Using these components, it calls `getVelocityArray` to compute the desired wheel velocities.
  - The calculated wheel velocities are returned as an integer array.

### `getVelocityArray(heading, absV, theta, rotV)`
- **Description**:
  - Calculates the desired wheel velocities based on the provided parameters:
    - `heading`: Current heading direction of the robot.
    - `absV`: Absolute translational speed of the robot.
    - `theta`: Desired direction of movement relative to the global field orientation.
    - `rotV`: Desired rotational velocity of the robot.
  - Utilizes trigonometric calculations to determine the appropriate wheel velocities to achieve the desired motion.

### `valuesToBytes(M)`
- **Description**:
  - Converts an array of integer wheel velocities (`M`) into a byte array format suitable for transmission.
  - Each integer value is split into two bytes and appended to the output byte array.

### `hexToRpmArray(headerLength, data)`
- **Description**:
  - Converts a hexadecimal string (`data`) into an array of integer RPM values.
  - The `headerLength` parameter specifies the length of the header within the data, aiding in accurate parsing.
  - Useful for data analysis purposes to interpret received data from embedded systems.

### `rpmArrayToHex(motorSpeed)`
- **Description**:
  - Converts an array of integer RPM values (`motorSpeed`) into a binary string representing hexadecimal values.
  - Each RPM value is split into two bytes and converted accordingly.

## Notes:
- Ensure that the necessary parameters (`heading`, `absV`, `theta`, `rotV`) are correctly provided when calling the functions to achieve accurate and desired wheel velocities.
- This module is integral for translating high-level commands (local velocities) into low-level motion control commands suitable for robotic systems.

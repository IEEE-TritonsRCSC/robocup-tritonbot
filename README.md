```bash
.
├── analytics
│   ├── plotter.py
│   ├── plotTester.py
│   └── saved_graphs
│       ├── 4plotTEST.png
│       ├── help.png
│       ├── test4plot2.png
│       └── test.png
├── archive
│   ├── deprecatedPlotter.py
│   ├── dribbler_RPI5.py
│   ├── tritonbot_022624.py
│   ├── uart_receiver.py
│   └── velocityConversions90.py
├── config.yaml
├── interface
│   ├── ai_interface.py
│   ├── dribbler.py
│   ├── dribbler_RPI4.py
│   ├── embedded_systems_interface.py
│   └── reg_ai_interface.py
├── packages
│   ├── filtered_packages.txt
│   ├── installed_packages.txt
│   ├── python_packages.txt
│   ├── readme.md
│   └── requirements.txt
├── proto
│   ├── messages_robocup_ssl_detection_pb2.py
│   ├── ssl_simulation_robot_control_pb2.py
│   └── triton_bot_communication_pb2.py
├── readme.md
├── README.md
├── remote_controller.py
├── tritonbot_message_processor
│   ├── pid.py
│   └── velocityConversions30.py
└── tritonbot.py

8 directories, 31 files
```

Folder Descriptions

    analytics: Contains a plotter module for visualizing data analytics.
    interface: Includes interfaces for AI and embedded systems communication.
    proto: Protocol buffer files for SSL simulation robot control and Triton Bot communication.
    tritonbot_message_processor: Provides velocity conversion scripts.

Requirements

    Python 3.x
    Protobuf (ensure Protobuf definitions are correctly installed)
    TritonBot message processor
    TritonBot interfaces
    TritonBot analytics module (optional, for data visualization)

To run TritonBot on a Raspberry Pi 4B, make sure to install the required dependencies. Use the following command:

pip install -r requirements.txt

For data analytics:
X11 Forwarding

Run the following on the raspberry pi to install x11:

sudo apt-get update
sudo apt-get install x11-apps

To ssh using X11, run:

ssh -X tritonbot@node1.local

For additional system-level requirements, consider checking the README files in the respective folders. Note: Additional sudo requirements must be installed manually and are not present in requirements.txt
Usage

    Ensure that all required dependencies are installed.
    Set the IP address and port in the script to match the configuration used in the UDP client.
    Run the script using the command: python TritonBot.py [-a]
        The optional -a flag triggers real-time data analytics and visualization.
    Monitor the console for incoming data and robot control actions.

Features

    Listens for UDP data from an AI system, processing and extracting relevant information.
    Parses data using Protobuf and extracts robot local velocity and heading.
    Controls the robot's actions based on received commands, including dribbler and kick actions.
    Optionally provides real-time data analytics and visualization using the -a flag.
    Graphical representation of expected and actual data is displayed and can be saved to a PNG file.

Configuration

    server_address: Set the IP address to bind the UDP socket (use "0.0.0.0" for all available interfaces).
    server_port: Set the port to match the configuration in the UDP client.
    The script expects the TritonBot message processor and interfaces to be correctly configured and available.

Data Analytics (Optional)

To enable real-time data analytics:

ssh using X11:

ssh -X tritonbot@node1.local

Then run:

python TritonBot.py -a

    The script initializes a Plotter object for graphical representation.
    During execution, it updates the plot with expected and actual data.
    Optionally, the user can save the plotted graph to a PNG file upon script termination.



# Overview of `tritonbot.py`

## Imports:
- `sys`, `yaml`: Used for accessing the config file.
- `proto.ssl_simulation_robot_control_pb2`, `proto.triton_bot_communication_pb2`: Local imports of protobuf decompilers for understanding protobuf data received from AI.
- `interface.ai_interface`: Handles setup of a UDP socket to receive data from the AI server.
- `tritonbot_message_processor.velocityConversions30`: Converts raw velocities to a byte format using a specified encoding scheme for communication with embedded systems.
- `interface.dribbler`: Interfaces with and controls the robot's onboard dribbler.
- `analytics.plotter`: Utilized for data analytics.

## Configuration:
1. Extracts network configuration settings (address and port) from `config.yaml`, loading them into local variables `server_address` and `server_port`.
2. Initializes a UDP socket and establishes a connection to the specified address and port via UDP multicast.
3. `received_robot_control = Communication.TritonBotMessage()`: Initializes an instance of the `TritonBotMessage` class from the `Communication` module to handle incoming data in a specific message format defined by the protocol buffer.
4. `setup_dribbler_pwm()`: Instantiates the dribbler for subsequent use in the script.

## Main Feedback Loop:

1. `data, client_address = udp_socket.recvfrom(1024)`: Receives data from the UDP socket.
2. `received_robot_control.ParseFromString(data)`: Decodes the binary data into a `received_robot_control` object.
3. `actions = received_robot_control.command`: Retrieves the `command` field from `received_robot_control`, containing `RobotCommand`s defined in the protobuf file `ssl_simulation_robot_control.proto` on the AI side.
4. `msg = action_to_byte_array(actions)`: Extracts forward/backward and left/right velocities from `actions`, converting them into individual wheel velocities stored in a byte array.
5. Checks if `actions` contains a kick command (`actions.kick_speed`), setting `kick` to `[0x14]` if true or `[0x00]` if false.
6. Controls the dribbler (`dribble_on()` or `dribble_off()`) based on the dribble speed specified in `actions`.
7. Constructs a packet (`msg`) with a predefined header (`header`) and appends the kick command (`kick`).
8. `sendToEmbedded(msg)`: Sends the packet (`msg`) across UART to the embedded systems (Robomaster STM32).

## Real-time Data Analytics (Optional):

- If the `-a` flag is passed in the command-line interface (CLI), additional code executes for real-time data analytics using X11 forwarding.

## Keyboard Interrupt and Termination:

- Upon detecting a `KeyboardInterrupt` (`Ctrl + C`), the script exits the feedback loop and terminates:
  - Turns off the dribbler.
  - If the `-a` flag was passed, prompts the user to save the graph.
- Finally, closes the UDP socket.

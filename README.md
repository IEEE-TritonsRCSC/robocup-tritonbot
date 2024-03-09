# TritonBot.py

This Python script, `TritonBot.py`, serves as the main control program for TritonBot, a robot equipped for soccer play. The script communicates with an AI system, receives control commands, and orchestrates the robot's movements accordingly. Additionally, it provides an option for real-time data visualization.

## File Structure
```
.
├── analytics
│   └── plotter.py
├── archive
│   ├── messages_robocup_ssl_detection_pb2.py
│   ├── remote_controller.py
│   ├── tritonbot_022624.py
│   └── uart_receiver.py
├── config.yaml
├── interface
│   ├── ai_interface.py
│   └── embedded_systems_interface.py
├── proto
│   ├── ssl_simulation_robot_control_pb2.py
│   └── triton_bot_communication_pb2.py
├── readme.md
├── requirements.txt
├── tritonbot_message_processor
│   ├── velocityConversions30.py
│   └── velocityConversions90.py
└── tritonbot.py

6 directories, 15 files
```
### Folder Descriptions

- **analytics:** Contains a plotter module for visualizing data analytics.
- **interface:** Includes interfaces for AI and embedded systems communication.
- **proto:** Protocol buffer files for SSL simulation robot control and Triton Bot communication.
- **tritonbot_message_processor:** Provides velocity conversion scripts.

## Requirements

- Python 3.x
- Protobuf (ensure Protobuf definitions are correctly installed)
- TritonBot message processor
- TritonBot interfaces
- TritonBot analytics module (optional, for data visualization)

To run TritonBot on a Raspberry Pi 4B, make sure to install the required dependencies. Use the following command:

```bash
pip install -r requirements.txt
```

For data analytics:
### **X11 Forwarding**

Run the following on the raspberry pi to install x11:

```bash
sudo apt-get update
sudo apt-get install x11-apps
```

To ssh using X11, run:

```bash
ssh -X tritonbot@node1.local
```

For additional system-level requirements, consider checking the README files in the respective folders.
Note: Additional sudo requirements must be installed manually and are not present in requirements.txt

## Usage

1. Ensure that all required dependencies are installed.
2. Set the IP address and port in the script to match the configuration used in the UDP client.
3. Run the script using the command: `python TritonBot.py [-a]`
   - The optional `-a` flag triggers real-time data analytics and visualization.
4. Monitor the console for incoming data and robot control actions.

## Features

- Listens for UDP data from an AI system, processing and extracting relevant information.
- Parses data using Protobuf and extracts robot local velocity and heading.
- Controls the robot's actions based on received commands, including dribbler and kick actions.
- Optionally provides real-time data analytics and visualization using the `-a` flag.
- Graphical representation of expected and actual data is displayed and can be saved to a PNG file.

## Configuration

- `server_address`: Set the IP address to bind the UDP socket (use "0.0.0.0" for all available interfaces).
- `server_port`: Set the port to match the configuration in the UDP client.
- The script expects the TritonBot message processor and interfaces to be correctly configured and available.

## Data Analytics (Optional)

To enable real-time data analytics:

ssh using X11:

```bash
ssh -X tritonbot@node1.local
```

Then run:

```bash
python TritonBot.py -a
```

- The script initializes a Plotter object for graphical representation.
- During execution, it updates the plot with expected and actual data.
- Optionally, the user can save the plotted graph to a PNG file upon script termination.
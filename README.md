# hscanner - IP Address Scanning Tool

## Description
The ```hscanner``` tool is an IP address scanner designed to help you detect active hosts on a local network and, if necessary, open ports on these hosts. You can customize the scanning parameters to suit your specific needs.

## Installation

To install Hscanner, follow these simple steps:

1. Clone the Hscanner GitHub repository:

    ```bash
    git clone https://github.com/H0ag/hscanner.git
    ```
    
2. Navigate to the project directory:
    ```bash
    cd Hscanner
    ```

3. Install the required dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ``` 

## Basic use
To use ```hscanner```, you need to run the script from the command line. Here's how to use it:

```bash
python hscanner.py [options]
```

## Options
- **```-t```** (*Optional*) : You can specify the timeout in seconds for each IP host. The default timeout is 0.2 seconds.

- **```-p```** (*Optional*): Use this option if you also wish to scan open ports on detected hosts. This function is in beta version.

- **```--ip```** (*Optional*): If you wish to scan specific ports on a given machine, you can supply its IP address using this option. Make sure you use a valid IP address.

## Examples of use
### Scanning hosts on the local network

To scan hosts on your local network with the default timeout (0.2 seconds) :
```bash
python hscanner.py
```

### Scan hosts on the local network with customized timeout
If you wish to adjust the timeout to 1 second :
```bash
python hscanner.py -t 1
```

### Host AND port scanning (Beta)
To scan open hosts and ports :
```bash
python hscanner.py -p
```
### Scanning ports on a specific IP address
If you wish to scan ports open on a specific machine (for example, 192.168.0.100):
```bash
python hscanner.py --ip 192.168.0.100 -p
```

## Dependencies
The "hscanner" script depends on the following Python libraries:

- **```'socket'```** : Used for network operations.
- **```'platform'```** : Used to detect the platform.
- **```'subprocess'```** : To execute system commands.
- **```'termcolor'```** : For colored text formatting.
- **```'netifaces'```** : To obtain information on network interfaces.
- **```'ipaddress'```** : To manipulate IP addresses.
- **```'os'```** : For system operations.

## Notes
- Be sure to install the required libraries on your system before using **hscanner**. 
```bash
pip install -r /PATH/TO/HSCANNER/requirements.txt
``` 
- If pinging doesn't work, you may need to install a ping utility on your system.
```bash
sudo apt-get install -y iputils-ping
```
- The **hscanner** tool is designed for the scanning of local IP addresses. Be sure to use this tool in compliance with local laws and regulations.
- The results of the scan will be displayed in the console, showing the number of hosts or ports tested, the number of them online and offline, and the total execution time.
- This documentation is intended to help you get started with "hscanner". For more detailed information on the inner workings of the script, please refer to the "Code and libraries used" section in the source code.

## Tip
If you are on Linux, you can copy/paste hscanner.py to /usr/local/bin/ or ~/.local/bin/ without the file extention.
And run the "chmod +x" command to make the file executable
```bash
sudo cp PATH/TO/HSCANNER/hscanner.py ~/.local/bin/hscanner && sudo chmod +x ~/.local/bin/hscanner
```
Now you can execute the command "hscanner" to run the script ;)

Have fun using **hscanner** to explore and monitor your local network!

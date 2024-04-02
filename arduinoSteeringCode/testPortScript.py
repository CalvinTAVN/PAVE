import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
currentPorts = ports[:]
print(len(currentPorts))
for port, desc, hwid in sorted(ports):
    print(hwid)
    for i in hwid.split():
        if i.startswith("SER="):
            if i == "SER=e661640843856f28":
                #pico = serial.Serial(port=port, baudrate=9600, timeout=0.1)
                currentPorts.remove(port)
                break
            

arduino1 = serial.Serial(port=currentPorts[0], baudrate=9600, timeout=0.1)
arduino2 = serial.Serial(port=currentPorts[1], baudrate=9600, timeout=0.1)

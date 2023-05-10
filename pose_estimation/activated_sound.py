import serial.tools.list_ports
from playsound import playsound
import glob

def main():
    ports = serial.tools.list_ports.comports()
    serialInst = serial.Serial()

    portList = []

    for onePort in ports:
        portList.append(str(onePort))
        print(onePort)

    val = input("Select Port: COM")

    for x in range(len(portList)):
        if portList[x].startswith("COM" + str(val)):
            portVar = "COM" + str(val)
            print(portList[x])

    serialInst.baudrate = 9600
    serialInst.port = portVar
    serialInst.open()

    while True:
        message = "Authorized access"
        if serialInst.in_waiting:
            packet = serialInst.readline()
            decodedPacket = packet.decode('utf').rstrip('\n')
            
            if message in decodedPacket:
                sound_track(r"C:\Users\ASUS\Academic\MA2012_Intro_to_Mechatronics_Systems_Design\Project\Project\MCU1_master\*.mp3")

def sound_track(path):
    for song in glob.glob(path):
        playsound(song)


if __name__ == "__main__":
    main()


    
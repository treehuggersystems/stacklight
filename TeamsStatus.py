import pystray
from pystray import Menu
from PIL import Image
import os
import time
import serial
import threading
import sys
import serial.tools.list_ports
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QComboBox, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget


previous_state = ""
current_user = os.getlogin()
commStatus = 0
prevComs =''
#find out if TeamsStatus directory has been created, if not, create it and then put a file called "config.txt" with the basic init and this will be where we start from.
current_user = os.getlogin()
directory = os.path.join(os.path.expanduser("~"),'.TeamsStatus')
ports = serial.tools.list_ports.comports()
run=True


def create_config_file():
    global directory
    # check if the directory exists
    if not os.path.exists(directory):
        # create the directory
        os.mkdir(directory)
    else:
        print("directory already exists")
    
    # create the file inside the directory if it does not exist
    filepath = os.path.join(directory, "config.txt")
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            # write to the file
            f.write("COM4\n")
            f.write("Brightness: 100%\n")
            
        # close the file
        f.close()
    else:
        print("File already exists, skipping creation.")

def read_config_file():
    global directory
    filepath = os.path.join(directory, "config.txt")
    # print (filepath)
    # read the contents of the file and return them as a tuple
    with open(filepath, "r") as f:
        contents = f.readlines()
        com_port = contents[0].strip()
        # print(com_port)
        brightness = contents[1].strip()
        # print (brightness)
    return com_port, brightness

def commEstablishConnection():
    global ser,commStatus, COM, prevComs, previous_state
    if commStatus == 0:
        try:
            ser = serial.Serial(COM, 115200, timeout=5)
            commStatus = 1
            prevComs = COM
            previous_state =''
        except serial.SerialException as e:
            print("error opening port:",e)
    elif prevComs != '' and prevComs !=COM:
        commStatus = 0

def comStatus():
    global ser,commStatus ,previous_state
    if commStatus == 1:
        try:
            ser.write(b'Status Is Being Tested')
        except serial.SerialException as e:
            print("error writing to port:",e)
            commStatus = 0
            previous_state =''

def find_current_state():
    filename = 'C:\\Users\\'+current_user+'\\AppData\\Roaming\\Microsoft\\Teams\\logs.txt'
    path = os.path.join(os.getcwd(), filename)
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in reversed(lines):
            if "current state:" in line:
                current_state = line.split("->")[1].split(")")[0].strip()
                return current_state
        return None
 
def states(status):
    global ser,commStatus
    if status =="Available" and commStatus == 1:
        #set to green (1)
        try:
            ser.write(b'1')
            # print("Available")
            return True
        except serial.SerialException as e:
            # print("error writing to port:",e)
            commStatus = 0
    elif (status =="Busy" or status =="DoNotDisturb" or status == "OnThePhone")and commStatus == 1:
        #set to red (2):
        try:
            ser.write(b'2')
            # print("Busy")
            return True
        except serial.SerialException as e:
            # print("error writing to port:",e)
            commStatus = 0    
    elif (status == "Away" or status =="BeRightBack") and commStatus == 1:
        #set to yellow(3):
        try:
            ser.write(b'3')
            # print("Away")
            return True
        except serial.SerialException as e:
            # print("error writing to port:",e)
            commStatus = 0       
    time.sleep(1)

def on_quit_clicked(icon):
    global run
    print("STOPPING THE CODE!")
    icon.stop()
    run=False

def run_icon():
    global icon
    # icon = pystray.Icon("TeamsStatus2", image, "TeamsStatus2")
    icon.run()

def create_menu(icon):
    # menu_item1 = pystray.MenuItem("Run Menu", on_quit_clicked, default=False)
    menu_item1 = pystray.MenuItem("Preferences", preferencesGUI, default=False)
    menu_item2 = pystray.MenuItem("Info", infoGUI, default=False)
    menu_item3 = pystray.MenuItem("Quit", on_quit_clicked, default=False)
    return pystray.Menu(menu_item1, menu_item2, menu_item3)

def infoGUI(icon):
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setFixedSize(QSize(400, 300))
            self.setWindowTitle("Teams Status Indicator Info")

            self.label1 = QLabel()
            self.label1.setText("This software was built to run in the background using a python\nexecutable written by Tyler Moore. The purpose is to indicate the\nstatus of teams on this PC with a 3D printed stacklight.")

            self.label2 = QLabel()
            self.label2.setText("Using the preferences you can select which COM port the 3D printed\nStacklight is connected to.\nIf all else fails....reboot")

            button = QPushButton("OK")
            button.setCheckable(True)
            button.clicked.connect(self.the_button_was)
                
            layout = QVBoxLayout()
            layout.addWidget(self.label1)
            layout.addWidget(self.label2)
            # layout.addWidget(self.label3)
            layout.addWidget(button)

            container = QWidget()
            container.setLayout(layout)

            # Set the central widget of the Window.
            self.setCentralWidget(container)

        def the_button_was(self):
            window.close()

    app = QApplication(sys.argv)

    # Set the window icon
    app.setWindowIcon(QIcon(QPixmap("C:\\pythonP\\stacklight.png")))

    window = MainWindow()
    window.show()
    window.activateWindow()
    app.exec()

def write_config_file(COM,Brightness):
    global directory
    print (directory)  
    if not os.path.exists(directory):
        # create the directory
        os.mkdir(directory)   
    # create the file inside the directory if it does not exist
    filepath = os.path.join(directory, "config.txt")
    with open(filepath, "w+") as f:
        # write to the file
        f.write(f"{COM}\n")
        f.write(f"Brightness: {Brightness}\n")         
    # close the file
    print("Config File Updated.....")
    f.close()
 
def preferencesGUI(icon):
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setFixedSize(QSize(400, 300))
            self.setWindowTitle("Teams Status Indicator Preferences")

            self.label1 = QLabel()
            self.label1.setText('Select COM Path:')

            self.combo1 = QComboBox(self)
            options = [port.device for port in ports]
            # options = ['COM1', 'COM2', 'COM3']
            self.combo1.addItems(options)

            self.label2 = QLabel()
            self.label2.setText('Select Brightness Level:')

            self.combo2 = QComboBox(self)
            options = ['50%', '75%', '100%']
            self.combo2.addItems(options)
        
            button1 = QPushButton("Apply/Save")
            button1.setCheckable(True)
            button1.clicked.connect(self.the_applyButton_was)

            button2 = QPushButton("OK")
            button2.setCheckable(True)
            button2.clicked.connect(self.the_button_was)
                
            layout = QVBoxLayout()
            layout.addWidget(self.label1)
            layout.addWidget(self.combo1)
            layout.addWidget(self.label2)
            layout.addWidget(self.combo2)
            # layout.addWidget(self.label3)
            layout.addWidget(button1)
            layout.addWidget(button2)

            container = QWidget()
            container.setLayout(layout)

            # Set the central widget of the Window.
            self.setCentralWidget(container)

        def the_button_was(self):
            window.close()

        def the_applyButton_was(self):
            button = self.sender()
            if button.text() == 'Apply/Save':
                selected_option1 = self.combo1.currentText()
                selected_option2 = self.combo2.currentText()
                #write to config file
                write_config_file(selected_option1,selected_option2)
                print("COM port selected: "+selected_option1)
                print("Brightness Level Selected: "+selected_option2)
                window.close()

    app = QApplication(sys.argv)

    # Set the window icon
    app.setWindowIcon(QIcon(QPixmap("C:\\pythonP\\stacklight.png")))

    window = MainWindow()
    window.show()
    window.activateWindow()
    app.exec()

#*----------Init of code and program----------*
image = Image.open("C:\\pythonP\\stacklight.png")
icon = pystray.Icon("TeamsStatus2", image, "TeamsStatus2")
icon.menu = create_menu(icon)
icon_thread = threading.Thread(target=run_icon)
icon_thread.start()

#Create a config file if one isn't already installed
create_config_file()
# Gather the settings currently in the config file
COM,Brightness= read_config_file()


while run==True:
    # COM = None
    # Brightness = None
    COM,Brightness= read_config_file()
    # print (directory)
    # print (COM,Brightness)
    # print ("-----------------------------------------------------------")
    commEstablishConnection()
    comStatus()
    current_state = find_current_state()
   
    if current_state != previous_state: #Detects state change after startup
        print(current_state)          
        change_status = states(current_state)
        if change_status:
            previous_state = current_state
    time.sleep(2)


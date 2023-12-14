import json
import os
from tools.tools import pause, stop, print_separator

info_file_path = "./info/info.json"


class Scrcpy:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.path = self.path.replace("<script_path>", os.path.dirname(os.path.abspath(__file__)))

    def connect(self, device):
        os.chdir(self.path)  # locate adb with absolute path

        # set up scrcpy command
        scrcpy_command = self.command
        scrcpy_command = scrcpy_command.replace("<title>", f'"{device.name}"')  # set device name as the window title
        scrcpy_command = scrcpy_command.replace("<id>", device.id)  # set device id for connecting

        if device.video is False:
            scrcpy_command += " --no-video"
        if device.audio is False:
            scrcpy_command += " --no-audio"
        if device.borderless is True:
            scrcpy_command += " --window-borderless"
        if device.fullscreen is True:
            scrcpy_command += " --fullscreen"

        # checking command before executing
        print_separator()
        print(scrcpy_command)
        print_separator()

        if len(input("Press Enter to continue if the command is correct...")) == 0:
            os.system(scrcpy_command)
        else:
            stop()


def read_scrcpy_info():
    with open(info_file_path, "r") as file:
        data = json.load(file)
        scrcpy = Scrcpy(**data["scrcpy"])

    return scrcpy


class Device:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
        if self.connection_type == "WIFI":
            # Use IP instead of serial number to specify devices (Wireless debugging)
            self.id = f"{self.ip_list[self.ip_id]}:{self.port}"    
        elif self.connection_type == "USB":
            # Use serial number to specify devices (USB debugging)
            self.id = f"{self.serial}"

    def print_info(self):
        for attribute, value in self.__dict__.items():
            print(f"{attribute:15} : {'✅' if (value is True) else ('❌' if (value is False) else value)}")

    def connect_adb(self):
        print("Connecting adb...")
        adb.connect(self)

    def activate_scrcpy(self):
        if self.video:
            print("Sharing screen...")
            scrcpy.connect(self)


def read_device_info():
    device_list = []
    with open(info_file_path, "r") as file:
        data = json.load(file)
        for device_info in data["device_list"]:
            device_list.append(Device(**device_info))

    return device_list


class Adb:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.path = self.path.replace("<script_path>", os.path.dirname(os.path.abspath(__file__)))

    def connect(self, device):
        os.chdir(self.path)  # locate adb with absolute path
        adb_connect_command = self.command.replace("<id>", device.id)  # set device id for wireless connecting
        os.system(adb_connect_command)


def read_adb_info():
    with open(info_file_path, "r") as file:
        data = json.load(file)
        adb = Adb(**data["adb"])

    return adb


adb = read_adb_info()
scrcpy = read_scrcpy_info()
device_list = read_device_info()

# print info of all devices with proper formatting
for i, device in enumerate(device_list):
    print_separator(i)
    device.print_info()
print_separator("END")

device_id = int(input("Selected Device ID = "))
print_separator()

if (device_list[device_id].connection_type == "WIFI"):
    device_list[device_id].connect_adb()
    
if (device_list[device_id].video is True) or (device_list[device_id].audio is True):
    device_list[device_id].activate_scrcpy()

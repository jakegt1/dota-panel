#!/usr/bin/env python3

import subprocess;
import re;
import shutil;

from tkinter import Tk, ttk

processList = ["steam", "chrome"]
kill_list = ["steam", "chrome", "dota2"]


def run_steam():
    subprocess.Popen(["steam"])


def run_chrome():
    subprocess.Popen(["mchrome", "tmphome"])


def change_mouse_sensitivity(devices, speed):
    def change_mouse_sensitivity_closure():
        matches = re.findall('id=\d+', devices.get())
        id = re.findall('\d+', matches[0])[0]
        multiplier = speed.getdouble(True)
        multiplier = str(1/float(multiplier))
        if (float(multiplier) > 0.1):
            command = ["xinput", "--set-prop", str(id), 'Device Accel Constant Deceleration', multiplier]
            subprocess.Popen(command)

    return change_mouse_sensitivity_closure


def kill_application(frozen_apps):
    def kill_application_closure():
        app = frozen_apps.get()
        subprocess.Popen(["pkill", "-9", app])

    return kill_application_closure


def create_panel():
    root = Tk()
    frame = ttk.Frame(root, padding=10)
    frame.master.title("Dota Panel")
    frame.grid()
    steam = ttk.Button(frame, text="Run Steam", command=run_steam)
    steam.grid(column=0, row=0)
    chrome = ttk.Button(frame, text="Run Chrome", command=run_chrome)
    chrome.grid(column=1, row=0)

    device_label = ttk.Label(frame, text="Choose your mouse")
    device_label.grid(column=0, row=1)
    devices = ttk.Combobox(frame, values=getXInputList())
    devices.grid(column=0, row=2)
    devices.current(0)
    speed_label = ttk.Label(frame, text="Speed Multiplier")
    speed_label.grid(column=1, row=1)
    speed = ttk.Entry(frame, text="Nice")
    speed.grid(column=1, row=2)
    activate_speed = ttk.Button(frame, text="Change mouse sensitivity", command=change_mouse_sensitivity(devices, speed))
    activate_speed.grid(columnspan=2, row=3)

    frozen_apps = ttk.Combobox(frame, values=kill_list)
    frozen_apps.grid(columnspan=2, row=4)
    frozen_apps.current(0)
    frozen_apps_button = ttk.Button(frame, text="Kill Application", command=kill_application(frozen_apps))
    frozen_apps_button.grid(columnspan=2, row=5)
    return root


def getXInputList():
    fullList = subprocess.check_output(["xinput", "--list", "--short"])
    return [s.strip().decode("utf-8") for s in fullList.splitlines()]


if __name__ == '__main__':
    panel = create_panel()
    try:
        panel.mainloop()
    finally:
        try:
            shutil.rmtree("/var/tmp/tmphome")
        except OSError:
            pass
        subprocess.Popen(["pkill", "gnome-session"])

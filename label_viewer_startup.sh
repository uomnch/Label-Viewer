#! /bin/bash

# Launches the Label-Viewer Python program on startup
# Usage: place in /home/pi and chmod 744
# in /home/pi/.config/lxsession/LDXE-pi/autostart add:
# @/home/pi/label_viewer_startup.sh

cd /home/pi/Desktop/Label-Viewer
python label_viewer.py

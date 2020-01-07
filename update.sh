#!/bin/bash

cd /home/ricardo-velho/Documents/sim_monitor/
python3 single_figure.py
git add --all
git commit -m "$(date)"
git push origin master

# Gamification for kids learning multiplications and divisions

![LearnArithmetics_2025-02-13T16_45_01_561189](https://github.com/user-attachments/assets/f71a128b-4fff-41d9-889e-67eacbf0cfb1)

![LearnArithmetics_2025-02-13T16_45_37_199586](https://github.com/user-attachments/assets/02036de4-cd94-492b-8acb-495048fef863)

# How it works

First 20 random multiplications are provided. The children do not have to type
the answer they shall speak it out loud. Parents shall oversee the process and
check if the result is correct. Hitting **ENTER** brings up the next
assignment. For each assignment the time is measured. After completing the 20
multiplications the worst 20% are selected and the student will have to repeat
them totaling in another 20 multiplications.

The average, maximum and minimum time for the 20 random multiplications is
stored and a trend line is plotted.

# Installation

The program is designed to work on Linux and not tested on any other OS

## Basic Install uv on your system and run main.py from the root of the
repository

## Ansible 

The ansible script is designed for Ubuntu/Gnome based systems.

The ansible script 
- installs uv
- creates a wrapper script that is stored under
~/.local/bin/point_operations_training.sh
- a desktop file under ~/.local/share/applications

<!-- # Requirements tkinter is required for matplot ``` sudo apt install
python3-tk ``` -->


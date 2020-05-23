import signal
import sys
import os

from App import App
import Effects


TEXT_HELP = """
WARNING! Some devices have a bigger connection latency.
This means that fast effects might not work on these devices.


exit - close application
flash - flash all devices in a single color
spectrum - cycle through the Chroma color spectrum
"""


def exit_handler(signal, frame):
    global App
    App.exit()
    sys.exit(0)


# Catch SIGINT to clean up first
signal.signal(signal.SIGINT, exit_handler)

App = App()
App.Flash.apply(3, 0.2, "#00FF00")

# Main menu
command = ""
wrong_command = False
while True:
    # Clear terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Print help
    if (wrong_command):
        App.Flash.apply(1, 1, "#FF0000")
        print(f"Command {command} not found, please try again.")
    print(TEXT_HELP)

    # Command parsing
    command = input("Enter command: ")
    if (command == "exit"):
        wrong_command = False
        App.exit()
        break
    elif (command == "spectrum"):
        App.Gradient.spectrum()
        wrong_command = False
    elif (command == "flash"):
        n = input("Flash how many times? ")
        delay = input("Delay between flashes? (in seconds, 0.1 for 100ms) ")
        color = input("What color? (in hexadecimal format \"#RRGGBB\") ")
        App.Flash.apply(int(n), float(delay), color)
        wrong_command = False
    else:
        wrong_command = True

import signal
import sys
import os

from App import App
import Effects


TEXT_HELP = """
WARNING! "smooth" tag means some devices might have laggy color effects.

stop - halt all effects
static - set all devices to a single color
flash - flash all devices in a 2 colors
fade - fade from one color to another
exit - close application
"""


def exit_handler(signal, frame):
    global App
    App.exit()
    sys.exit(0)


# Catch SIGINT to clean up first
signal.signal(signal.SIGINT, exit_handler)

App = App()
App.Static.apply("#ffffff", cl=False, kb=False, ms=False)
App.Flash.apply(2, 0.15, "#00ff00", "#004400", smooth=True)
App.Gradient.apply(1, "#00ff00", "#ffffff", smooth=True)

# Main menu
command = ""
wrong_command = False

while True:
    # Clear terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Print help
    print(TEXT_HELP)

    # Notify wrong command
    if (wrong_command):
        App.Gradient.apply(1, "#ff0000", "#ffffff", smooth=True)
        print(f"Command {command} not found, please try again.")

    # Command parsing
    command = input("Enter command: ")

    if (command == "stop"):
        App.Gradient.running = False
        App.Gradient.thread.join()
        App.Static.apply("#ffffff", cl=False, kb=False, ms=False)
        App.Gradient.apply(1, "#00ff00", "#ffffff", smooth=True)
        wrong_command = False
        continue

    elif (App.Gradient.running):
        print("Running effects detected!")
        finish = input("Wait for all effects to finish? (y/n) ")
        # TODO Create interrupt keyboard event
        if (finish == "y"):
            continue
        else:
            App.Gradient.running = False
            App.Gradient.thread.join()
            App.Static.apply("#ffffff", cl=False, kb=False, ms=False)
            App.Gradient.apply(1, "#00ff00", "#ffffff", smooth=True)

    # TODO proper menu
    if (command == "exit"):
        wrong_command = False
        App.exit()
        break

    elif (command == "static"):
        color = input(
            "What color? (in hexadecimal format \"#RRGGBB\") ")
        App.Static.apply(color)

    elif (command == "flash"):
        n = input("Flash how many times? ")
        delay = input(
            "Delay between flashes? (in seconds, 0.1 for 100ms) ")
        color1 = input(
            "Brighter color code? (in hexadecimal format \"#RRGGBB\") "
        )
        color2 = input(
            "Darker color code? (in hexadecimal format \"#RRGGBB\") "
        )
        smooth = input("Smooth? (y/n) ")
        App.Flash.apply(int(n), float(delay), color1, color2,
                        smooth=(True if smooth == "y" else False)
                        )
        wrong_command = False

    elif (command == "fade"):
        time = input(
            "How long? (in seconds, 0.1 for 100ms) ")
        color1 = input(
            "Colorcode to fade from? (in hexadecimal format \"#RRGGBB\") "
        )
        color2 = input(
            "Color code to fade to? (in hexadecimal format \"#RRGGBB\") "
        )
        smooth = input("Smooth? (y/n) ")
        App.Gradient.apply(int(time), color1, color2, smooth=(
            True if smooth == 'y' else False))
        wrong_command = False

    else:
        wrong_command = True

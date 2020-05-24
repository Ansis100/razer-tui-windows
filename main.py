import signal
import sys
import os

from App import App
import Effects

TEXT_WELCOME = """                                      
  _ __  _   _ ___  ___ _ __ ___   
 | '_ \\| | | / __|/ _ \\ '_ ` _ \\  
 | |_) | |_| \\__ \\  __/ | | | | | 
 | .__/ \\__, |___/\\___|_| |_| |_| 
 | |     __/ |    _           _   
 |_|    |___/    (_)         | |  
  ____  _ __ ___  _  ___  ___| |_ 
 | '_ \\| '__/ _ \\| |/ _ \\/ __| __|
 | |_) | | | (_) | |  __/ (__| |_ 
 | .__/|_|  \\___/| |\\___|\\___|\\__|
 | |            _/ |              
 |_|           |__/               
 
 """
TEXT_HELP = """Smooth flag enables more fancy effects, such as smoother gradient fades and faster flashes.
Toggle this on to disable lower-latency devices (such as headsets, speakers) from receiving effects."""
commands = [
    ("stop", "stop", "halt all effects"),
    ("toggle", "toggle smooth tag"),
    ("static", "set all devices to a single color"),
    ("flash", "flash all devices in a 2 colors"),
    ("fade", "fade from one color to another"),
    ("exit", "close application"),
    ("rainbow", "cycle through the colors of the rainbow")
]
smooth = False


def exit_handler(signal, frame):
    global App
    App.exit()
    sys.exit(0)


# Catch SIGINT to clean up first
signal.signal(signal.SIGINT, exit_handler)

App = App()

# Main menu
command = ""
wrong_command = False

while True:
    # Clear terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Print menu
    print(TEXT_WELCOME)
    print(TEXT_HELP)
    print(f"\nSmooth flag (disable slow devices) - {smooth}\n")
    for i in range(len(commands)):
        print("{0} - {1}".format(commands[i][0], commands[i][1]))

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
            print("Halting effects...")
            App.Gradient.running = False
            App.Gradient.thread.join()
            App.Static.apply("#ffffff", cl=False, kb=False, ms=False)
            App.Gradient.apply(1, "#00ff00", "#ffffff", smooth=True)

    if (command == "exit"):
        wrong_command = False
        App.exit()
        break

    elif (command == "toggle"):
        smooth = not smooth

    elif (command == "static"):
        color = input(
            "What color? (in hexadecimal format \"#RRGGBB\") ")
        App.Static.apply(color)
        wrong_command = False

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
        App.Flash.apply(int(n), float(delay), color1, color2, smooth=smooth)
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
        App.Gradient.apply(int(time), color1, color2, smooth=smooth)
        wrong_command = False

    elif (command == "rainbow"):
        App.Rainbow.apply(smooth=smooth)
        wrong_command = False

    else:
        wrong_command = True

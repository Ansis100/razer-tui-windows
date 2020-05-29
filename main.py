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
    ("stop", "halt all effects/reset to white"),
    ("toggle", "toggle smooth tag"),
    ("static", "set all devices to a single color"),
    ("flash", "flash all devices in a 2 colors"),
    ("fade", "fade from one color to another"),
    ("exit", "close application"),
    ("rainbow", "cycle through the colors of the rainbow"),
    ("weather", "display the current weather condition (WeatherAPI)"),
]
smooth = False


def exit_handler(signal, frame):
    print("Halting all effects...")
    global App
    if (App.Gradient.running):
        App.Gradient.running = False
        App.Gradient.thread.join()
    if(App.Rainbow.running):
        App.Rainbow.running = False
        App.Rainbow.thread.join()
    if(App.Weather.running):
        App.Weather.running = False
        App.Weather.thread.join()
    App.exit()
    sys.exit(0)


# Catch SIGINT to clean up first
signal.signal(signal.SIGINT, exit_handler)

App = App()

# Notify connect
App.Flash.apply(2, 0.6, "#00ff00", "#ffffff")
App.Gradient.apply(2, "#00ff00", "#ffffff")

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
        App.Flash.apply(3, 0.10, "#ff0000", "#000000", smooth=True)
        App.Static.apply("#ffffff")
        print(f"Command {command} not found, please try again.")

    # Command parsing
    command = input("Enter command: ")

    if (command == "stop"):
        print("Halting all effects...")
        if (App.Gradient.running):
            App.Gradient.running = False
            App.Gradient.thread.join()
        elif(App.Rainbow.running):
            App.Rainbow.running = False
            App.Rainbow.thread.join()
        elif(App.Weather.running):
            App.Weather.running = False
            App.Weather.thread.join()
        App.Gradient.apply(1, "#00ff00", "#ffffff")

        wrong_command = False
        continue

    elif (App.Gradient.running or App.Rainbow.running or App.Weather.running):
        print("Running effects detected!")
        finish = input("Wait for all effects to finish? (y/n) ")
        # TODO Create interrupt keyboard event
        if (finish == "y"):
            continue
        else:
            print("Halting all effects...")
            if (App.Gradient.running):
                App.Gradient.running = False
                App.Gradient.thread.join()
            if(App.Rainbow.running):
                App.Rainbow.running = False
                App.Rainbow.thread.join()
            if(App.Weather.running):
                App.Weather.running = False
                App.Weather.thread.join()
            print("Done!")

    if (command == "exit"):
        wrong_command = False
        App.exit()
        break

    elif (command == "toggle"):
        if (smooth):
            App.Flash.apply(1, 0.6, "#000000", "#ffffff")
            smooth = False
        else:
            App.Static.apply("#000000")
            App.Flash.apply(1, 0.6, "#000000", "#ffffff", smooth=True)
            smooth = True

        wrong_command = False

    elif (command == "static"):
        color = input(
            "What color? (in hexadecimal format \"#RRGGBB\") ")
        App.Static.apply(color)
        wrong_command = False

    elif (command == "flash"):
        n = input("Flash how many times? ")
        delay = input(
            "Delay between flashes? (in seconds, 0.1 for 100ms) ")
        brighter = input(
            "Brighter color code? (in hexadecimal format \"#RRGGBB\") "
        )
        darker = input(
            "Darker color code? (in hexadecimal format \"#RRGGBB\") "
        )
        App.Flash.apply(int(n), float(delay), darker, brighter, smooth=smooth)
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

    elif (command == "weather"):
        city = input("What city are you in? ")
        App.Weather.apply(city, smooth=smooth)

    else:
        wrong_command = True

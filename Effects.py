import requests
import App
from time import sleep
from threading import Thread


class Static:
    def __init__(self, uri):
        self.uri = uri

    def hex_to_bgr(self, hex):
        return int(hex[5:] + hex[3:5] + hex[1:3], 16)

    def apply(self, color, hs=True, cl=True, kb=True, ms=True):
        data = {
            "effect": "CHROMA_STATIC",
            "param": {
                "color": self.hex_to_bgr(color)
            }
        }

        if (hs):
            requests.put(url=self.uri + "/headset", json=data)
        if (kb):
            requests.put(url=self.uri + "/keyboard", json=data)
        if (ms):
            requests.put(url=self.uri + "/mouse", json=data)
        if (cl):
            requests.put(url=self.uri + "/chromalink", json=data)


class Gradient:
    def __init__(self, uri):
        self.uri = uri
        self.running = False
        self.Static = Static(uri)

    def calculate_gradient_step(self, color_tuple1, color_tuple2, t):
        r = str(hex(int(
            color_tuple1[0]
            + (color_tuple2[0] - color_tuple1[0])
            * t
        )))[2:]

        g = str(hex(int(
            color_tuple1[1]
            + (color_tuple2[1] - color_tuple1[1])
            * t
        )))[2:]

        b = str(hex(int(
            color_tuple1[2]
            + (color_tuple2[2] - color_tuple1[2])
            * t
        )))[2:]

        if (len(r) == 1):
            r = '0' + r
        if (len(g) == 1):
            g = '0' + g
        if (len(b) == 1):
            b = '0' + b

        return '#' + r + g + b

    def apply(self, time, color1, color2, smooth=False):
        """Send a gradient from color1 to color2 with a length of time.

        Arguments:
            time {float} -- Gradient length in seconds
            color1 {str} -- Color in the format "#FFFFFF" (hex)
            color2 {str} -- Color in the format "#FFFFFF" (hex)

        Keyword Arguments:
            smooth {bool} -- Smooth flag, disables headsets which allows for faster effects (default: {False})
        """

        color_tuple1 = (
            int(color1[1:3], 16),
            int(color1[3:5], 16),
            int(color1[5:], 16)
        )
        color_tuple2 = (
            int(color2[1:3], 16),
            int(color2[3:5], 16),
            int(color2[5:], 16)
        )

        # Create an array of gradient hex codes
        gradient = []
        steps = time * (30 if smooth else 10)
        for i in range(steps):
            # Gradient code calculation
            gradient.append(
                self.calculate_gradient_step(
                    color_tuple1,
                    color_tuple2,
                    i/steps
                )
            )
        gradient.append(color2)

        self.running = True
        self.thread = Thread(target=self.thread_send_gradient,
                             args=("thread_keep_alive", gradient, smooth, time, steps))
        self.thread.start()

    def thread_send_gradient(self, thread_name, gradient, smooth, time, steps):
        for i in range(len(gradient)):
            if (self.running):
                self.Static.apply(gradient[i], hs=(False if smooth else True))
                sleep(time/steps)
            else:
                print("Halting effect...")
                return
        self.running = False

    def spectrum(self):
        """Cycle through the whole rainbow spectrum
        """
        self.apply("#ff0000", "#00ff00", 2)
        # for i in range(len(rainbow)):
        #     send_static(hex_to_bgr(rainbow[i]))
        #     sleep(0.1)


class Flash:

    def __init__(self, uri):
        self.uri = uri
        self.Static = Static(uri)

    def apply(self, n, delay, color1, color2, smooth=False):
        """Flash color n times.

        Arguments:
            n {int} -- How many times should the color appear
            delay {float} -- Delay between flashes in seconds
            color {str} -- Flash color in the format "#FFFFFF" (hex)

        Keyword Arguments:
            smooth {bool} -- Smooth flag, disables headsets which allows for faster effects (default: {False})
        """
        for i in range(n):
            self.Static.apply(color1, hs=(False if smooth else True))
            sleep(delay/2)
            self.Static.apply(color2, hs=(False if smooth else True))
            sleep(delay/2)

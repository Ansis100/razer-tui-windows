import requests
import App
from time import sleep


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
        self.Static = Static(uri)

    def calculate_gradient_step(self, color_tuple1, color_tuple2, t):
        r = str(hex(int(
            color_tuple1[0]
            + (color_tuple2[0] - color_tuple1[0])
            * t
        )))[2:]

        g = str(hex(int(
            (color_tuple2[1] - color_tuple1[1])
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

    def apply(self, color1, color2, time):
        """Send a gradient from color1 to color2 with a length of time.

        Arguments:
            color1 {str} -- Color in the format "#FFFFFF" (hex)
            color2 {str} -- Color in the format "#FFFFFF" (hex)
            time {float} -- Gradient length in seconds
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
        steps = time * 10
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

        for i in range(len(gradient)):
            self.Static.apply(gradient[i])
            sleep(time/steps)

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

    def apply(self, n, delay, color):
        """Flash color n times.

        Arguments:
            n {int} -- How many times should the color appear
            delay {float} -- Delay between flashes in seconds
            color {str} -- Flash color in the format "#FFFFFF" (hex)
        """
        for i in range(n):
            self.Static.apply(color)
            sleep(delay/2)
            self.Static.apply("#000000")
            sleep(delay/2)

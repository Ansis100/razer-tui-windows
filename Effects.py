import requests
import App
import datetime
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

    def apply(self, time, color1, color2, smooth=False, thread=True):
        """Send a gradient from color1 to color2 with a length of time.

        Arguments:
            time {float} -- Gradient length in seconds
            color1 {str} -- Color in the format "#FFFFFF" (hex)
            color2 {str} -- Color in the format "#FFFFFF" (hex)

        Keyword Arguments:
            smooth {bool} -- Smooth flag, disables headsets which allows for faster effects (default: {False})
            thread {bool} -- Thread flag, runs the effect on a separate thread, set to False if calling from another effect thread (default: {True})
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
        if (thread):
            self.thread = Thread(target=self.effect_thread,
                                 args=("thread", gradient, smooth, time, steps))
            self.thread.start()
        else:
            self.effect_thread("thread", gradient, smooth, time, steps)

    def effect_thread(self, thread_name, gradient, smooth, time, steps):
        for i in range(len(gradient)):
            if (self.running):
                self.Static.apply(gradient[i], hs=(False if smooth else True))
                sleep(time/steps)
            else:
                break
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
        for _ in range(n):
            self.Static.apply(color1, hs=(False if smooth else True))
            sleep(delay/2)
            self.Static.apply(color2, hs=(False if smooth else True))
            sleep(delay/2)


class Rainbow:

    def __init__(self, uri):
        self.uri = uri
        self.running = False
        self.Gradient = Gradient(uri)

    def apply(self, smooth=False):
        codes = [
            "#FF0000",
            "#FF7F00",
            "#FFFF00",
            "#00FF00",
            "#0000FF",
            "#4B0082",
            "#9400D3",
            "#FF0000"
        ]

        self.running = True
        self.thread = Thread(target=self.effect_thread,
                             args=("thread", codes, smooth))
        self.thread.start()

    def effect_thread(self, thread_name, codes, smooth):
        for i in range(len(codes) - 1):
            if(self.running):
                self.Gradient.apply(
                    2, codes[i], codes[i+1], smooth=smooth, thread=False)
            else:
                break
        self.running = False


class Weather:

    def __init__(self, uri):
        self.uri = uri
        self.running = False
        self.Gradient = Gradient(uri)

    def apply(self, city, smooth=False):

        r = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key=77bec6452ff6453f98a94016202705&q={city}"
        )

        if (r.status_code == 400):
            return False

        r = r.json()

        self.running = True
        self.thread = Thread(target=self.effect_thread,
                             args=("thread", city, smooth))
        self.thread.start()

        return True

    # TEMP
    # def test(self, code, smooth=False):
    #     conditions = {
    #         "01d": ["#ffff00", "#ffff00", 2],  # Clear
    #         "02d": ["#ffff00", "#ffff33", 4],  # Few Clouds
    #         "03d": ["#ffff33", "#ffffaa", 4],    # Scattered Clouds
    #         "04d": ["#ffffaa", "#333333", 4],    # Broken Clouds
    #         "09d": ["#ffffff", "#66bbff", 2],    # Shower Rain
    #         "10d": ["#003333", "#0000ff", 2],    # Rain
    #         "11d": ["#ffffff", "#0000ff", 2],    # Thunderstorm
    #         "13d": ["#ffffff", "#000000", 2],    # Snow
    #         "50d": ["#222222", "#222222", 2],    # Mist
    #     }

    #     self.running = True
    #     self.thread = Thread(target=self.effect_thread,
    #                          args=("thread", smooth))
    #     self.thread.start()
    # # /TEMP

    def effect_thread(self, thread_name, city, smooth):
        conditions = {
            1000: ["#ffff00", "#ffff00", 2],  # Clear
            1003: ["#ffff00", "#ffff33", 4],  # Few Clouds
            1006: ["#ffff33", "#ffffaa", 4],  # Scattered Clouds
            1009: ["#ffffaa", "#333333", 4],  # Broken Clouds

            1030: ["#222222", "#222222", 2],  # Mist
            1135: ["#222222", "#222222", 2],
            1147: ["#222222", "#222222", 2],

            1150: ["#ffffff", "#66bbff", 2],  # Light Rain
            1153: ["#ffffff", "#66bbff", 2],
            1063: ["#ffffff", "#66bbff", 2],
            1168: ["#ffffff", "#66bbff", 2],
            1180: ["#ffffff", "#66bbff", 2],
            1183: ["#ffffff", "#66bbff", 2],
            1198: ["#ffffff", "#66bbff", 2],

            1186: ["#003333", "#0000ff", 2],  # Rain
            1171: ["#003333", "#0000ff", 2],
            1189: ["#003333", "#0000ff", 2],
            1192: ["#003333", "#0000ff", 2],
            1195: ["#003333", "#0000ff", 2],
            1201: ["#003333", "#0000ff", 2],
            1240: ["#003333", "#0000ff", 2],
            1243: ["#003333", "#0000ff", 2],
            1246: ["#003333", "#0000ff", 2],

            1087: ["#ffffff", "#0000ff", 2],  # Thunderstorm
            1273: ["#ffffff", "#0000ff", 2],
            1276: ["#ffffff", "#0000ff", 2],
            1279: ["#ffffff", "#0000ff", 2],
            1282: ["#ffffff", "#0000ff", 2],

            1066: ["#ffffff", "#000000", 2],  # Snow
            1069: ["#ffffff", "#000000", 2],
            1072: ["#ffffff", "#000000", 2],
            1114: ["#ffffff", "#000000", 2],
            1117: ["#ffffff", "#000000", 2],
            1204: ["#ffffff", "#000000", 2],
            1207: ["#ffffff", "#000000", 2],
            1210: ["#ffffff", "#000000", 2],
            1213: ["#ffffff", "#000000", 2],
            1216: ["#ffffff", "#000000", 2],
            1219: ["#ffffff", "#000000", 2],
            1222: ["#ffffff", "#000000", 2],
            1225: ["#ffffff", "#000000", 2],
            1237: ["#ffffff", "#000000", 2],
            1249: ["#ffffff", "#000000", 2],
            1252: ["#ffffff", "#000000", 2],
            1255: ["#ffffff", "#000000", 2],
            1258: ["#ffffff", "#000000", 2],
            1261: ["#ffffff", "#000000", 2],
            1264: ["#ffffff", "#000000", 2],
        }

        r = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key=77bec6452ff6453f98a94016202705&q={city}"
        ).json()
        codes = conditions[r["current"]["condition"]["code"]]

        while True:
            # Fetch new data every hour
            if (((datetime.datetime.now().minute == 0) or (datetime.datetime.now().minute == 30)) and (0 <= datetime.datetime.now().second <= 10)):
                r = requests.get(
                    f"http://api.weatherapi.com/v1/current.json?key=77bec6452ff6453f98a94016202705&q={city}"
                ).json()
                codes = conditions[r["current"]["condition"]["code"]]

            if (self.running):
                self.Gradient.apply(
                    codes[2], codes[0], codes[1], smooth=smooth, thread=False)
            if (self.running):
                self.Gradient.apply(
                    codes[2], codes[1], codes[0], smooth=smooth, thread=False)
            else:
                break
        self.running = False

import requests
from time import sleep
from threading import Thread
import Effects


class App:

    keep_alive = True
    uri = ""

    developer_name = 'Ansis Spruģevics'
    developer_contact = 'ansis100@gmail.com'
    category = 'application'
    supported_devices = ['keyboard', 'mouse', 'chromalink', 'headset']
    description = 'Sāk jau reāli besīt.'
    title = 'Kāpēc Šitas Nestrādā'

    def __init__(self):
        # TODO:
        # errors

        # Set up app info

        # Init Connection
        url = "http://localhost:54235/razer/chromasdk"
        data = {
            "title": self.title,
            "description": self.description,
            "author": {
                "name": self.developer_name,
                "contact": self.developer_contact
            },
            "device_supported": self.supported_devices,
            "category": self.category
        }

        # Attempt to connect
        print("Connecting to Razer Chroma REST API...")
        response = requests.post(url=url, json=data)
        self.uri = response.json()['uri']

        # Wait for Chroma API to detect connection
        sleep(2)

        # Start maintaining connection
        self.tkeepalive = Thread(target=self.thread_keep_alive,
                                 args=("thread_keep_alive", self.uri))
        self.tkeepalive.start()

        # Set up effects
        self.Static = Effects.Static(self.uri)
        self.Flash = Effects.Flash(self.uri)
        self.Gradient = Effects.Gradient(self.uri)
        self.Static = Effects.Static(self.uri)
        self.Rainbow = Effects.Rainbow(self.uri)

    def exit(self):
        self.keep_alive = False
        self.tkeepalive.join()
        print('\nClosing connection...')
        # Close connection
        requests.delete(url=self.uri)
        print("Goodbye!")

    def thread_keep_alive(self, thread_name, URI):
        # Send keepalives
        while True:
            requests.put(url=self.uri + "/heartbeat")
            sleep(1)

            if (not self.keep_alive):
                return

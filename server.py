import logging
import pickle
from socketserver import BaseRequestHandler, TCPServer

from pynput.mouse import Controller

from mouse_event import ClickState, MouseEvent

HOST, PORT = "localhost", 9999


class MyTCPHandler(BaseRequestHandler):
    data: bytes

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mouse = Controller()

    def handle(self):
        self.request.settimeout(60)
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                if not self.data:
                    return
                serialized_obj = self.data
                event: MouseEvent = pickle.loads(serialized_obj)
                self.mouse.position = event.position
                if event.clicked_button and event.click_state:
                    if event.click_state == ClickState.PRESSED:
                        self.mouse.press(event.clicked_button)
                    elif event.click_state == ClickState.RELEASED:
                        self.mouse.release(event.clicked_button)
                if event.scroll_delta:
                    self.mouse.scroll(event.scroll_delta)
                self.request.sendall(bytes("OK", "utf-8"))
            except TimeoutError:
                logging.error("Timeout, closing connection with %s", self.client_address[0])
                return


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Create the server, binding to localhost on port 9999
    with TCPServer((HOST, PORT), MyTCPHandler) as server:
        logging.info("Server is running")
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

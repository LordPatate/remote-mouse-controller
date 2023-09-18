import logging
import pickle
from socketserver import BaseRequestHandler, TCPServer

from pynput.mouse import Controller

from mouse_event import ClickState, MouseEvent

HOST, PORT = "0.0.0.0", 9999


class MyTCPHandler(BaseRequestHandler):
    data: bytes

    def handle(self):
        logging.info(f"Connected to {self.client_address[0]}")
        mouse = Controller()
        self.request.settimeout(60)
        while True:
            try:
                self.data = self.request.recv(1024).strip()
            except TimeoutError:
                logging.error("Timeout, closing connection with %s", self.client_address[0])
                return
            if not self.data:
                logging.info(f"Disconnected from {self.client_address[0]}")
                return
            serialized_obj = self.data
            event: MouseEvent = pickle.loads(serialized_obj)
            mouse.position = event.position
            if event.clicked_button and event.click_state:
                if event.click_state == ClickState.PRESSED:
                    mouse.press(event.clicked_button)
                elif event.click_state == ClickState.RELEASED:
                    mouse.release(event.clicked_button)
            if event.scroll_delta:
                mouse.scroll(event.scroll_delta)
            self.request.sendall(bytes("OK", "utf-8"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Create the server, binding to localhost on port 9999
    with TCPServer((HOST, PORT), MyTCPHandler) as server:
        logging.info("Server is running")
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

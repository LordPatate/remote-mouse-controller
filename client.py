import pickle
import socket
from argparse import ArgumentParser
from queue import Queue

from pynput import mouse

from mouse_event import ClickState, MouseEvent
from server import PORT

DELAY = 1 / 120


class MouseMonitor:
    def __init__(self):
        self._event_queue = Queue()
        self._listener = mouse.Listener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll,
        )
        self._listener.start()

    def poll(self):
        return self._event_queue.get()

    def _on_move(self, x, y):
        event = MouseEvent(position=(x, y))
        self._event_queue.put(event)

    def _on_click(self, x, y, button, pressed):
        event = MouseEvent(
            position=(x, y),
            clicked_button=button,
            click_state=ClickState.PRESSED if pressed else ClickState.RELEASED
        )
        self._event_queue.put(event)

    def _on_scroll(self, x, y, dx, dy):
        event = MouseEvent(
            position=(x, y),
            scroll_delta=(dx, dy),
        )
        self._event_queue.put(event)

    def close(self):
        self._listener.stop()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()


def main(server_ip: str):
    monitor = MouseMonitor()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # SOCK_STREAM means a TCP socket
        print(f"Trying to connect to {server_ip}:{PORT}")
        sock.connect((server_ip, PORT))
        print("Connected to server")
        while True:
            event = monitor.poll()
            data = pickle.dumps(event)
            try:
                sock.sendall(data)
                _ = sock.recv(256)
            except (ConnectionAbortedError, ConnectionResetError):
                print("Connection closed by server")
                break
        print("Shutting down.")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "server_ip",
        nargs="?",
        default="localhost",
        type=str,
    )
    args = parser.parse_args()
    main(args.server_ip)

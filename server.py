import logging
from socketserver import BaseRequestHandler, TCPServer

HOST, PORT = "localhost", 9999


class MyTCPHandler(BaseRequestHandler):
    data: bytes

    def handle(self):
        self.request.settimeout(60)
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                if not self.data:
                    return
                message = str(self.data, 'utf-8')
                logging.info("%s wrote: %s", self.client_address[0], message)
                answer = f"Your message '{message}' was well received"
                self.request.sendall(bytes(answer, "utf-8"))
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

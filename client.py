import socket

HOST, PORT = "localhost", 9999

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server
    sock.connect((HOST, PORT))
    while True:
        try:
            data = input("> ")
        except EOFError:
            break
        sock.sendall(bytes(data + "\n", "utf-8"))
        try:
            received = str(sock.recv(1024), "utf-8")
        except (ConnectionAbortedError, ConnectionResetError):
            print("Connection closed by server")
            break
        print(received)
    print("Shutting down.")

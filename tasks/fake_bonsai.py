# fake bonsai
from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher


def default_handler(address, *args):
    print(f"BONSAI {address}: {args}")


dispatcher = Dispatcher()
dispatcher.set_default_handler(default_handler)

client = udp_client.SimpleUDPClient("127.0.0.1", 5006)
server = osc_server.BlockingOSCUDPServer(("127.0.0.1", 5005), dispatcher)

server.handle_request()
client.send_message("/initialized", 1)
print("waiting for handshake from python")
server.handle_request()
# client.send_message("/running", 1)

while True:
    print("waiting for task params")
    server.handle_request()
    client.send_message("/trial", 1)

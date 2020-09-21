"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
import asyncio
import numpy as np

def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")

dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(default_handler)

client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
with osc_server.BlockingOSCUDPServer(("127.0.0.1", 5006), dispatcher) as server:
    client.send_message("/grid", [8,8])
    
    trials = np.random.choice(np.arange(64),64)
    for i in trials:
        client.send_message("/select", [int(i)])
        server.handle_request()
    
    client.send_message("/end", [0])
    

# reply = 0

# def filter_handler(address, *args):
#     global reply
#     reply = args[0]
#     # print(f"{address}: {args}")
#     print("reply: ",reply)

# dispatcher = dispatcher.Dispatcher()
# dispatcher.map("/filter", filter_handler)

# ip = "127.0.0.1"
# port = 5006

# async def loop():
#     global reply
#     """Example main loop that only runs for 10 iterations before finishing"""
#     while reply < 60:
#         if reply > 10:
#             client.send_message("/client", [random.randint(0,10),time.time()])
#             client.send_message("/python", random.random())
#         await asyncio.sleep(1)

# async def init_main():
#     server = osc_server.AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
#     transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving
#     await loop()  # Enter main loop of program
#     transport.close()  # Clean up serve endpoint

# asyncio.run(init_main())

# print("done.")


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

numchannels = 8
channel_grid_dict = {}
channel_grid_dict[8] = [2,4]
channel_grid_dict[16] = [4,4]
channel_grid_dict[64] = [8,8]


dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(default_handler)

client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
with osc_server.BlockingOSCUDPServer(("127.0.0.1", 5006), dispatcher) as server:

    client.send_message("/metadata", [numchannels, "../../data/calibration"])
    msg = server.handle_request()
    print(msg)

    client.send_message("/grid", channel_grid_dict[numchannels])
    
    trials = np.random.choice(np.arange(numchannels),numchannels,replace=False)
    for i in trials:
        client.send_message("/select", [int(i)])
        server.handle_request() # blocks to recieve message
    
    client.send_message("/end", [0])
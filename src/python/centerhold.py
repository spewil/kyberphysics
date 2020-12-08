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
import utils

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


folder = "../../data/reaching"
base_filename = folder + "/test/"
metadata_filename = base_filename + "_behavior"
num_channels = 32
random_channels = np.random.choice(range(num_channels), size=num_channels, replace=False)
ITI = 1 # seconds

# TODO: add decoder and dynamics filename messages for Decoder

client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
with osc_server.BlockingOSCUDPServer(("127.0.0.1", 5006), dispatcher) as server:
    
    # compute target coordinates for each trial
    xy = utils.roots_of_unity(num_channels).T
    x = xy[0,:]
    y = xy[1,:]
    client.send_message("/metadata", [num_channels, metadata_filename])
    for i, target_channel in zip(range(num_channels), random_channels):
        # Item1 as TargetX
        # Item2 as TargetY
        # Item3 as Radius
        # Item4 as TimeoutTime
        # Item5 as HoldingTime
        # Item6 as ReachTime
        data_filename = base_filename + "emg__direction_" + str(target_channel) + "_trial_" + str(i)
        client.send_message("/start", [data_filename, float(x[target_channel]), float(y[target_channel]) , 0.1, 5000, 500, 5000])
        server.handle_request()
        time.sleep(ITI)
    client.send_message("/session_end", 1)
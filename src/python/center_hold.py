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

num_channels = 64
buffer_size = 10 
sampling_freq = 2000
record_path = "C:/Users/spencer/data/experiment_1/spencer_wilson/session_3/"
subject_folder = "C:\Users/spencer/Dropbox (Personal)/phd/experiments/experiment_1/subjects/spencer_wilson/"
decoder_filename = subject_folder + "decoder.bin"
dynamics_filename = subject_folder + "dynamics.bin"

recording_params = [num_channels, buffer_size, sampling_freq, str(record_path)]
decoding_params = [decoder_filename, dynamics_filename]

folder = "../../data/andy/"
base_filename = folder + "/center_hold_circular_1/"
metadata_filename = base_filename + "_behavior"
num_channels = 32
random_channels = np.random.choice(range(num_channels), size=num_channels, replace=False)
ITI = 1 # seconds

radius = 0.1
timeout_time = 5000
holding_time = 500
reach_time = 5000

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
        trial_data_filename = base_filename + "emg__direction_" + str(target_channel) + "_trial_" + str(i) + "__"
        client.send_message("/start", [trial_data_filename, float(x[target_channel]), float(y[target_channel]) , radius, timeout_time, holding_time, reach_time])
        server.handle_request()
        time.sleep(ITI)
    client.send_message("/session_end", 1)
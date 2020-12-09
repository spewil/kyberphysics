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

numchannels = 32
channel_grid_dict = {}
channel_grid_dict[8] = [8,1]
channel_grid_dict[16] = [4,4]
channel_grid_dict[32] = [8,4]
channel_grid_dict[64] = [8,8]

sample_frequency = 2000
buffer_length = 50
seconds_per_trial = 10
buffers_per_trial = (sample_frequency//buffer_length)*seconds_per_trial

# when bonsai starts, it cant record because it needs metadata for the recording

dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(default_handler)

client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
with osc_server.BlockingOSCUDPServer(("127.0.0.1", 5006), dispatcher) as server:

    # we are acquiring data from the device
    # send the metadata
    client.send_message("/metadata", [numchannels, "../../data/andy/dot_calibration", buffers_per_trial])
    # get an "initialized" response
    msg = server.handle_request()
    print(msg)

    # all set up, waiting for grid
    # send grid  
    client.send_message("/grid", channel_grid_dict[numchannels])
    
    # signal is piped into a row of "data" when select message is sent 
    trials = np.random.choice(np.arange(numchannels),numchannels,replace=False)
    for i in trials:
        client.send_message("/select", [int(i)])
        server.handle_request() # blocks to recieve message
    
    client.send_message("/end", [0])

# edit c# PointGrid.cs script to change the dot layout etc

# for each of these sessions, there will be a data block (trials x channels x time) upt o transpose
# .csv file with the channel order sent through the select message
# metadata from subject, day, etc etc --> another .csv 

# todo;
# - compute abs path here for data file, send entire path to bonsai
# - 

# sending data filename, format it like a python string
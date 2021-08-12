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

sample_frequency = 2000
buffer_length = 50
seconds_per_trial = 10
buffers_per_trial = (sample_frequency//buffer_length)*seconds_per_trial

numchannels = 
filepath = "../../data/test/bar_calibration"

# when bonsai starts, it cant record because it needs metadata for the recording

dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(default_handler)

client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
with osc_server.BlockingOSCUDPServer(("127.0.0.1", 5006), dispatcher) as server:

    # we are acquiring data from the device
    # send the metadata
    client.send_message("/metadata", [numchannels, filepath, buffers_per_trial])
    # get an "initialized" response
    msg = server.handle_request()
    print(msg)
    
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
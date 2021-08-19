"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time

from numpy.core.records import record
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
import asyncio
import numpy as np
import utils
import generate_mappings as genmaps

def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

def default_handler(address, *args):
    print(f"BONSAI {address}: {args}")

dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(default_handler)

num_channels = 64
num_targets = 4
buffer_size = 10 
sampling_freq = 2000
home_path_windows = "C:/Users/spencer/"
home_path_unix = "/mnt/c/Users/spencer/"
record_path = home_path_windows+"data/experiment_1/spencer_wilson/session_3/"
subject_folder = "Dropbox (Personal)/phd/experiments/experiment_1/subjects/spencer_wilson/"
decoder_filename = subject_folder + "decoder.bin"
dynamics_filename = subject_folder + "dynamics.bin"

dynamics, decoder = genmaps.generate_dynamics_and_mapping(num_channels=64, mapping_type="identity", save=True, dynamics_filename=home_path_unix+dynamics_filename, decoder_filename=home_path_unix+decoder_filename)

recording_params = [num_channels, buffer_size, sampling_freq, str(record_path)]
print(recording_params)
decoding_params = [home_path_windows+decoder_filename, home_path_windows+dynamics_filename]
print(decoding_params)
metadata_filename = subject_folder + "metadata.json"
random_targets = np.random.choice(range(num_targets), size=num_targets, replace=False)
ITI = 1 # seconds

radius = 0.05
timeout_time = 5000 # ms
holding_time = 500 # ms
reach_time = 5000 # ms

# ideally nothing computed by bonsai! 

client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
with osc_server.BlockingOSCUDPServer(("127.0.0.1", 5006), dispatcher) as server:
    
    # compute target coordinates for each trial
    xy = utils.roots_of_unity(num_targets).T
    scale=1
    x = xy[0,:]*scale
    y = xy[1,:]*scale
    client.send_message("/decoding_params", decoding_params)
    client.send_message("/recording_params", recording_params)
    server.handle_request()
    input("Press enter to begin session.")

    session_filename = record_path + "session_outcomes"
    client.send_message("/session_params", session_filename)
    for i, target_idx in zip(range(num_targets), random_targets):
        trial_emg_filename = record_path + "emg__direction_trial_" + str(i) + "__"
        trial_behavior_filename = record_path + "behavior__direction_trial_" + str(i) + "__"
        task_params = [trial_emg_filename, \
                      trial_behavior_filename, \
                      float(x[target_idx]), \
                      float(y[target_idx]), \
                      radius, \
                      timeout_time, \
                      holding_time, \
                      reach_time]
        client.send_message("/trial_params", task_params)
        client.send_message("/trial_index", i)
        print(task_params)
        server.handle_request()
        time.sleep(ITI)
    client.send_message("/end_session", 1)
    server.handle_request()

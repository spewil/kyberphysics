import argparse
from os import replace
import random
import time
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
import asyncio
import sys
import json
from pathlib import Path
import numpy as np
import utils

def print_volume_handler(unused_addr, args, volume):
    print("[{0}] ~ {1}".format(args[0], volume))


def print_compute_handler(unused_addr, args, volume):
    try:
        print("[{0}] ~ {1}".format(args[0], args[1](volume)))
    except ValueError:
        pass


def default_handler(address, *args):
    pass


# print(f"DEFAULT {address}: {args}")

dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(default_handler)

client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
server = osc_server.BlockingOSCUDPServer(("127.0.0.1", 5006), dispatcher)

# base_experiment_folder = Path(
#     "/mnt/c/Users/spencer/Documents/kyberphysics/metadata/")
# base_data_folder = Path("C:/Users/spencer/data/")
# data_extension = ".bin"

experiment = sys.argv[1]
session = sys.argv[2]
subject = sys.argv[3]

record_path = utils.setup_record_path(experiment, session, subject)
experiment_metadata, session_metadata, subject_metadata = utils.get_metadata(experiment, session, subject)

# experiment_folder = base_experiment_folder / experiment
# # assert experiment_folder.exists(), print(f"path {experiment_folder} not found" )
# subject_folder = experiment_folder / subject
# # assert subject_folder.exists(), print(f"path {subject_folder} not found" )
# experiment_data_folder = base_data_folder / experiment
# # assert experiment_data_folder.exists(), print(f"path {experiment_data_folder} not found" )
# subject_data_folder = experiment_data_folder / subject
# # assert subject_data_folder.exists(), print(f"path {subject_data_folder} not found" )
# record_path = subject_data_folder / "calibration_bars"

# print(subject_folder)
# print(subject_data_folder)

# with open(experiment_folder / "recording.json", 'r') as fp:
#     experiment_metadata = json.load(fp)

# with open(subject_folder / "metadata.json", 'r') as fp:
#     subject_metadata = json.load(fp)

num_channels = experiment_metadata.get("num_channels", 64)
commands = np.arange(num_channels)
  # [command.strip("\n") for command in command_file.readlines()]

sampling_freq = experiment_metadata.get("sampling_freq", 2000)
# show the commmand for x seconds
seconds_per_command = experiment_metadata.get("seconds_per_command", 2)
# data_extension = experiment_metadata.get("data_extension", ".bin")
# show command + cue for y seconds
num_repetitions = experiment_metadata.get("num_repetitions", 5)
ITI = experiment_metadata.get("ITI", 2)

# num_samples = sampling_freq*seconds_per_command
# must be a multiple of buffer size for sample precision timing
samples_per_command = sampling_freq * seconds_per_command

buffer_size = experiment_metadata.get("buffer_size", 10)
buffer_size = 20
# show command for samples_per_command
# show command + cue for samples_per_cue
# show blank for samples_per_ITI

recording_params = [num_channels, buffer_size, sampling_freq, str(record_path)]

client.send_message("/recording_params", recording_params)
msg = server.handle_request()  # blocks to recieve message
input("Enter to begin recording session.")

for command in commands:
    task_params = [samples_per_command, int(command)]
    client.send_message("/task_params", task_params)
    msg = server.handle_request()  # blocks to recieve message
    print("SLEEP")
    time.sleep(ITI)
client.send_message("/stop", 1)

# command_file.close()

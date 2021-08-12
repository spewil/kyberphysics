import argparse
import random
import time
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
import asyncio
import sys
import json
from pathlib import Path

def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

def default_handler(address, *args):
	pass
    # print(f"DEFAULT {address}: {args}")

dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(default_handler)

client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
server = osc_server.BlockingOSCUDPServer(("127.0.0.1", 5006), dispatcher)

base_experiment_folder = Path("/mnt/c/Users/spencer/Dropbox (Personal)/phd/experiments/")
base_data_folder = Path("/mnt/c/Users/spencer/data/")
data_extension = ".bin"

experiment = sys.argv[1]
subject = sys.argv[2]

experiment_folder = base_experiment_folder / experiment
assert experiment_folder.exists(), print(f"path {experiment_folder} not found" )
subject_folder = experiment_folder / "subjects" / subject
assert subject_folder.exists(), print(f"path {subject_folder} not found" )
experiment_data_folder = base_data_folder / experiment
assert experiment_data_folder.exists(), print(f"path {experiment_data_folder} not found" )
subject_data_folder = experiment_data_folder / subject
assert subject_data_folder.exists(), print(f"path {subject_data_folder} not found" )
record_path = subject_data_folder / ""

print(subject_folder)
print(subject_data_folder)

with open(experiment_folder / "experiment.json", 'r') as fp:
	experiment_metadata = json.load(fp)

with open(subject_folder / "metadata.json", 'r') as fp:
	subject_metadata = json.load(fp)

command_filepath = experiment_metadata["command_file"]
command_file = open(experiment_folder / command_filepath, 'r')
commands = [command.strip("\n") for command in command_file.readlines()]
print(command_filepath)

num_channels = experiment_metadata["num_channels"]
sampling_freq = experiment_metadata["sampling_freq"]
seconds_per_command = experiment_metadata["seconds_per_command"]
data_extension = experiment_metadata["data_extension"]
num_samples = sampling_freq*seconds_per_command

print(num_channels)

for command in commands:
	print(command)
	# client.send_message("/recording_params", [num_samples, num_channels, buffer_size, data_filepath, command])
	# msg = server.handle_request() # blocks to recieve message
# client.send_message("/stop", 1)

command_file.close() 
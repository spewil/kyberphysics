import time
from utils import utils
from pathlib import Path
import sys

# grab experiment name and subject name
experiment = sys.argv[1]
session = Path(__file__).name.split(".")[0]  # script name is session name
subject = sys.argv[2]

# compute record path
record_path = str(utils.setup_record_path(experiment, session, subject))
print("RECORD PATH")
print(record_path)

# grab the metadata
experiment_metadata, session_metadata, subject_metadata = utils.get_metadata(
    experiment, session, subject)

#  RECORDING
num_channels = experiment_metadata["num_channels"]
sampling_freq = experiment_metadata["sampling_freq"]
buffer_size = experiment_metadata["buffer_size"]
recording_params = [num_channels, buffer_size, sampling_freq, str(record_path)]

# SESSION
commands = session_metadata["movements"]
samples_per_command = sampling_freq * session_metadata["seconds_per_command"]
samples_per_cue = sampling_freq * session_metadata["seconds_per_cue"]
num_repetitions = session_metadata["num_repetitions"]
ITI = session_metadata["ITI"]

client, server = utils.setup_osc()

print("sending recording params.")
client.send_message("/recording_params", recording_params)
print("waiting for initialization...")
server.handle_request()
print("bonsai initialized.")
input("Enter to begin recording session.")

time.sleep(3)
for i, command in enumerate(commands):
    task_params = [
        samples_per_command, samples_per_cue, num_repetitions, command
    ]
    print("trial ", i, ": ", task_params)
    client.send_message("/task_params", task_params)
    server.handle_request()
    time.sleep(ITI)
client.send_message("/stop", 1)

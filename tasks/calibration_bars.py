import numpy as np
import time
import sys
import utils

def make_target_channels():
    channels = []
    for i in range(8):
        for j in range(0, 7, 2):
            if i % 2 == 0:
                channels.append(j + (i * 8))
            else:
                channels.append(j + (i * 8) + 1)
    return channels

client, server = utils.setup_osc()

# grab experiment name and subject name
experiment = sys.argv[1]
session = __file__.split(".")[0]  # script name is session name
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
recording_params = [num_channels, buffer_size, sampling_freq, record_path]

# SESSION
target_channels = make_target_channels()
print(np.array(target_channels).reshape(-1, 4))
print(len(target_channels))
seconds_per_trial = session_metadata["seconds_per_trial"]
samples_per_trial = sampling_freq * seconds_per_trial
ITI = session_metadata["ITI"]
scale = session_metadata["emg_to_bar_scale"]

print("sending recording params.")
client.send_message("/recording_params", recording_params)
# print("sending session params.")
# client.send_message("/session_params", scale)
print("waiting for initialization...")
server.handle_request()
print("bonsai initialized.")
input("Enter to begin recording session.")

for i, channel in enumerate(target_channels):
    print(f"TRIAL {i} : CHANNEL {channel}")
    task_params = [samples_per_trial, int(channel)]
    client.send_message("/task_params", task_params)
    msg = server.handle_request()
    time.sleep(ITI)
client.send_message("/stop", 1)

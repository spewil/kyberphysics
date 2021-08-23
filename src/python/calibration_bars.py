import numpy as np
import time
import sys
import utils

client, server = utils.setup_osc()

# grab experiment name and subject name
experiment = sys.argv[1]
session = __file__.split(".")[0]  # script name is session name
subject = sys.argv[2]

# compute record path
record_path = utils.setup_record_path(experiment, session, subject)

# grab the metadata
experiment_metadata, session_metadata, subject_metadata = utils.get_metadata(
    experiment, session, subject)

#  RECORDING
num_channels = experiment_metadata["num_channels"]
sampling_freq = experiment_metadata["sampling_freq"]
buffer_size = experiment_metadata["buffer_size"]
recording_params = [num_channels, buffer_size, sampling_freq, str(record_path)]

# SESSION
target_channels = np.arange(num_channels)
seconds_per_trial = session_metadata["seconds_per_trial"]
samples_per_trial = sampling_freq * seconds_per_trial
ITI = session_metadata["ITI"]

client.send_message("/recording_params", recording_params)
msg = server.handle_request()
input("Enter to begin recording session.")

for channel in target_channels:
    task_params = [samples_per_trial, int(channel)]
    client.send_message("/task_params", task_params)
    msg = server.handle_request()
    time.sleep(ITI)
client.send_message("/stop", 1)

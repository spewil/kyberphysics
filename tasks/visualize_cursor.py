import time
import sys
import numpy as np
from pathlib import Path
from utils import utils

msg = None


def strip_newlines(message):
    return str(message).strip("\n")


def center_hold_handler(address, *args):
    global msg
    msg = strip_newlines(args[0])
    print("Message Handler: ", msg)
    print(f"{address}: {args}")


client, server = utils.setup_osc(center_hold_handler)

# grab experiment name and subject name
experiment = sys.argv[1]
session = Path(__file__).name.split(".")[0]  # script name is session name
print("hello", session)
subject = sys.argv[2]

# grab the metadata
experiment_metadata, session_metadata, subject_metadata = utils.get_metadata(
    experiment, "center_hold", subject)

#  RECORDING
num_channels = experiment_metadata["num_channels"]
sampling_freq = experiment_metadata["sampling_freq"]
buffer_size = experiment_metadata["buffer_size"]
record_folder = utils.setup_record_path(experiment,
                                        "center_hold",
                                        subject,
                                        add_session=False,
                                        convert_to_windows=False)

# SESSION
num_targets = session_metadata["num_targets"]
ITI = session_metadata["ITI"]
ISI = session_metadata["ISI"]
radius = session_metadata["radius"]
timeout_time = session_metadata["timeout_time"]
holding_time = session_metadata["holding_time"]
reach_time = session_metadata["reach_time"]
max_holds = session_metadata["max_holds"]

# SUBJECT
subject_folder = utils.get_subject_folder(experiment, subject)
decoder_filename = (subject_folder / "decoder.bin").resolve()
dynamics_filename = (subject_folder / "dynamics.bin").resolve()
variance_filename = (subject_folder / "variance.bin").resolve()
offset_filename = (subject_folder / "offsets.bin").resolve()

decoding_params = [
    str(utils.convert_abspath_wsl_to_windows(decoder_filename)),
    str(utils.convert_abspath_wsl_to_windows(dynamics_filename)),
    str(utils.convert_abspath_wsl_to_windows(variance_filename)),
    str(utils.convert_abspath_wsl_to_windows(offset_filename))
]

# compute target coordinates for each trial
xy = utils.roots_of_unity(num_targets).T
x = xy[0, :]
y = xy[1, :]

# SESSION LOOP

recording_params = [num_channels, buffer_size, sampling_freq, ""]
print(f"sending recording params: {recording_params}")
client.send_message("/recording_params", recording_params)
print(f"sending decoding params: {decoding_params}")
client.send_message("/decoding_params", decoding_params)
print("waiting for initialization...")
server.handle_request()
print("bonsai initialized.")
input("Enter to begin recording.")

time.sleep(1)
target_indices = np.random.choice(range(num_targets),
                                size=num_targets,
                                replace=False)
task_params = [
    str(0),
    float(x[target_indices[0]]),
    float(y[target_indices[0]]), radius, timeout_time, holding_time,
    reach_time
]
print(f"Trial {0} -- Task Params: {task_params}")
client.send_message("/trial_params", task_params)
server.handle_request()

input("Running...")

client.send_message("/stop", 1)

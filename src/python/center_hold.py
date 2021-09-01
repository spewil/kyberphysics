import time
import sys
import numpy as np
import utils
import sys
import io

def grab_input_from_buffer(osc_server):
    old_stdout = sys.stdout # Memorize the default stdout stream
    sys.stdout = buffer = io.StringIO()
    osc_server.handle_request()
    sys.stdout = old_stdout # Put the old stream back in place
    return buffer.getvalue() # Return a str containing the entire contents of the buffer.

def center_hold_handler(address, *args):
    print(args[0])

def strip_newlines(message):
    return str(message).strip("\n")

client, server = utils.setup_osc(center_hold_handler)

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
num_targets = session_metadata["num_targets"]
target_indices = np.random.choice(range(num_targets),
                                  size=num_targets,
                                  replace=False)
ITI = session_metadata["ITI"]
radius = session_metadata["radius"]
timeout_time = session_metadata["timeout_time"]
holding_time = session_metadata["holding_time"]
reach_time = session_metadata["reach_time"]
min_scale = session_metadata["min_scale"]
max_scale = session_metadata["max_scale"]
session_params = [min_scale, max_scale]

# SUBJECT
subject_folder = utils.get_subject_folder(experiment, subject)
decoder_filename = (subject_folder / "decoder.bin").resolve()
dynamics_filename = (subject_folder / "dynamics.bin").resolve()

decoding_params = [
    str(utils.convert_abspath_wsl_to_windows(decoder_filename)),
    str(utils.convert_abspath_wsl_to_windows(dynamics_filename))
]

# dynamics, decoder = generate_mappings.generate_dynamics_and_mapping(
#     num_channels=64,
#     mapping_type="identity",
#     save=True,
#     dynamics_filename=home_path_unix + dynamics_filename,
#     decoder_filename=home_path_unix + decoder_filename)

# compute target coordinates for each trial
xy = utils.roots_of_unity(num_targets).T
x = xy[0, :]
y = xy[1, :]

print("sending recording params.")
client.send_message("/recording_params", recording_params)
print("sending session params.")
client.send_message("/session_params", session_params)
print("sending decoding params.")
client.send_message("/decoding_params", decoding_params)
print("waiting for initialization...")
server.handle_request()
print("bonsai initialized.")
input("Enter to begin recording session.")

for i, target_idx in enumerate(target_indices):
    num_no_holds = 0
    task_params = [
        str(i),
        float(x[target_idx]),
        float(y[target_idx]), 
        radius, timeout_time, holding_time, reach_time
    ]
    print(f"Trial {i} -- Task Params: {task_params}")
    client.send_message("/trial_params", task_params)
    msg = strip_newlines(grab_input_from_buffer(server))
    print(f"Outcome: {msg}")
    time.sleep(ITI)
    while msg == "No Hold":
        num_no_holds += 1
        print(f"Rehold {num_no_holds}")
        print(f"Trial {i} -- Task Params: {task_params}")
        client.send_message("/trial_params", task_params)
        msg = strip_newlines(grab_input_from_buffer(server))
        print(f"Outcome: {msg}")
        if num_no_holds > 2: # third attempt finished
            msg = None
            print("Number of hold attempts exceeded.")
        time.sleep(ITI)
client.send_message("/stop", 1)

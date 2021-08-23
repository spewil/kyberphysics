import time
import sys
import numpy as np
import utils
import generate_mappings

home_path_windows = "C:/Users/spencer/"
home_path_unix = "/mnt/c/Users/spencer/"
record_path = home_path_windows + "data/experiment_1/spencer_wilson/session_3/"
subject_folder = "Documents/kyberphysics/metadata/emg_olympics/spencer/"

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
num_targets = session_metadata["num_targets"]
target_indices = np.random.choice(range(num_targets),
                                  size=num_targets,
                                  replace=False)
ITI = session_metadata["ITI"]
radius = session_metadata["radius"]
timeout_time = session_metadata["timeout_time"]
holding_time = session_metadata["holding_time"]
reach_time = session_metadata["reach_time"]

# SUBJECT
subject_folder = utils.get_subject_folder(
    experiment,
    subject)  # "Documents/kyberphysics/metadata/emg_olympics/spencer/"
decoder_filename = subject_folder / "decoder.bin"
dynamics_filename = subject_folder / "dynamics.bin"
decoding_params = [
    str(decoder_filename.resolve()),
    str(dynamics_filename.resolve())
]
print(decoding_params)

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

# emg running
client.send_message("/recording_params", recording_params)
server.handle_request()
client.send_message("/subject_params", decoding_params)
input("Press enter to begin session.")

# TODO
# - fix session filename with bonsai filepath (record path+"session_outcomes")
# - fix trial filename, do this in bonsai? (record path + "emg_" + trial_idx)

for i, target_idx in zip(range(num_targets), target_indices):
    trial_emg_filename = str(record_path) + "emg_" + str(i)
    trial_behavior_filename = str(record_path) + "behavior_" + str(i)
    task_params = [
        trial_emg_filename, trial_behavior_filename,
        float(x[target_idx]),
        float(y[target_idx]), radius, timeout_time, holding_time, reach_time
    ]
    print(float(x[target_idx]), float(y[target_idx]))
    client.send_message("/trial_params", task_params)
    client.send_message("/trial_index", i)  # use this for filename?
    server.handle_request()
    time.sleep(ITI)
client.send_message("/end_session", 1)
server.handle_request()

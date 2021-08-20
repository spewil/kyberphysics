import time
import utils
import sys

client, server = utils.setup_osc()

# grab experiment name and subject name
experiment = sys.argv[1]
session = sys.argv[2]
subject = sys.argv[3]

# compute record path
record_path = utils.setup_record_path(experiment, session, subject)
# grab the metadata
experiment_metadata, session_metadata, subject_metadata = utils.get_metadata(
    experiment, session, subject)

command_filepath = experiment_metadata["command_file"]
commands = session_metadata["movements"]

#  RECORDING
num_channels = experiment_metadata.get("num_channels")
sampling_freq = experiment_metadata.get("sampling_freq")
buffer_size = experiment_metadata.get("buffer_size", 10)

# TASK
# show the commmand for x seconds
seconds_per_command = experiment_metadata.get("seconds_per_command")
# show command + cue for y seconds
seconds_per_cue = experiment_metadata.get("seconds_per_cue")
num_repetitions = experiment_metadata.get("num_repetitions")
ITI = experiment_metadata.get("ITI")

samples_per_command = sampling_freq * seconds_per_command
samples_per_cue = sampling_freq * seconds_per_cue

recording_params = [num_channels, buffer_size, sampling_freq, str(record_path)]

client.send_message("/recording_params", recording_params)
msg = server.handle_request()  # blocks to recieve message
# separate task and acquisition specific stuff

input("Enter to begin recording session.")

for command in commands:
    task_params = [
        samples_per_command, samples_per_cue, num_repetitions, command
    ]
    client.send_message("/task_params", task_params)
    msg = server.handle_request()  # blocks to recieve message
    time.sleep(ITI)
client.send_message("/stop", 1)

command_file.close()

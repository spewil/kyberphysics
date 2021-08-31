import numpy as np
from numpy.core.einsumfunc import _update_other_results
from numpy.core.records import record
from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher
import json
import pathlib
import sys
import os


def test_dynamics():
    # timesteps = 100
    # states = np.zeros((6, timesteps))
    # state = np.zeros((6, 1))
    # controls = np.zeros((32, timesteps))
    # controls[7, :] = np.hstack(
    #     [np.ones(timesteps // 4) * .1,
    #      np.zeros(3 * timesteps // 4)])

    # for i in range(timesteps):
    #     states[:, i] = state[:, 0]
    #     state = advance_dynamics(dynamics, state, decoder,
    #                              controls[:, i].reshape(-1, 1))
    pass


def roots_of_unity(num_points, radius=1, offset=0):
    # offset in radians
    c = 2j * np.pi / num_points
    points = [
        [np.around(x.imag, decimals=2),
         np.around(x.real, decimals=2)] for x in
        [radius * np.exp((k * c) + 1j * offset) for k in range(num_points)]
    ]
    return np.array(points)


def advance_dynamics(A, state, B, control):
    return np.dot(A, state) + np.dot(B, control)


def write_array_to_disk(a, name):
    with open(name, "wb") as file:
        file.write(a.tobytes())


def load_array_from_disk(path):
    return np.fromfile(path, dtype=np.float32)


def setup_osc(handler=None):
    if handler is None:

        def default_handler(address, *args):
            print(f"BONSAI {address}: {args}")

        dispatcher = Dispatcher()
        dispatcher.set_default_handler(default_handler)
    else:
        dispatcher = Dispatcher()
        dispatcher.set_default_handler(handler)

    client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
    server = osc_server.BlockingOSCUDPServer(("127.0.0.1", 5006), dispatcher)

    return client, server


def get_experiment_folder(experiment):
    base_metadata_folder = pathlib.Path.cwd().parent.parent  # module path
    experiment_folder = base_metadata_folder / "metadata" / experiment
    assert experiment_folder.exists(), f"Path {experiment_folder} not found"
    return experiment_folder


def get_subject_folder(experiment, subject):
    experiment_folder = get_experiment_folder(experiment)
    subject_folder = experiment_folder / subject
    assert subject_folder.exists(), f"Path {subject_folder} not found"

    return subject_folder


def get_experiment_metadata(experiment):
    experiment_folder = get_experiment_folder(experiment)
    with open(experiment_folder / "metadata.json", 'r') as fp:
        experiment_metadata = json.load(fp)
    return experiment_metadata


def get_session_metadata(experiment, session):
    experiment_folder = get_experiment_folder(experiment)
    with open(experiment_folder / (session + ".json"), 'r') as fp:
        session_metadata = json.load(fp)
    return session_metadata


def get_subject_metadata(experiment, subject):
    subject_folder = get_subject_folder(experiment, subject)
    with open(subject_folder / "metadata.json", 'r') as fp:
        subject_metadata = json.load(fp)
    return subject_metadata


def get_metadata(experiment, session, subject):
    return get_experiment_metadata(experiment), get_session_metadata(
        experiment, session), get_subject_metadata(experiment, subject)


def setup_record_path(experiment, session, subject):

    if sys.platform == "linux":
        base_data_folder = pathlib.Path("/mnt/c/Users/spencer/data/")
    else:
        base_data_folder = pathlib.Path("/Users/spencerw/phd_data/")
    experiment_data_folder = base_data_folder / experiment
    assert experiment_data_folder.exists(
    ), f"Path {experiment_data_folder} not found"
    subject_data_folder = experiment_data_folder / subject
    assert subject_data_folder.exists(
    ), f"Path {subject_data_folder} not found"
    record_path = subject_data_folder / session
    assert record_path.exists(
    ), f"Path {subject_data_folder / session} not found"
    record_path = add_session_folder(record_path)

    if sys.platform == "linux":
        return convert_abspath_wsl_to_windows(record_path)
    else:
        return record_path


def add_session_folder(path):
    num_existing_folders = len([_ for _ in path.iterdir() if _.is_dir()])
    new_path = path / ("session_" + str(num_existing_folders))
    return new_path


def convert_abspath_wsl_to_windows(abspath):
    converted_path = "C:/"
    for s in list(abspath.parts)[3:]:
        converted_path += (s + "/")
    converted_path = pathlib.Path(converted_path)
    return converted_path


def compute_experiment_time(experiment):
    experiment_metadata = get_experiment_metadata(experiment)
    tasks = experiment_metadata["tasks"]
    total_time = 0
    for task in tasks:
        total_time += experiment_metadata["num_sessions_per_task"][task] * globals()["compute_" + task + "_time"](experiment)
    total_time /= 3600  # hours
    return total_time


def compute_natural_movement_time(experiment):
    session_metadata = get_session_metadata(experiment, "natural_movement")
    # num_movements * (ITI + (command + cue)*reps)
    return len(session_metadata["movements"]) * (
        session_metadata["ITI"] + (session_metadata["num_repetitions"] *
                                   (session_metadata["seconds_per_command"] +
                                    session_metadata["seconds_per_cue"])))


def compute_calibration_bars_time(experiment):
    experiment_metadata = get_experiment_metadata(experiment)
    session_metadata = get_session_metadata(experiment, "calibration_bars")
    return experiment_metadata["num_channels"] * (
        session_metadata["ITI"] + session_metadata["seconds_per_trial"])


def compute_center_hold_time(experiment):
    session_metadata = get_session_metadata(experiment, "center_hold")
    return session_metadata["num_targets"] * 0.5 * 0.001 * (
        session_metadata["holding_time"] + session_metadata["reach_time"])


if __name__ == "__main__":
    print(compute_experiment_time("self_test"))

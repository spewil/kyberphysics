import numpy as np
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


def get_metadata(experiment, session, subject):

    # basic paths

    base_metadata_folder = pathlib.Path(
        os.path.dirname(__file__)).parent.parent / "metadata"

    # confirm session folders have been made
    experiment_folder = base_metadata_folder / experiment
    assert experiment_folder.exists(), f"Path {experiment_folder} not found"
    subject_folder = experiment_folder / subject
    assert subject_folder.exists(), f"Path {subject_folder} not found"

    print("SUBJECT FOLDER")
    print(subject_folder)

    with open(experiment_folder / ("recording" + ".json"), 'r') as fp:
        experiment_metadata = json.load(fp)

    with open(experiment_folder / (session + ".json"), 'r') as fp:
        session_metadata = json.load(fp)

    with open(subject_folder / "metadata.json", 'r') as fp:
        subject_metadata = json.load(fp)

    return experiment_metadata, session_metadata, subject_metadata


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

    print("RECORD PATH")
    print(record_path)

    path = "C:/"
    for s in list(record_path.parts)[3:]:
        path += (s+"/")

    return path[:-1]

if __name__ == "__main__":
    record_path = setup_record_path("emg_olympics","calibration_bars","spencer")
    print(record_path)
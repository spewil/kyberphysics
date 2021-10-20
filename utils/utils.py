import numpy as np
from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher
import json
import pathlib
import sys
from utils import files, analysis


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


def write_array_to_disk(a, path, overwrite=False):
    if overwrite:
        with open(path, "wb") as file:
            file.write(a.tobytes())
    else:
        if path.exists():
            raise FileExistsError
        else:
            with open(path, "wb") as file:
                file.write(a.tobytes())

def load_array_from_disk(path, dtype=np.float32):
    return np.fromfile(path, dtype=dtype)


def setup_osc(handler=None):
    dispatcher = Dispatcher()
    if handler is None:

        def default_handler(address, *args):
            print(f"BONSAI {address}: {args}")

        dispatcher.set_default_handler(default_handler)
    else:
        dispatcher.set_default_handler(handler)

    client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
    server = osc_server.BlockingOSCUDPServer(("127.0.0.1", 5006), dispatcher)

    return client, server


def get_session_path(d, subject, task, session):
    return d["subjects"][subject]["tasks"][task]["sessions"][session]


def load_movement_emg(session_path, movement=None):
    data = {}
    # emg
    emg_paths = sorted(
        [x for x in session_path.iterdir() if x.suffix == ".bin"], key=str)
    for p in emg_paths:
        name = p.name.rstrip(".bin")[:-17]
        print(name)
        data.update({name: {}})
        data[name].update(
            {"emg": np.fromfile(p, dtype=np.int32).reshape(-1, 68)})
    # cue
    cue_paths = sorted([x for x in session_path.iterdir() if "cue" in x.name],
                       key=str)
    print(cue_paths)
    for p in cue_paths:
        name = p.name.rstrip(".bin")[:-28]
        cue = np.genfromtxt(str(p), delimiter=',')[:, 2].reshape(-1, 1)
        data[name].update({"cue_raw": cue})
        data[name].update({
            "cue":
            np.round(
                np.interp(
                    np.linspace(0,
                                cue.shape[0],
                                data[name]["emg"].shape[0],
                                endpoint=True), np.arange(cue.shape[0]),
                    cue[:, 0]))
        })
    if movement is None:
        return data
    else:
        return data[movement]


def load_calibration_emg(session_path, channel=None):
    data = {}
    paths = sorted([
        x for x in session_path.iterdir()
        if x.suffix == ".bin" and "emg" in x.name
    ])
    for p in paths:
        prefix = files.parse_filename_prefix(p)
        data[str(prefix)] = np.fromfile(p, dtype=np.int32).reshape(-1, 68)
    if channel is None:
        return data
    else:
        return data[channel]


def load_calibration_filtered(session_path, channel=None):
    data = {}
    paths = sorted([
        x for x in session_path.iterdir()
        if x.suffix == ".bin" and "filtered" in x.name
    ])
    for p in paths:
        prefix = files.parse_filename_prefix(p)
        data[str(prefix)] = np.fromfile(p, dtype=np.float32).reshape(-1, 68)
    if channel is None:
        return data
    else:
        return data[channel]


def load_center_hold_emg(session_path, channel=None):
    data = {}
    paths = sorted([
        x for x in session_path.iterdir()
        if "emg" in x.name and "filtered" not in x.name and x.suffix == ".bin"
    ],
                   key=files.parse_filename_prefix)
    for p in paths:
        prefix = files.parse_filename_prefix(p)
        data[str(prefix)] = np.fromfile(p, dtype=np.int32).reshape(-1, 68)
    if channel is None:
        return data
    else:
        return data[channel]


def concat_movement_emg_trials(session_dict):
    emg = []
    for movement in session_dict.keys():
        emg.append(session_dict[movement]["emg"])
    return np.vstack(emg)


def concat_emg_trials(session_dict):
    return np.vstack(list(session_dict.values()))


def get_cue_on_indices(cue):
    # get indices where cue turns on
    step_indices = np.where(cue[:-1] != cue[1:])[0] + 1
    return step_indices[[0, 2, 4]]


def extract_quiescent(md, num_samples=500, samples_before_cue=1000):
    quiescents = []
    movements = list(md.keys())
    for movement in movements:
        movement_emg = analysis.highpass(md[movement]["emg"], cutoff=3)[:, :64]
        cue = md[movement]["cue"]
        cue_on_indices = get_cue_on_indices(cue)
        # concat intra-movement signals before cues
        for idx in cue_on_indices:
            quiescents.append(movement_emg[idx - num_samples - samples_before_cue:idx - samples_before_cue])
    return np.vstack(quiescents)



def standardize(a, s):
    assert a.shape[1] == s.shape[0]
    standardized = np.divide(a, s)
    print(standardized.shape)
    return standardized


def filter_emg(a, cutoff=5):
    filtered = analysis.lowpass(analysis.rectify(a), cutoff=cutoff)
    print(np.min(filtered), np.max(filtered))
    min_channel = np.argmin(np.min(filtered, axis=0))
    print("min channel: ", min_channel)
    filtered = analysis.rectify(filtered)
    print(np.min(filtered), np.max(filtered))
    print(filtered.shape)
    return filtered


def get_experiment_folder(experiment):
    base_folder = pathlib.Path.cwd()  # module path
    if "notebooks" in str(base_folder):
        base_folder = base_folder.parent
    experiment_folder = base_folder / "metadata" / experiment
    assert experiment_folder.exists(), f"Path {experiment_folder} not found"
    return experiment_folder


def get_experiment_data_folder(experiment):
    if sys.platform == "linux":
        base_data_folder = pathlib.Path("/mnt/c/Users/spencer/data/")
    else:
        base_data_folder = pathlib.Path(
            "/Users/spencerw/Dropbox (UCL)/Murray Lab/Spencer/")
    experiment_data_folder = base_data_folder / experiment
    assert experiment_data_folder.exists(
    ), f"Path {experiment_data_folder} not found"
    return experiment_data_folder


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
    with open(experiment_folder / (str(session) + ".json"), 'r') as fp:
        session_metadata = json.load(fp)
    return session_metadata


def get_subject_metadata(experiment, subject):
    subject_folder = get_subject_folder(experiment, subject)
    with open(subject_folder / "metadata.json", 'rb') as fp:
        subject_metadata = json.load(fp)
    return subject_metadata


def get_metadata(experiment, session, subject):
    return get_experiment_metadata(experiment), get_session_metadata(
        experiment, session), get_subject_metadata(experiment, subject)


def setup_record_path(experiment,
                      session,
                      subject,
                      add_session=True,
                      convert_to_windows=True):

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

    if add_session:
        record_path = add_session_folder(record_path)

    if convert_to_windows:
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
        total_time += experiment_metadata["num_sessions_per_task"][
            task] * globals()["compute_" + task + "_time"](experiment)
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
        session_metadata["reach_time"])


def normal(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) /
                  (2 * np.power(sig, 2.))) * (1 / (sig * np.sqrt(2 * np.pi)))


def mahalanobis(vec, inv_cov):
    prod = vec.reshape(-1, 1).T @ inv_cov @ vec.reshape(-1, 1)
    return np.sqrt(prod)[0, 0]


def polar_to_cartesian(coord):
    return [coord[0] * np.cos(coord[1]), coord[0] * np.sin(coord[1])]


def cartesian_to_polar(coord):
    output = [0, 0]
    output[0] = np.sqrt(coord[0]**2 + coord[1]**2)
    # change behavior depending on quadrant
    output[1] = np.arccos(coord[0] / output[0])
    if coord[1] >= 0:
        output[1] = np.arccos(coord[0] / output[0])
    else:
        if coord[0] >= 0:
            output[1] = -np.arccos(coord[0] / output[0])
        else:
            output[1] = np.pi + np.arccos(-coord[0] / output[0])
    return output


def radians(degrees):
    return (np.pi / 180) * degrees


def quadratic(x, a, b, start=-250):
    return a * (x - start)**2 + b


def generate_arc(num_points, radius=250, start=0, end=180, polar=False):
    start_angle_rad = (np.pi / 180) * start
    end_angle_rad = (np.pi / 180) * end
    angles = np.linspace(end_angle_rad,
                         start_angle_rad,
                         num_points,
                         endpoint=True)
    radii = np.ones(num_points) * radius
    polar_coords = np.array(list(zip(radii, angles)))
    if polar:
        return polar_coords
    else:
        return np.array([polar_to_cartesian(p) for p in polar_coords])


def unique(data: list):
    ul = []
    for x in data:
        if x not in ul:
            ul.append(x)
    return ul


# invert trajectories if it increases their correlation coeff
def align_trajectory(trajectory, reference):
    corr = np.dot(trajectory, reference)
    corr_flipped = np.dot(-trajectory, reference)
    if corr > corr_flipped:
        return trajectory
    else:
        return -trajectory


def random_matrices():
    # A problem with a low condition number is said
    # to be well-conditioned, while a problem with
    # a high condition number is said to be ill-conditioned.

    size = 5
    conds = []
    for _ in range(1000):
        A = np.random.normal(size=(size, size))
        # print(A)
        # print(np.linalg.norm(A, axis=0))
        A_normed = A / np.linalg.norm(A, axis=0)
        # print(A_normed)
        # print(np.sqrt(np.sum(A_normed[:, 1]**2)))
        conds.append(np.linalg.cond(A_normed))

    print(np.min(conds), np.max(conds), np.median(conds), np.mean(conds))
    # plt.hist(conds, bins=100)
    # plt.show()


if __name__ == "__main__":
    print(get_experiment_folder("test"))
    print(compute_experiment_time("test"))

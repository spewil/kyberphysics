import numpy as np
from utils import utils


def build_experiment_path_dict(experiment):
    data_folder = utils.get_experiment_data_folder(experiment)
    subjects = [x.name for x in data_folder.iterdir() if x.name[0] != "."]
    path_dictionary = {"subjects": {}}
    for subject in subjects:
        subject_folder = data_folder / subject
        path_dictionary["subjects"].update({subject: {}})
        path_dictionary["subjects"][subject].update({"path": subject_folder})
        tasks = [x.name for x in subject_folder.iterdir() if x.name[0] != "."]
        path_dictionary["subjects"][subject].update({"tasks": {}})
        for task in tasks:
            path_dictionary["subjects"][subject]["tasks"].update(
                {task: {
                    "path": subject_folder / task
                }})
            session_paths = sorted([
                x
                for x in (subject_folder / task).iterdir() if x.name[0] != "."
            ],
                                   key=lambda x: x.name[-1])
            session_names = [x.name for x in session_paths]
            path_dictionary["subjects"][subject]["tasks"][task].update(
                {"sessions": {}})
            for path, session in zip(session_paths, session_names):
                path_dictionary["subjects"][subject]["tasks"][task][
                    "sessions"].update({session: path})
    return path_dictionary


def parse_filename_prefix(x):
    name = x.name
    prefix = name[:2]
    if prefix[-1] == "_":
        return int(prefix[0])
    else:
        return int(prefix)


def parse_timestamp(x):
    name = x.name
    return name[-16:]


def write_array_to_disk(a, name):
    with open(name, "wb") as file:
        file.write(a.tobytes())


def data_files(directory):
    print(f'+ {directory}')
    paths = []
    for path in sorted(directory.rglob('*.data')):
        depth = len(path.relative_to(directory).parts)
        spacer = '    ' * depth
        print(f'{spacer}+ {path.name}')
        paths.append(path)
    return paths


def list_folder_names(path):
    return [e.name for e in path.iterdir() if e.is_dir()]


def list_file_names(path, ext=None):
    if ext:
        return [
            e.name for e in path.iterdir() if e.is_file() and e.suffix == ext
        ]
    else:
        return [e.name for e in path.iterdir() if e.is_file()]


def list_folders(path):
    return [e for e in path.iterdir() if e.is_dir()]


def list_files(path, ext=None):
    if ext:
        return [e for e in path.iterdir() if e.is_file() and e.suffix == ext]
    else:
        return [e for e in path.iterdir() if e.is_file()]


def load_from_bin_file(path):
    if path.suffix != ".bin":
        raise AssertionError("Files must be in binary format.")
    data = np.fromfile(path, dtype=np.int32)
    num_channels = 32
    return np.array(data.reshape(-1, num_channels + 4).T, dtype=np.float)


def load_from_file(filepath, nch, dtype, order="C"):
    with open(filepath, 'rb') as f:
        data = np.fromfile(f, dtype=dtype)
    return data.reshape(-1, nch).T


def tree(directory, ignore=[]):
    ignore_files = [".DS_Store"] + ignore
    print(f'+ {directory}')
    for path in sorted(directory.rglob('*')):

        if path not in ignore_files:
            depth = len(path.relative_to(directory).parts)
            spacer = '    ' * depth
            print(f'{spacer}+ {path.name}')
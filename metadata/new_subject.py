import sys
import json
import pathlib
from utils import utils

experiment = sys.argv[1]
subject = sys.argv[2]

# metadata
metadata_folder = utils.get_experiment_folder(experiment)
assert metadata_folder.exists(), f"Experiment metadata folder does not exist: {str(metadata_folder)}"

experiment_metadata = utils.get_experiment_metadata(experiment)
subject_metadata_folder = metadata_folder/subject
assert not (subject_metadata_folder).exists(), f"Subject metadata folder exists: {str(subject_metadata_folder)}"

paths = []
paths.append(subject_metadata_folder)

# data 
base_data_folder = pathlib.Path("/mnt/c/Users/spencer/data/")
experiment_data_folder = base_data_folder / experiment
assert experiment_data_folder.exists(), f"Experiment data folder does not exist: {experiment_data_folder}"
subject_data_folder = experiment_data_folder / subject
assert not subject_data_folder.exists(), f"Experiment data folder exists: {subject_data_folder}"

for task in experiment_metadata["tasks"]:
    paths.append(subject_data_folder / task)

print("Creating:")
for path in paths:
    print(str(path))

response = input("Are these correct [y/n]?")

if response == "y":
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
    metadata = {"name":subject}
    with open(subject_metadata_folder/"metadata.json","w") as fp:
        json.dump(metadata, fp)
# kyberphysics

When we talk about human ability, we often use theory and experimental results from *psychophysics*, the formalization of perception and sensation in the language of physics.

Here, we are interested in the inverse: developing an understanding of action, control, and learning in the language of physics. We call this *kyberphysics*.

The word **kyber** is Greek for governance, control, or steering and **physics** is the study of information and dynamics.

## how to run this code

Everything should be done from the top-level direction `kyberphysics`.

The first step is to create or activate a conda environment, and make sure it's updated with what's in `requirements.txt`.

Next, install the `kyberphysics` package locally with `pip install .` while inside your conda environment.

Now, let's say we're going to begin a new experiment. To do this, you must run `python3 -m metadata.new_subject <experiment name> <subject name>` with your new experiment and subject name. This will ask you to create some files. If the filepaths look correct, enter `y`. 

Now you want to run one of the tasks. With the bonsai version of that task running (from `workflows`), use `python3 -m <tasks.<task name> <experiment name> <subject name>` with your experiment and subject to launch the python side of the setup. If the amplifier is turned on and connected, you should see "Ready to begin recording" at which point press enter and you're running.

## how to use notebooks

Notebooks should work fine if you open them from the top-level directory.

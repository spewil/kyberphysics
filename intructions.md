# instructions for experimenter

## troubleshooting 

### dropped samples

always watch the 68th channel for dropped data-- you'll know samples are being dropped if the 68th channel deviates from a ramp between 0 and 65356. In the case of dropped samples it helps to close all other applications and to make sure the bonsai window is active. More than a few occasional drops will result in noticeable lag for the participant. It helps to not have any other visualizations running in bonsai simultaneously. I only have the ramping signal open after checking the signal for noise.

### line noise:

- check that electrodes are making contact. often the participant has shifted their arm and electrodes are lifting
- check that the band fits snugly on the arm. add velcro or the bandage in case it's needed to get good contact
- check that cables are bent or stretched
- check the "ground" cable connecting participants to the metal box

### if anything goes wrong

- stop bonsai first! then the terminal


### creating a new subject

to create a new subject, run `python3 -m metadata.new_subject <experiment_name> <subject_name>` and follow the prompts

### running tasks

#### natural movements & calibration bars

- make sure you're connected to the device via wifi (Sessantaquattro)
- start the bonsai workflow
- run `python3 -m tasks.<task_name> <experiment_name> <subject_name>` (I tend to run this in a dedicated terminal, only tested in WSL)
- in the python terminal, wait for the `Initialized.` response
- if you don't get this, make sure you're connected to the device! otherwise restart everything

once things are running:
- pull up the ramp signal to check for drops
- pull up all 64 channels of the EMG to check for line noise (sinusoidal corruption)
	- I usually make the window +/- 200 y scale, any line noise that isn't visibly noticeable here isn't worth adjusting for.

hit enter from the terminal to start running the task

Repeat the natural movements task with the same set of instructions.

After this run the calibration bars experiment twice, using the bonsai `calibration_bars.bonsai` workflow
`python3 -m tasks.calibration_bars <experiment_name> <subject_name>` 

#### center hold

1. compute and save the modes: 

- run the notebook `mappings.ipynb` making sure to change the `subject` and `experiment` variables appropriately
- visually inspect the modes and the test plot, if the test plot looks one-sided, change the order of the modes

2. changing the offset parameters: 

- in bonsai, click "Create Window" node
- change "DisplayDevice" to "First" and "WindowState" to "Normal" (put the task on your screen so the participant can't see it)
- start the task running in the usual way (start bonsai, then python)
- instruct the subject to move randomly, then relaxing their hand, arm, shoulder, posture
- while they are relaxing, visualize the "UpdateCursor" node (Trials > CreateTrial) and change the OffsetX and OffsetY values to zero these values (it will fluctuate, I try to aim for as close to 0.00xx as possible)
- visually confirm the dot is in the center
- stop bonsai, stop python
- change the DisplayDevice and WindowState back to "Second" and "Fullscreen" (put the task back on the subject's screen)
- delete the session of data you just recorded while setting the offset parameters (data/subject/center_hold/session_0)

start the task normally, checking the signal and the counter channel


# instructions for participants 

the goal here is to do two things:
- clearly and succintly explain the "object" or cost function of the task
- clearly and succintly explain the structure of the task, what a trial is and how long trials last

things that help:
- hand gestures
- a kind tone
- saying ready (yes), set, go

notes:
- ask if it makes sense, if they have any questions
- say "i can't say" if questions or clarification of the task drifts into strategy, etc 

## natural movements

the name of each movement will come up on the screen
wait until the green cue appears to initiate the movement, then make the movement and hold until the green cue goes away
the green cue will appear three times per movement, each time for one second
the movements are in order [list and demonstrate each movement]
NB: subjects confuse wrist in and out with wrist up and down-- make this clear. "In" is towards you and "out" is away from you.
we will do this task twice

## calibration bars

this is an "exploration" and "isolation" task
you will see 63 vertical white bars and 1 red bar on the screen
object of the task is to explore your movements to activate the red bar (increase its height) without activating the white bars (increase their heights) by isolating the red bar from the white bars
it's important that you try your best every trial so we get a picture of your capability
you are not necessarily "good" or "bad" at the task, it's most important that you try your best each trial
it is more important here to isolate than to activate (less total activity is better)
**any movement can be used to complete the task** -- forget about the natural movements you did before, any movement is on the table in this task
we will repeat this task two times in total

## center hold

white circle will appear
rest until your blue cursor is hidden by the white dot
once youre at rest, the white circle will disappear and a red target will appear
you have a short amount of time to move to the target, 
this completes one trial
we will complete three sessions with short breaks in between
if you have trouble holding, this is most likely due to posture adjustment
make sure you are in a totally comfortable rest position now for the parameter settings
make sure to relax your hand, arm, and shoulder fully
if you have trouble holding, try a postural adjustment first
if you feel that you cannot return the blue circle to the center, let me know and i will jump in and fix it
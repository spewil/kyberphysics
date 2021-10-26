# instructions for experimenter

## general 

always watch the 65th channel for dropped data-- in the case of dropped samples it helps to close all other applications and to make sure the bonsai window is active

to create a new subject, run `python3 -m metadata.new_subject <experiment_name> <subject_name>` and follow the prompt

to run each task, run the bonsai workflow first, then run `python3 -m tasks.<task_name> <experiment_name> <subject_name>` 


## natural movements

- start the bonsai
- start the python
- check the counter (channel 68 of EMG) is counting without drops

## calibration bars

- start the bonsai
- start the python
- check the counter (channel 68 of EMG) is counting without drops

## center hold

run the notebook `mappings.ipynb` making sure to change the `subject` and `experiment` variables appropriately
visually inspect the modes and the test plot, if the test plot looks one-sided, change the order of the modes

in bonsai click "Create Window" node
change "DisplayDevice" to "First" and "WindowState" to "Normal"
start the task in the usual way
instruct the subject to move randomly, then relax
while they are relaxing, visualize the "UpdateCursor" node (Trials > CreateTrial) and change the OffsetX and OffsetY values to zero these values (it will fluctuate, I try to aim for as close to 0.00xx as possible)

# intructions for participants 

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
any movement can be used to complete the task
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
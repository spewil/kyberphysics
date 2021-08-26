# 8_26_21
## second self test
filtering is better, scaling needs work
calibration bars outside of box, then took sleeve off


## miranda

# 8_25_21

first self test
using wrong decoder
filtering/scaling is horrible
check this for data sanity, etc
how to visualize "space" of activations?
# 3/6/21

starting recordings again:

- enter subject details
- finger calibration
- pick up filenames for calibration
- compute NMF features
- visually inspect features
- store weights as decoder 64x4 (up.down,left,right)
 

## TODO

- finish FakeEMG for testing 
- finish rescale channels
	- defer input == load scaling n-array, 1 element per channel
	- main input == nxb matrix to be scaled
	- tile the scaling array from nx1 to nxb to use CV.Divide

- figure out channel mapping from arm to force directions

- fix filenames / messages for center hold task

--- 

bonsai notes
- buffer node with skip one is a true sliding window even if signal comes in buffers already
if count > incoming
- to make a workflow editable, group it as workflow
- to save it for use elswhere, save as workflow and overwrite
- delete and replace in other workflows

- externalized property + workflow output = outer level properties


--- 

data notes

calibration
- makes one csv and one bin file
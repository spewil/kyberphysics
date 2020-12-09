## TODO

- finish FakeEMG for testing 
- finish rescale channels
	- defer input == load scaling n-array, 1 element per channel
	- main input == nxb matrix to be scaled
	- tile the scaling array from nx1 to nxb to use CV.Divide

- figure out channel mapping from arm to force directions

- fix filenames / messages for center hold task


- andy 7/12/20 -- fix data folders into 2 and 3 

--- 

bonsai notes
- buffer node with skip one is a true sliding window even if signal comes in buffers already
if count > incoming
- to make a workflow editable, group it as workflow
- to save it for use elswhere, save as workflow and overwrite
- delete and replace in other workflows

- externalized property + workflow output = outer level properties
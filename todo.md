todo

- average over channel 56

- calibration task
	- fix ITI blanking X 
	- check recording raw EMG X
	- record filtered EMG X
	- break filtering into reusable workflow? X
	- NB: recording EMG as int32 and bar_heights as float32
	- filenames sent by python?

- offline decoder
	- pick up correct files
	- dim reduce
	- test?

- 2D task
	- tinker with circle aesthetics
	- use filtering module
	- fix dynamics of the dot
	- record raw
	- record filtered
	- record dot x,y 
	- trial structure

- decouple recording params from task params
- make task params per-trial, send decoder
- start emg, push go, trials begin, ITI sleep
- save behavior result, behavior trajectory, rawEMG, filteredEMG, decodedEMG

python
- modularize running tasks, sessions, trials


debugging inexact frame count for calibration data saving
- not dropped frames (logevent bar height buffers in excel = no drops)
- add a weight to have the barheights setup
- extra frame in the visualized recording is likely at the end, effect of display swap timing
- still plus or minus one frame, must be timer firing relative to buffer swap? syncing makes this worse

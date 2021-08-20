0. enter subject details, arrange filepaths appropriately
	- make a data folder for each subject, with experimental notes
	- make subject info json (to be picked up by python later)
1. clean and prep arm
2. attach electrodes at a fixed position
	- measure arm at ulnar styloid
	- measure arm 5cm from elbow tip
	- where to place band?
3. set up arm in enclosure, attach ground
4. test recording
	- **validation: visual inspection of data**
		- noise
		- electrode liftoff / seating
	- in case of issues, adjust sleeve etc. accordingly
	- **validation: check filepaths, etc**
5. explain calibration protocol
	- first, total relaxation of the hand
		- experimenter guides subject through this
	- you will be asked to perform a series of movements:
		- see "movements.txt"
	- once the subject is ready, the calibration (rest + movements) is done 3 times
6. scripts are run to produce modes and choose decoder
	- **validation: modes are visually inspected**
		- if an error is seen, calibration is repeated
	- if modes look reasonable, continue to task
7. explain task to subject
	- you will be asked to move a dot to target locations on the screen using muscles controlling your hand movements. first you must hold the dot in the center of the screen for a required time, after which a trial will begin. each trial you will attempt to move the dot towards the target and hold it there for a desired time. if you are successful, a new trial will begin. if you run out of time, a new trial will begin.
	- run task for desired number of trials for a range of targets.
		- after each run, briefly interview the subject about discomfort, feeling, strategies, glaring errors (only doing one movement), etc.

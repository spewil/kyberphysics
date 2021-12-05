UCL guidelines:
introduction and context
lit review
research question and hypothesis
methodology
substantial work towards objectives
plan for remainder
bibliography

TODO:
- timebox each section
- combine all writing into here from overleaf


# intro & aims 
- what are we interested in?
  - why can't robots move like humans?
  - What is special about human movement?
  - why is this the most interesting problem?
- how are we going to approach this interest?
- what do we hope to achieve?
  	- experiments with interesting and novel movement data
	- analysis of muscle and behavioral data
	- inject RL / control theory into skill acquisition
		- what do we mean by "RL" here?
		- is "RL" relevant? why?
- What is motor learning vs. motor control?
- claim about control needing an extension for learning
- use RL concepts to analyze motor learning experiments
- can we defend this use of RL for learning?
- what do we mean by "RL" here?
- substance
- short summary of exactly what we're doing
- what is our approach?
- develop models of ...
  


# human motor physiology
 engineering problem for movement 
	- what can physiology tell us about the movement problem?
		- can it inform theory to describe motor solutions?
		- this will inform the shape our models
		- the constraints of our tasks, questions
	- **what do we know about brain and motor?**
		- graziano
		- synergies, bizzi
		- hands, cm connections
	- **why hands?**
		- from muscles to cortex
		- basic CSN circuits
		- spinal circuits
		- motor cortex
		- corticomotoneuronal connections
		- muscles, recruitment curves
		- graziano experiments
		- synergies
			- multiple definitions
			- bizzi, mussa-ivaldi
	- **how does what we know inform experiment?**
		- **things are very different depending on system, behavior**
		- hands (and maybe cortex) evolved to be flexible-- how is this achieved?
	- how does this inform theory?


# what has been done experimentally?
experimental methods
prior work on human motor control and learning (doesn't have to be long!)
	- what theory doesn't exist?
		- we have control, but not really learning?
	- what are the most important concepts / results that inform our experiments?
	- classic reaching adaptation --> this is a different goal
		- shadmehr
		- krakauer
	- unperturbed movements
		- van beers
	- skill learning tasks
		- ball and cup / kendama
		- throwing tasks
	- skill learning via BMI work using EMG, key findings
		- Mosier remapping experiments
		- Berger
		- Radakrishnan
		- de Rugy
	- cortical BMI work
		- Batista papers, lee miller papers
	- speech learning -- analogy to speech
	- bird vocal learning


# what experiments do we need to do?
experimental setup
i made a thing, it works like this, here's the data
	- detail how this works
	--> what are the constraints?
	--> what perturbations can be achieved?
	- prelim data from the rig
		- figures of this data
		- thoughts about how versions of the task
	- hardware
		- recording 64 channels of EMG from multiple muscles the arm and hand with realtime feedback
		- in an isometric learning task
	- software
pictures n stuff

# preliminary data & discussion

- andy data

# theory (3 days)

- what theory doesn't exist?
- we have control, but not really learning?

1 day
existing error learning models
existing control model (OFC) 

1 day
fancier control models for Composition
how does this relate?

1 day
fancy learning models for selection

what models do we have to describe these experiments?
we need these models to test our hypotheses from our experiment

	- problem formalization (of our setup)

		- what is happening in this task with this rig?
			- learning?
				- different kinds of learning
			- control?
				- definitions of control

		- system ID
			- we should be able to describe what the optimal data collection strategy should be for a person faced with learning an entirely new set of dynamics in this virtual environment -- what is the model-learner optimizing for and how does it relate to the task?
			- is this a regression problem for x' = f(x)? what dataset x (and thus what action set u) is optimal to solve this regression problem?
			- can we use trial-to-trial dynamics of the learner's errors in the task to determine how this model acquisition proceeds?
		- learning primitives
			- this problem, if it is one, is more like the adaptation of a reach (in the case of a single target goal)
			- this might be framed by the adapting of certain gains for pre-existing primitive movements, but this depends on the muscle-to-force mapping
		- constructing composite movements

	we know about control, but we don't have models of learning
		but is it actually learning? RL type learning
		or is it more like composition/selection?
		we need to look at the data to know?

	- goal is to describe + predict motor output
		- models to test hypotheses
	- is this learning or is it a selection / composition process?

models
	- coded up LQR -- the stock model(?)
		- discussion of the rig model with reference to the LQR model
			- noise models
			- dynamics
		- discussion of varying different constants in the rig and model to test model hypothesis?
			- hypothesis: LQR is a good model for this experimental setup
			- for basic tasks?

	- coded up compositional LQR
		- KL version
		- selection version
		- discuss how these might predict behavior?


# next steps

our own selection model
the idea behind it

our OFC extension
idea behind that

some analysis of APT data
	- this shows what our task needs relative to this "skilled execution" task
	- compare this task our suite of tasks
	--> does reward impact behavior in these tasks?
	--> is "RL" the right framework?
		- if they're doing something else, what is that?
		- adaptive control? -- flesh this out

actual next steps
	- collect more data
	- test different types of tasks to narrow down phenomena
	- run more simulations
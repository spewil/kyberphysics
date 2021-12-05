## 6/3/20

things to be addressed
- dropping frames during recording
- noise in recordings
- adding eyetracking into the mix
- recording the data in a stable way
  - regardless of task
- 

## 21/11/20

wolpert 2011:
- what has to be learned
- how it is learned
- how knowledge developed during learning is represented

- state estimation -- given a model, use sensor data to infer latent state (minimize error)
- control -- given a model, compute controls given state (minimize cost)

- error-based adaptation -- use error from prediction under internal model to adjust

- reward-based learning -- value functions

- how do you learn feedback controllers? using internal models, reward, and sensory errors
	- do these learned controllers generalize to new parts of the workspace / to new tasks?
	- do the

## 2/9/20

for each trajectory, (x_t - R)/R is a kind of spatially normalized data.

the autocorrelation tells us how similar observations are as a function of the timelag between them
- do earlier observations correlate with later ones?
- over what timescale do earlier observations predict later ones?
- how does this measure of time-correlations relate to a planning horizon?

The question with each trajectory is-- are they random walks? What is the time-correlation horizon?
	- if the horizon is long, my early choices will affect my later choices -- more like a feedforward process?
	- if short, then I'm just accumulating noise... -- more like a feedback process?

spurious correlations:
https://stats.stackexchange.com/questions/133155/how-to-use-pearson-correlation-correctly-with-time-series

## notes 1/9/20

rig:
hardware electrodes
hardware frame
python
bonsai

write up:
one step back plot breakdown (decision probability vs past trial reward + state)
	- probability of current decision -- some aspect of the control problem?
		- should this be 1D? could it be something about the control policy?
		- this should reflect some choice that is model-based or model-free
			- the choice of variance?
		- model-free would reinforce aspects of the trajectory/policy based on features that were rewarded
		- model-based would alter future trajectories based on whether the planned trajectory (the intended control) matched the actual sample-- do the statistics of the planned control match the actual trajectory statistics?
			- if the planner is optimal under a certain model, but the resulting trajectory is suboptimal, the model should change...
		- on one hand (mf), the reward is known but the control isn't-- control features (and the resulting trajectory features) should be reinforced if successful
			- features of the last trajectory are repeated if successful
				- what features?
			- this should learn "biases" in the trajectories, simply reinforcement what happens before (higher "stick" if rewarded)
		- on the other hand (mb), the outcome is known, the planner (controller) should be altered such that the simulation is successful -- close the mismatch between successful simulation and successful outcome -- keep the controller but change the model?
			- how does this predict how the resulting trajectory would change?
				- maybe the "strategy" stays the same, but the gains are tuned?
				- maybe we'll see model-free first (big changes), then tweak the strategy with model-based?
				- if an outlier trajectory is rewarded, it won't be immediately reinforced
			- the mb learner wants to be able to predict the world, then it can make optimal plans for whatever goal it has
				- we would readily correct trajectories that misaligned with our plans
			- if outlier trajectory features are rewarded, these features will stick
	- is there a "first stage" and "second stage" in trajectories?
		- the "transition structure" of movement is already known, but it's parameters aren't tuned. the mb learner should adapt these gains push the planning horizon further into the future? perhaps time-correlations in trajectories stand in for transitions -- if early movement / choices correlate with success, less corrections later?
		- if you're a better predictor, reward should lead to you making more "risky" predictions, your confidence in your predictive power should go up? so this means you should stick to the plan...
			- make less submovements / corrections?
			- variability should go down
			- uniformity in momentum / velocity
			- statistically maybe trajectories should actually be more variable (less stereotyped) than mf, but maintain reward-- trajectory distribution should maxEnt in the reward zone (you can explore in your trust region?)
	- some combination of the autocorrelation in time, and the probability / variance of the past/current trajectory in its trajectory distribution


apt data features that can be plotted, extracted
	- aspects of each trial
		- time taken
		- within time
		- within limits (success)
		- variability? in radii,
	- each trial has a distribution of radii
	- each trial is a sample from a trajectory distribution (super high dimensional)
		- could try to fit this, but it would be super sparse
		- can we try to dimensionality reduce this thing? for what end?

apt optimal control model fitting steps, alternative models
what questions model parameters can answer?
- the action an agent takes is the trajectory under study, which can also be said to be the noisy result of an optimal control law

- for a task that is well described by a quadratic cost function, do subjects move optimally?
- if a cost function isn't readily available under the quadratic assumption, under what approximate performance criterion are subjects optimal?
- how (over what trajectory) do subjects achieve this optimality "from scratch"? can we produce a principle that predicts/recovers this optimality?
- what information from each trial can be used to predict structural changes in the control strategy?

## one-step back signatures

- expected signatures of model-based and model-free learning
- expected signatures from SR / something in between?
- signatures from the data?

todo:
- what is the appropriate (quadratic) cost function for this task?


## goal

- what are computers really bad at? moving
- what are computers really good at? simulating stuff
- how do computers work more like neural machines, where programs change over time?
- how do humans decide to change their programs?
	- reward
	- cost
- learn something about how humans update their movements in time
	- before production a goal-directed trajectory (planning, action selection)
	- during execution of a goal-directed trajectory (feedback control)
	- across goal-directed trajectories (learning)

## APT 2012 dataset

- what costs are optimized in the performance of trajectories? (control)
- what features of individual trajectories predict/explain changes in subsequent trajectories (learning)
- are these trial-level changes based on a model-based or model-free
	- does the path of the trajectory distribution distinguish these two alternatives?
	- what model can be fit for each strategy?

## high-level

design, implement, and execute a project so that I can find support to repeat the cycle


## precision neural coding

thought through from discussions with goncalo, sent to latham for input

We often read about the brain being “corrupted” by noise, Poisson spiking statistics, having to “overcome” inherent noisiness to reach abstract goals. I’m curious if there are any results suggesting that in fact that spiking statistics reflect optimal coding, in the sense that in order to represent and produce reliable behaviour, the brain needs to both optimally compress incoming percepts and take actions with optimal precision depending on the task.

You could imagine an experiment where you record from a single neuron and play in a low-dimensional stimulus such as a sine wave / Gabor grating in one trial and naturalistic noise in another trial. Over trials, which stimulus produces more reliable firing?

For my stuff (motor control / learning), it appears to me that the hottest new thing (geometric invariants in population codes simply reflect the correlations in behaviour. The neural code isn’t noisy because of internal variation so much as it reflects the optimal level of variation given the task at hand.

For instance, a recent result shows that humans can identify stimuli at the level of single fingerprint ridges, and other results show that humans can learn to produce reliable spike times both at the muscle and in cortex if given the right feedback.

Most likely this is all known and I spend my time working and reading about behaviour-level models rather than neuron-level models but I would be interested to know what you think about this idea that we can assume the code is optimal given the task at hand, the reason we see a noisy code with different spatiotemporal scales of covariance simply reflects the correlations of one’s environment. What does this mean for brain computation? It might mean that what matters more than neural data is precise understanding and control over a behaving agent’s environment...


## van gelder ""

the centrifugal governor is not a homuncular system. It has parts, to be sure, and its overall be- havior is the direct result of the organized interaction of those parts. The difference is that those parts are not modules interacting by com- munication; they are not like little bureaucratic agents passing repre- sentations among themselves as the system achieves the overall task

As an account of the actual decisions people reach, however, classical utility theory is seriously flawed; human subjects typically deviate from its recommendations in a variety of ways. As a result, many theories incorporating variations on the classical core have been developed, typically relaxing certain of its standard assumptions, with varying degrees of success in matching actual human choice behavior. Nevertheless, virtually all such theories remain subject to some further drawbacks:

(1) They do not incorporate any account of the underlying motivations that give rise to the utility that an object or outcome holds at a given time.
(2) They conceive of the utilities themselves as static values, and can offer no good account of how and why they might change over time, and why preferences are often inconsistent and in- constant.
(3) They offer no serious account of the deliberation process, with its attendant vacillations, inconsistencies, and distress; and they have nothing to say about the relationships that have been uncovered be- tween time spent deliberating and the choices eventually made

What kind of model of decision-making behavior we would get if, rather, we took the centrifugal governor as a prototype? It would be a model with a relatively small number of continuous variables influencing each other in real time. It would be governed by nonlinear differential equations. And it would be a model in which the agent and the choice environment, like the governor and the engine, are tightly interlocked.

In this approach, decision making is better thought of as the behavior of an agent under the influence of the pushes and pulls that emanate from desirable out- comes, undesirable outcomes, and internal desires and motivations; in a quasi-gravitational way, these forces act on the agent with strength varying as a function of distance.

**Computational systems** are abstract state-dependent systems whose states are constituted in part by configurations of symbol types, whose time set is the integers (or some equivalent set), and whose rule of evolution specifies sequences of such configurations. Note that a computation, from this perspective, is a sequence of transitions from one total state of the computational system to another; or, in other words, a matter of touring the system's symbolic state space.

Because differential equations involve derivatives, they presuppose continuity; hence the "time" set in an abstract dynamical system is standardly R the real numbers. Rather than configurations of tokens of symbol types, the concrete dynamical system is made up of quantities changing in a way that corresponds to the numerical sequences specified by the rule of evolution. The dynamical hypothesis in cognitive science, then, is the exact counterpart to the computational hypothesis: cognitive systems such as people are dynamical systems in the sense just laid out, and cognition is state-space evolution in such systems. Alternatively, dynamicists are committed to the claim that the best model of any given cognitive process will turn out to be drawn from the dynamical sub- category of state-dependent systems.

**Note that because the cognitive system traffics only in symbolic representations, the human body and the physical environment can be dropped from consideration; it is possible to study the cognitive system as an autonomous, bodiless, and worldless system whose function is to transform input representations into output representations.**

The core dynamical hypothesis-that the best models of any given cognitive process will specify sequences, not of configurations of symbol types, but rather of numerical states-goes hand in hand with a conception of cognitive systems not as devices that transform symbolic inputs into symbolic outputs but rather as complexes of continuous, simultaneous, and mutually determining change, for which the tools of dynamical modeling and dynamical systems theory are most appropriate. In this vision, the cognitive system is not just the encapsulated brain; rather, since the nervous system, body, and environment are all constantly changing and simultaneously influencing each other, the true cognitive system is a single unified system embracing all three. The cognitive system does not interact with the body and the external world by means of the occasional static symbolic inputs and outputs; rather, interaction between the inner and the outer is best thought of as a matter of coupling, such that both sets of processes continually influencing each other's direction of change.

It is clear that nonlinear dynamical systems can not only match but exceed the complexity of behavior of standard computational systems such as Turing machines.

For current purposes, one of the most important anti-Cartesian movements is the one spearheaded by Gilbert Ryle in Anglo- American philosophy and Martin Heidegger in "continental" philos- ophy.28 Its target has been the generically Cartesian idea that mind is an inner realm of representations and processes, and that mind con- ceived this way is the causal underpinning of our intelligent behav- ior. This movement comprises at least three major components, all intimately interrelated. The first is a relocating of mind. The Cartesian tradition is mistaken in supposing that mind is an inner entity of any kind, whether mind-stuff, brain states, or whatever. Ontologically, mind is much more a matter of what we do within en- vironmental and social possibilities and bounds. Twentieth-century anti-Cartesianism thus draws much of mind out, and in particular outside the skull. The second component is a reconceiving of our fundamental relationship to the world around us. In the Cartesian framework, the basic stance of mind toward the world is one of rep- resenting and thinking about it, with occasional, peripheral, causal interaction via perception and action. It has been known since Bishop Berkeley that this framework had fundamental epistemologi- cal problems. It has been a more recent achievement to show that es- caping these epistemological problems means reconceiving the human agent as essentially embedded in, and skillfully coping with, a changing world; and that representing and thinking about the world is secondary to and dependent upon such embeddedness.29 The third component is an attack on the supposition that the kind of be- haviors we exhibit (such that we are embedded in our world and can be said to have minds) could ever be causally explained utilizing only the generically Cartesian resources of representations, rules, procedures, algorithms, and so on. A fundamental Cartesian mistake is, as Ryle variously put it, to suppose that practice is accounted for by theory; that knowledge how is explained in terms of knowledge that; or that skill is a matter of thought. That is, not only is mind not to be found wholly inside the skull; cognition, the inner causal un- derpinning of mind, is not to be explained in terms of the basic enti- ties of the Cartesian conception of mind.

*The skill is not "in" the mind -- it is the dynamics of performing the skill from brain to muscle*

**The post-Cartesian conception rejects the model of mind as an atemporal representer and, like the dynamical approach to cognition, emphasizes instead the ongoing, real-time interaction of the situated agent with a changing world. The post- Cartesian agent is essentially temporal, since its most basic relationship to the world is one of skillful coping; the dynamical framework is a therefore natural choice since it builds time in right from the very start. The post-Cartesian agent manages to cope with the world without necessarily representing it; a dynamical approach suggests how this might be possible by showing how the internal operation of a system interacting with an external world can be so subtle and complex as to defy description in representational terms-how, in other words, how cognition can transcend representation.**


## computation

what we're interested in is the forms of computation necessary to plan and generate coordinated actions. specifically, how can these plans and their execution be computed efficiently. what kind of structure is needed and what is the nature of the computation controlling flexible coordinated action?


## law of effect

In 1898, Thorndike proposed the law of effect, which states that the association between some action (R) and some environmental condition (S) is enhanced when the action is followed by a satisfying outcome (O). For instance, if an infant moves his right hand and left leg in just the right way, he can perform a crawling motion, thereby producing the satisfying outcome of increasing his mobility. (wiki motor skill)

## coordination

Each motor neuron in the body innervates one or more muscle cells, and together these cells form what is known as a motor unit. For a person to perform even the simplest motor task, the activity of thousands of these motor units must be coordinated. It appears that the body handles this challenge by organizing motor units into modules of units whose activity is correlated. (wiki motor learning)

Bernstein proposed that individuals learn coordination first by restricting the degrees of freedom that they use. By controlling only a limited set of degrees of freedom, this enables the learner to simplify the dynamics of the body parts involved and the range of movement options. Once the individual has gained some proficiency, these restrictions can be relaxed so allowing them to use the full potential of their body (wiki motor coordination)

## learning v. adaptation

Motor learning is "relatively permanent", as the capability to respond appropriately is acquired and retained. Temporary gains in performance during practice or in response to some perturbation are often termed motor adaptation, a transient form of learning. (wiki motor learning)


## complexity
- perhaps "rare" events drive learning?
- events, or insights, that are critical for model shifts?
	- we should be able to track the points at which people's policy's change abruptly
	- how can we track this within a trial?

## flexibility

- primitives that can be reused make a system flexible
- contextual use of primitives

emo studied state of the art control literature, saw connections, and built models for control. what i need to do is follow that line, study his work to death, and shoot for the same thing with regard to learning. it took him 5 years to do the phd, nature paper took another 4. slow and steady, and take good notes. we take what we know from the learning literature and adapt it as a conceptual framework for understanding motor learning-- we "teach" the field something new, a new way to think about the problem of redundancy, equivalence, etc -- we try to understand how we might reconcile this with mouse work as well as more human cognitive work about planning, etc. humans are good at motor control, perhaps, because we have really good models to work with and we're really good at online optimization/replanning/simulation. can we prove/show this in a new skill?

## physiology experts
Marc H. Schieber (Univ. Rochester)
Fugelvand (Arizona)

## todo

- read this document, organize / edit

## to read
- lemon review
- hand anatomy
- hand knob
- yang cowen haith
- franklin multirate models
- VAE sussillo task

## compositionality

- our hypothesis is that the motor system solves the redundancy problem in a task-specific way by optimizing a policy for that task which is based on prior task-specific learning. Thus, the motor system leverages task-specific

## wolpert talk

overthrow the two-rate model:
	- spontaneous recovery doesn't fit with two-rate model
	- savings over days doesn't fit either
what else doesn't fit with this model, which is actually meaningful for understanding motor learning at a deep level?


> "The motor learning field does not yet possess an adequate computational model for practice-induced increases in motor acuity. The models discussed in other parts of this review instead speak to how an average movement is converged upon and properly selected. They do not address how execution of the selected action then improves with subsequent practice." (Krakauer 2019)

> "Although it is unclear exactly how de novo tasks are learned, there is likely to be a substantial cognitive component. The control solution that participants acquire depends strongly on the type of visual feedback they are provided. If participants are shown only a cursor moving on a screen, they learn to move the cursor along straight lines on the screen (304). If, by contrast, the cursor is represented as the endpoint of a simple two-link arm, participants learn to move the cursor in a way that minimizes distance in terms of the changes in joint angles of the two-link arm, despite the fact that the mapping between hand posture and the cursor is identical in either case (76). Thus, the control solution that participants arrive at depends critically on how they cognitively conceive the task." (Krakauer 2019)

**** there is evidence that fast, slow != explicit, implicit 1:1.

## Implicit learning is too fast to be a slow process (Ruttle 2020)

> The two-rate model fits visuomotor adaptation data excellently. We suggest here that the conventionally implicit components of motor learning; changes in estimates of hand location, and no-cursor reach deviations, do not follow the pattern of the two-rate model’s slow process, nor indeed the fast process. The fast emergence of reach aftereffects and changes in hand estimates indicate implicit components of motor learning appear before or alongside explicit components of learning. Perhaps implicit processes lead or drive motor learning, unlike previously believed, but certainly they do not lag behind explicit processes.

*visual-proprioceptive discrepancy error drives implicit learning, while explicit is something like a strategy, a planned bias*

**** many result based on self-reporting, which we'd like to stay away from?

## Implicit / Explicit

limiting preparation time isolates a single learning process, which is likely related to the implicit process measured through explicit aiming reports

**** time is a key component of teasing out explicit cognitive strategies and implicit learning

## Internal Models

> Theory suggests that learning of a forward model, as a form of supervised learning, should be guided by the errors in its output. The output of a forward model is a prediction about the sensory consequences of a movement, and thus the appropriate error signal to update a forward model is a sensory prediction error: the difference between where you

> It is important to note that optimal control can only be ‘optimal’ if the internal models are accurate. That is, we cannot hope to maximize reward unless our predictions about the behavior of our body generally agree with the sensory feedback (otherwise, the predictions would bias observations). Therefore, a strong implication of the OFC theory is that building internal models (a process called system identification) must go hand-in-hand with the process of optimization. This is an interesting prediction that to our knowledge has not been tested. (Shadmehr, Krakauer Comp Neuroanatomy)

> Unfortunately, we cannot make optimized movements unless we have an accurate set of constraint equations, i.e., an accurate internal model. When we see a sub- optimum movement, can we dissociate the effects of an inaccurate internal model from effects of an inaccurate cost function? (Shadmehr Comp Neuroanatomy)

## Variability

> Motor variability in a reaching task increases following unsuccessful movements (335, 437), suggesting that variability can be flexible: if the same movement has repeatedly led to more success than other movements, the motor system can exploit this by trying to produce as similar a movement as possible on the next trial, reducing variability; by contrast, if a given movement is unsuccessful, the motor system can increase variability to explore for more successful ones in the next attempt. (Krakauer review)

> movement variability is partially a form of exploration driven by the recent history of rewards (shadmehr 2015 Reward-Dependent Modulation of Movement Variability)

> Improved performance at the task level was mainly attributable to reductions in trial-to-trial trajectory variability, with minimal changes in the mean. The term “motor acuity” was coined to capture this reduction in movement variability. (krakauer review)

**** what would we predict about motor variability in task space and motor space?

## Planning

> Planning refers to the process of generating novel control policies internally rather than learning favorable motor outputs from repeated interactions with the environment (Figure 1c). Internal forward modeling on timescales significantly longer than those implemented in state estimation contributes significantly at this point in the sensorimotor control process. Ultimately, once a task has been specified and potential goals identified, the brain needs to generate a complex spatiotemporal sequence of muscle activations. Planning this sequence at the level of muscle activations is computationally intractable due to the curse of dimensionality (123). Specifically, the number of states (or volume, in the case of a continuous control problem) that must be evaluated scales exponentially with the dimensionality of the state space. This issue similarly afflicts the predictive performance of forward dynamic models, where state-space dimensionality is determined by the intricate structure and nonstationarity of the musculoskeletal system and the wider external world. Biological control hierarchies have been described across the spectrum of behavioral paradigms, from movement primitives and synergies in motor control (124) to choice fragments in decision-making (125). From a computational efficiency perspective, these hierarchies allow low-level, partially automated components to be learned separately but also flexibly combined in order to generate broader solutions in a hierarchical fashion, thus economizing control by enabling the nervous system to curtail the number of calculations it needs to make (126). (McNamee ARN)

> OFC relies on state estimation, which itself relies on internal models that are also of general use in a variety of processes and for which there is accumulating behavioral and neurophysiological evidence. (McNamee ARN)

> even given a cost function or goal state specification, fully solving OFC in a reasonable time for a complex system such as a human body is intractable. The brain must use approximations to the optimal solution that are still unknown (McNamee)

## themes / topics
- myocontrol
- reaching
- error-based learning model
- two-rate learning model

goal = krakauer review focused on skill learning + math models of learning

Explicit v. implicit, fast v. slow -- because we have mixed results, we must need a new model?

Similarly for synergies -- because we have mixed results, we must need a new model?

![](../images/motor_system.png)

## papers

todorov - optimal control / oracle control
internal models - dan and dan - how do we learn optimal control?
krakauer big review
grillner -- current principles of motor control
shamdmehr & krakauer -- computational neuroanatomy

### Signal Dependent Noise

Here is a basic internal model with additive noise
$$
\begin{align*}
\hat{x}_{t+1|t} &= \hat{A}\hat{x}_{t|t} + \hat{B}u_t \\
\hat{y} &= \hat{H}\hat{X}_{t+1|t}
\end{align*}
$$

Here is the Kalman state estimation equation

$$
\begin{align*}
\hat{x}_{t+1|t+1} = \hat{x}_{t+1|t} + K_{t+1}(y_{t+1}-\hat{y}_{t+1})
\end{align*}
$$

noise dependent on the magnitude of a signal $\mathbf{u}$

$$
\begin{align*}
C_i &= \begin{bmatrix} \ddots & & 0 \\ & c_i & \\ 0 & & \ddots \end{bmatrix} \\
\phi_i &\sim \mathcal{N}(0,1) \\
\xi_i &= \sum_i{C_i\mathbf{u}\phi_i} =  \begin{bmatrix} \ddots & & 0 \\ & c_iu_i\phi_i & \\ 0 & & \ddots \end{bmatrix} \\
\mathbb{V}ar(\xi_i) &= \sum_i{C_i\mathbf{u}\mathbf{u}^TC_i^T}
\end{align*}
$$


## Probabilistic Motor Control

- forward model (prediction)
- inverse model (output transformation)
- feedback (error correction)

## successor representation

The Successor Representation (SR) of state i predicts the expected future occupancy of all other states if you are currently in state i. That is, if you enumerate your states from 0 to N and started from state i, the jth component of the SR of state i, $\mathbf{x_i}]_j$, would equal the expected (discounted) number of times you would visit state j in future if you are currently in state i.

The value function is the expected discounted cumulated reward if you start from state s and follow a policy \pi. Intuitively, it is the value of being in the state s given your current goal (what rewards you receive). From this, we can see that the SR has the potential to be a reward-independent model learner – it factorises the value function into reward-independent and reward-only components. That is, it learns an implicit model of the environment that is independent of the reward.


## Control Feature Theory

We want to determine a redundant control space from data taken during natural activity. The difficulty with this is that such a natural activity manifold may display spatial (channel-wise) correlations that are possibly physiologically separable. Thus, there are two aims which must be addressed separately:
1. Expore subjects' ability to decorrelate descending output to the muscles which have been shown to be correlated in a natural activity dataset.
    - Such a structured exploration might provide support for the hypothesis that "synergies" are flexible correlations between muscles driven by task demands rather than (or in addition to) physiological structure. This needs to be done incredibly carefully to escape criticism of hard-wired synergy enthusiasts.
    - See *de Rugy 2012* for a critique of OFC and hard-wired synergies
2. Use common correlated outputs to develop a family of BMI-type learning tasks as a proxy for a "novel skill", then track motor planning of this new skill to compare with motor planning algorithms.
    - We might be able to get #1 for free by going after this goal if we're careful in the setup
    - This is arguably a more impactful focus as it connects low-level motor hierarchy data (EMG) to high-level planning with a normative hypothesis.

## OFC

what is the relationship between uncertainty and cost? Is there a way to formalize high cost equating with high/low uncertainty?

## exploratory time series analysis
- indpendent
	- clustering (UMAP)
	- SVD -- spatial basis functions
	- PCA
	- Factor Analysis
- markovian
	- HMM / LDS
- factors

### gaussian processes

gaussian process fitting is good for little data as it resists (catastrophic) overfitting

### rl problem statement

the trajectory distribution

$$
\begin{align*}
p(\tau) &= p(x_0,u_0,x_1,u_1,\dots,u_T,x_T|\theta) \\
&= p(x_0)\Pi_{t=1}^Tp(u_t|x_t,\theta)p(x_{t+1}|x_t,u_t)
\end{align*}
$$

the q function is the optimal cost-to-go for a particular state-control tuple, and the value function is the cost-to-go from a particular state under the optimal control:



In the LQG problem, the estimated latent state is based on the observation:

$$
\begin{align*}
\hat{x}_{t|t} &= \hat{x}_{t|t-1} + K_t(y_t - M\hat{x}_{t|t-1}) \\
&= (I - K_tM)\hat{x}_{t|t-1} + K_ty_t
\end{align*}
$$

where $K$ is the Kalman gain which again depends on the unknown mapping.

## for PCA

use covariance matrix when variance of the original variable is important, and use correlation when it is not.

# info geometry?

Manifold/geometric assumption: functions of interest are smooth with respect to the underlying geometry.

Probabilistic version: conditional distributions P(y|x) are smooth with respect to the marginal P(x).


A trajectory through the space of covariance matrices is a fundamental computation?
https://www.sciencedirect.com/science/article/pii/S0165027013003464

online windowed covariance
https://softwareengineering.stackexchange.com/questions/337617/algorithm-for-windowed-online-covariance

# the problem

most motor learning / adaptation focuses on reaching, and subjects are able to "adapt" within one or a few trials (REF)


# system level

think of the CNS producing motor output as a hierarchical system -- this system is arguably the best we have at responding flexibly to perturbations and acquiring new arbitrary mappings from very little data. What about the structure of the system tells us something about how it is able to achieve these feats? How can the structure of the system drive a theoretical understanding of the algorithms? Can we reverse-engineer this ability by providing a controlled context for the system to explore?


## people who have hand skills

piano / string musicians
eSports
puppeteers

# phrases

"speculative computing"
information processing limits / constraints
human output constraints
constraints on learning at the periphery

# reward hypothesis

all goals can be described by the maximization of expected cumulative reward

# overall tasks

- build a myocontrol rig
- model muscle activity data across a learning task (naive-->expert)
- build an understanding of control algorithms, motor learning, sensorimotor physiology


# tasks

1. guided exploration task
	- wack-a-mole style
	- grid / continuous
	- goal: "color-in" entire space
	- some kernel/brush width
	- you're only exploring the image of the mapping; how can we explore the nullspace?
		- cycle through degrees of freedom?
		- how do you make sure the null space is kept silent?
		- geometric interpretation of the mapping?

2. via-point task
	- analogous to keys in a door
	- goal: connect-the-dots within a time limit
	- easily comparable to OFC models


# constraints
- a very specific outcome from each trial
- continuous feedback, smooth error gradient
- portable to visual/auditory stimulus


# frameworks for thinking about motor learning

krakauer
	implicit/explicit learning
	adaptation v. de novo

models
	- "forward model (sensory prediction error learning)" = make motor command, predict its consequence in task space, adjust forward model due to error in task space. Invert this predictive forward model to find appropriate muscle commands
	- "direct policy" = with desire sensory state, produce motor command via inverting this desired state, change inverse model based on resulting error in task space
	- "feedback error model" = motor feedback signals act as a teacher (Albert & Shadmehr, 2016; Kawato, 1990; Kawato & Gomi, 1992)
	- these seem very similar... maybe different in an open-loop context?



# prior work
- experiment
	- reaching
	- visuomotor rotations
	- mirror prisms
	- myocontrol
- theory
	- multiple exponential rate models
	- LDS learning model
	- LQG controllers
	- policy gradient

# skepticism

Holder's skepticism is annoying but good to face early on.
- Why are we using EMG? What does EMG help us answer that couldn't be answered with motion tracking or similar?
- What is our hypothesis? What is our prediction?

General answers:
- Why record from the brain when the behavior isn't interesting? By interesting here, I mean a problem that is difficult for a subject to learn such that we can prolong the learning process in order to dissect it more carefully.
- We want to craft a very deliberate learning environment based off muscle activity directly so that we can build a learning problem that is unlike anything you've ever learned before. We want to return you to an infant state and watch how you cope with this novel environment. Using tracking or similar would bias you to have already solved a large part of the redundancy problem.
- We simply don't know what people are capable of learning with respect to (decorrelated, orthogonalized) motor outputs.

# data collection

new subject comes in

semi-anatomical placement for maximum muscle capture

aligned photo for subsequent placement over trials

scanning of the arm for fixture creation
OR
adjustment of fixture for subject-specific arm shape

test protocol -- colored grid, try to match patterns
	demo this with force pad?



# modeling

If we're trying to model a planning problem with hierarchy (a hard control problem), then we might want to use a policy gradient method.

If we're modeling a reach, this is probably overkill because our inherent policies are already pretty much optimal, so we just need to compare the optimal solution to the expert data.

What is a good, continuous task that contains hierarchy?


# Proposal Notes

## Outline
Main goal/question
	- the human motor system has evolved to enable fine manipulation of objects as seen in our use of a range of tools, while remaining adaptive to flexibly accommodate a changing environment full of unpredictable perturbations. This combination of learned predictive processing and flexible responsiveness to uncertainty is the hallmark of the human motor system. In order to robustly achieve such a wide set of goals to a high degree, what approximations are used to quickly adapt to new situations?
Physiological underpinnings
Modeling prior work
Task setup / data shape

## Active Sensing
- Hierarchical Bayesian models -- what does this actually look like…?
- Information theoretic constraints -- how are these formalized? (maybe see Braun’s work)
- Could this lead to characterizing some information theoretic constraints on how we can learn new skills? How we use strategies to cope with this limitations?
- What strategies are used for learning, and how do they relate to the statistical structure of the task?

## Adversarial Mappings

- What sensorimotor mappings are nontrivially unlearnable? (Where trivially unlearnable would mean something that requires more processing than we are capable of by simple transduction, etc. Example?)
- Can we engineering mappings with temporal correlations? What are the limits of such an internal model of this dynamics?
- Is the mapping a dynamical system? What aspect of dynamical systems can we (not) represent and use in the brain?
- What is the difference between these two versions?
- How do we generate these structured mappings in a principled manner?
- Can we engineer “latent” structure in a sensorimotor mapping to characterize the constraints of a neural learning system?

## Task

- Not dependent on limb mechanics
	- Focused on muscles of the hand (for CM connections)
- intuitive (preferably without explanation (@Huk)
- Think about priors? E.g. remaining upright…
- Complex / Naturalistic / High-dimensional
- Perhaps it is generative based on state? So no two subjects experience the exact same environment
- Why hand muscles directly? This removes the transformation from brain to hand coordinates, we’re directly tapped into the muscle space to test the limits of what can be learned by direct motor output

Thinking about the hands in particular, which seem to have far fewer constraints computationally / behaviorally as the arm, how can we begin to connect motor learning control to a broader understanding of learning and control in general?
What do we mean when we say learning and control in the context of the hands, who seem to have more “freedom” than the other limbs.
That is, the hands can be utilized as an output of cognition over the arms, which are more constrained.

## Model

Bayesian active sensor for uncovering latent structure of a novel sensorimotor mapping
Primitives (Todorov, Ghahramani) / modularity
We know that there are synergies at some level (Takei 2017, Gizster and his frogs)
What are their limits? When do we overcome them? With the hands, but what does this help us explain, or how does know this system, or modeling it, help us make more naturally moving robots / soft systems?
These synergies arise for several reasons
Biomechanical constraints (trivial)
Statistical structure of environmental demands (task dimensionality / dynamics)
Hierarchy (example? Todorov?)
How to structure this?
Todorov has a two-step mapping-- input to sensors to high (hidden) to low to output
This hierarchy relies on the statistics of the environment in which learning takes place
Override / Exploration / Dexterity -- how does this arise?
How do we test for this?
How is this different from Nazapour?
An ability to remain open to unpredictable events?
Based on the statistical structure of the task world
How can we leverage this to develop some behavioral analysis of motor “modules” or some such solution to the task?
How can we generate an understanding of how movements are shaped by the statistics of the environments in which we move?
Can we engineer the statistics of tasks to probe how the brain attempts to learn in the face of uncertainty, and choose a motor output solution (out of many) that suits the system? Can we relate this to subject-specific differences?
We know motor memories have multiple timescales of decay that reflect the statistics of the environment / skill (Shadmehr, Bastian, Wolpert)
“we present experimental evidence that sensory uncertainty, which affects motor variability, instead of variability per se, determines learning speed during trial-by-trial random perturbations” (Kording 2016 Statistical Determinants)

The reverse engineering problem is cool-- we present the system with a problem to solve, and we keep giving it problems until we define the boundaries of what it can learn, not learn, learn well, learn not-so-well. We have to construct these tasks in such a way that they tell us something specific.

What makes a mapping learnable, and how does a system change to learn a new mapping?
What has evolution done to accommodate mappings while retaining (or evolving) flexibility / dexterity?
How does robotics try to deal with this?
The system is hierarchical-- it has overlapping motor pools, synergies, reflexes, direct cortical overriding signals. It seems that it has a higher amount of direct control the further distal you go in the human arm.
The dynamics of the types of tasks humans can learn to do our crazy-- so we have to give up modeling them and learn how the system adapts to produce these outputs without an explicit model-- where does the “model” live?
What types of internal models can you learn? Not learn?
The motor system seems to effectively solve difficult inverse problems-- how

Drill in on the types of mappings, classes of mappings, that are learnable-- this tells us something about how the brain is undergoing the learning/adaptation process. This is the learning question, and it gives us insight into a model for how the brain learns to adjust for error in it’s task. We can even study this simply with a force output to start.
The second question is what the muscles are doing during the learning problem, and tying this back to our knowledge of the physiology of the system. The problem here is not providing mere speculation on what’s happening under the hood, but generating testable hypotheses. This step also required being very careful about the data collection process in order to make sure we have data that is capable of supporting out hypotheses
The next step is to design perturbations, within the task and for the mapping, and detect, for a given mapping, whether synergies are re-recruited or if other mechanisms are used to accommodate for unpredictable perturbations.

Interesting that users found it frustrating to adjust the mapping after each trial block-- how can we continually shift the mapping to maintain constant learning, or show some metalearning?

Perhaps with nonlinear mappings there is no closed form control solution, but we are able to control the system with our bodies. Is understanding how the system is solved (quickly?) by biological neural control connected to how it might be solved using, say, a neural network?


## Motor Control at an Algorithmic Level

Wolpert:
> From laboratory learning to real-world learning. We now have a detailed understanding of the learning and control of a narrow range of tasks, including simple reaching tasks in which visuomotor and dynamics perturbations are applied. Although these tasks are amenable to analysis and modelling, they do not capture the full complexity of real-world motor control and it is not clear whether the learning models that are developed will generalize to tasks such as tying shoelaces or learning to skateboard. The study of sensorimotor control is fundamentally difficult because it deals with a dynamic, real-time control system that turns sensations and memory into action and vice versa. Given this complexity, it is understandable that the field has focused on a limited number of simplified tasks. However, expanding the range of tasks may help us deal with new challenges.

Optimal Feedback Control (Todorov):
> In our motor outputs, we attempt to reduce variability in task relevant dimensions over task-irrelevant ones by what we call the "minium intervention principle".

This was shown to occur at the muscle level in a single finger task [@Valero-Cuevas2009].

## Towards a Model

Modeling the data from this work will:

- combine prior physiological and anatomical knowledge with behavioral evidence. The questions surrounding this element of a model are: optimality of behavior, the origins of versatility/dexterity in fine movements.
- explore the nature of synergies in fine motor tasks involving the hand. How does the motor system use synergies to learn new mappings while remaining robust to perturbations
- be hierarchical in nature to reflect knowledge about the CST and prior modeling efforts[@Todorov2005,Loeb2004].
- produce muscle-level predictions for a given mapping or family of mappings.

The center of interest converges on a muscle-level description of the learning process of a novel mapping between muscle activity and a virtual scene.

The place to start is by using a force pad in place of the EMG signal to replicate behavioral studies. The force pad can be mapping to a virtual scene and data can be taken. This gives us a testing ground for investigating interesting mappings.

There are three concepts that tend to inhabit three separate realms in the literature:

- muscle synergies, particularly their flexibility and origin
- algorithms for motor control and learning, particularly optimal feedback control and the uncontrolled manifold hypothesis
- the physiology of the corticospinal tract, particularly corticomotoneuronal (CM) connections

I believe that by thinking about these disparate research topics as interconnected, we can learn something about the mechanisms by which humans are capable of quickly learning novel motor tasks.

## Task notes

- Mapping
    - linear
    - nonlinear (with tunable nonlinearity)
- Control mode
    - closed-loop (e.g. tracking, balancing)
    - open-loop (e.g. reach, point)
- Sensory feedback
	- auditory
	- visual
	- proprioceptive
	- cutaneous

Our hypothesis that relatively high dimensionality tasks can be learned in the distal muscles with increasing learning curve time constant. Additionally, we expect to discover synergetic muscle activations in higher dimensional tasks that prohibit further fractionation of motor outputs. A second, slower time constant, we hypothesize, will emerge at higher dimensional tasks that is limited by the reformulation of synergies. These time constants should underlie a multi-rate, hierarchical neural controller.

These types of control problems are something primates in particular are most adept at. We want to generate a systematic characterization of our ability to solve such control problems using the hands using recent physiological findings.

Such characterization, we think, will gain ground on the following questions:

- What are the limits of human learning? (As opposed to the limits of motor output[@Scheiber2004])
- How can we best extend current theory of motor learning and control?
- Can our findings and models advance engineering motor learning and control _in silico_?

We hypothesize a particular purpose for CM connections in dealing with online error correction. Specifically, we should find suboptimal control to perturbations if synergies are fixed. We agree with the suggestion by Takei et al. that CM connections may underlie the fractionation of synergies. Perhaps this can be seen in response to an unexpected disturbance, when synergies would supply suboptimal motor responses.

Recording at the muscle allows us to relate the learning of novel mappings (and possibly new synergies) to dealing with online corrections.

Apart from generating a family of sensorimotor mappings to be learned under spatial or temporal dependence and/or sttochasticity, we could imagine mapping the eletromyographic input to the control input of various dynamical control systems. In this way, we can understand what strategies a subject uses to explore the passive dynamics of an unknown system. This system identification process, however, may complicate the task beyond the the relevant questions.

## After doing Tim’s task:
- We’re building an internal model of the task structure, and we might even have competing models to drive decisions
- How much data do we use from the past to alter our current model(s)?
- We might take inspiration from “active learning” or “online learning” or “incremental learning” which uses streaming data to alter models. How does that evolving model then inform actions/policy?
- Data Horizon:  How quickly do you need the most recent datapoint to become part of your model?  Does the next point need to modify the model immediately, or is this a case where the model needs to behave conditionally based on that point?  If it is the latter, perhaps this is a time-series prediction problem rather than an incremental learning problem.
- Data Obsolescence:  How long does it take before data should become irrelevant to the model?  Is the relevancy somehow complex?  Are some older instances more relevant than some newer instances?  Is it variable depending on the current state of the data?  Good examples come from economics; generally, newer data instances are more relevant.  However, in some cases data from the same month or quarter from the previous year are more relevant than the previous month or quarter of the current year.  Similarly, if it is a recession, data from previous recessions may be more relevant than newer data from a different part of the economic cycle.
- Generalization of task structure (apply acquired models to solve similar, but noticeably different, task) -- or maybe new sensory feedback? This feels like structural learning

## Implications / Future / Wide Angle
- The promise of a noninvasive neural interface may seem like science fiction, but many groups are making headway in this direction, highlighting the large amount of information present in a noisy surface EMG signal.
- For any neural interface, there exists a learning gap between the output and the intended sensory feedback. This gap can be filled if an appropriate model is constructed such that input and output match in a predictable manner.
- For such an interface to accord properly with our intentions, we need to better characterize the “learnability” constraints of such models. By characterizing these constraints and modeling the strategies used to acquire internal models of new sensorimotor mappings, we can better understand how to develop interfaces that accord with our natural ability and thus move closer to the best interface—one that you forget is there.
- I want to find out what constraints exists in motor learning, and how this relates to human-machine interfaces. That is, what constraints must we consider when designing interactions with machines? What sorts of principles can we use to facilitate such interactions in order to best extend our minds into the machine?
- What are the limits of what we can learn? How can we quantify learnability?
- Does the brain/body use a compressed sensing strategy in the face of uncertainty?
What do you do if you’re in an unlearnable environment?
How can we quantify learnability (apart from the biomechanical constraints) and how does this tell us something about cognition, learning— our strategies for learning?





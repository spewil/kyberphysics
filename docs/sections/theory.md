# Preliminary Theory {#sec:theory}

> *An interesting open question is how to relate trial-to-trial dynamics of learning to asymptotic predictions regarding optimal adaptation.*
>
> &mdash; Todorov, *2007*

What are "normative models"?

> Normative models suggest that the nervous system optimally adapts when faced with an error. To determine this optimal adaptation, the normative model must specify two key features of the world. First, how different factors, such as tools or levels of fatigue, influence the motor system — the so-called generative model. Second, how these factors are likely to vary over both space and time — that is the prior distribution. The structure of the generative model and the prior distribution together determine how the motor system should attribute an error to the underlying causes and, therefore, how it should adapt. [@wolpertPrinciplesSensorimotorLearning2011]

<!-- OFC MODELING AND DISCUSSION -->
$include includes/ofc.md

<!-- MODEL ADAPTATION VIA GRADIENT DESCENT -->
$include includes/model_adaptation.md


<!-- 

adaptive is within trial, as you move
episodic has endless access to a simulator

## List of variants, etc 

- LQR + SDN
- robust control (?)
- KL-control + composition
- game theoretic control-- compare solutions

## Distributed Control

> The hierarchical organization typical of earlier sensory areas is not adhered to everywhere. On the contrary, the anatomy of associative areas and prefrontal  cortex suggests a more "democratic"  organization, and  processing  appears to take place  in webs of strongly interacting networks (8). Decisions to act and the execution of plans and  choices  could be the outcome of a  system with  distributed control rather than  a single control center. Coming to grips  with systems having distributed control will require both new experimental techniques and new  conceptual advances. Perhaps more  appropriate  metaphors for this  type of processing will emerge from studying  models of interacting  networks of neurons. [@sejnowskiPerspectivesCognitiveNeuroscience1988]

## Policy Selection

each timestep you combine actions from component policies to choose an action

Here we'll review and discuss models of action selection and policy composition as a means of theorizing about how subjects learn novel skills. 

In a sense, we're setting up several different directions for our understanding of composition and action selection which can be experimentally tested. 

We have a direct selection algorithm, composition through policy addition, and composition through policy multiplication. 


### KL-control Composition (1 day)

This setup is particular subset of OFC problems. 

Dynamics
Cost

Composable policies

PLOT OF INTUITIVE EXAMPLE

### Multiplicative Policy Composition

Policies are distributionally weighted, as opposed to chosen each timestep? 

### Temporal Composition

there is a spectrum of latency in the feedback response

can different controllers be used for different latencies, and adjusted accordingly?

### Generalized Policy Selection (1 day)

This is in the MDP case

Learning happens in several ways-- reward regression, Q-learning

What are rewards? 
What are tasks?
What are actions?

Is GPI with LQRs / LQR-RL a good model for motor learning? Define a model and see if it recapitulates known motor learning phenomena on existing experiments + accounts for things that previous models don’t. (Similar in spirit to Geerts et al. (2020)). Can this model track the higher-order statistics of trajectories during motor learning?

### Model-based Reinforcement Learning

Since we only have an approximate model of the system dynamic, we could simply work towards an optimal policy directly using gradient derivative-free optimization methods in a model-free approach. Since we have good evidence that humans leverage internal models to make decisions (at least in a motor problem domain), we need to define an algorithm which uses past observations and controls to update our approximation for the system dynamic. Here is a very general algorithm:

0. Define a base policy/controller and base system model ($L_0$ and $\hat{M}_0$)
1. Collect samples (by interacting with the true environment $M_{true}$) using the current policy/controller (collect $y_t,u_t,y_{t+1}$ triples using $L_i$ for $i \in \{0\dots N\}$
2. Use sample(s) / trajectories to update current system dynamical model $\hat{M}_i$
3. Update current policy/controller $L_i$ (using the system dynamics or using a direct policy method)

If the true system dynamics were known, we could solve the Algebraic Riccati Equation with a backwards pass, and compute our controls in a forward pass. This general algorithm structure highlights how the (unknown) system identification and controller design are intertwined: identifying a system appropriately must rely on sampling and fitting regions of the state space pertinent to adequate control in terms of cost (Ross ICML 2012). Otherwise, our approximation to the true system dynamic will only produce a valid controller in regions we have previously explored. The question is how we can effectively (sample and time efficiently) utilize new state transitions we encounter either online as feedback or between trials to update our model and policy. That is, the number of trials and/or trajectories to use before updating either the system model and/or policy is an important parameter.

In the LQG setting, this might be called "adaptive LQG". -->

Learning LQR controllers

    Q-learning for LQR
    policy gradient for LQR
    what is an LQR-SR? what does this help us do?

where does LQR break?
- goal shift (is this true?)
- task shift (different goal? this isn't true)
- goal uncertainty (this can't be modeled...)
- LQR variants break more easily?

where does KL-LQR / control break?
 - one policy at a time...? re-optimize your single policy per task? (task could have multiple goals)
 - could have multiple possible (terminal) goal states
 - not continuous -- code this up and understand it in continuous would be a good result
 - selection is done beforehand... can this shift online...?
 - allows you to construct more interesting policies...
 - can we connect this to KL between passive and dynamic? change this to planned and replanned?

is there a multiplicative LQR composition?
- sergey levine multiplicative paper?
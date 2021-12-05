# Next Steps{#sec:next_steps}

> *When it comes to the problem of skilled movement, the algorithm is simply not known.*
>
> &mdash; Wolpert & Ghahramani, *2000*

## EMG Hardware

Our preliminary data confirms the working principle of the setup and highlights the next steps for producing quality datasets. This is in accordance with the literature, where more advanced use of EMG is emerging as an important tool in understanding the complexities of motor computation[@Hug2011]. Our next steps are to build a new version of the EMG hardware doubling the number of channels to 64 electrodes placed across the forearm and to provide better hand constraints to ensure completely isometric contractions. The next hardware version will also include investments in shielding to provide proper noise mitigation. Most EMG in the literature is smoothed and trial-averaged due to noise, but we are confident that our records can be analyzed at the level of single trials, much like recent developments in neural data analyses [@churchlandNeuralVariabilityPremotor2006;@churchlandNeuralPopulationDynamics2012a].

### Eye Tracking

To completely close the loop in our experiments, we are working to integrate pupil and gaze tracking to more closely follow the perceptual aspects of our task. We hope to find correlations in line with the literature dealing with active learning[@yangTheoreticalPerspectivesActive2016;@huangActiveLearningLearning2008].

<!-- > EMG activity was recorded using hook-wire electrodes (44 gauge with a 27 gauge cannula; Nicolet Biomedical, Madison, WI) placed in the muscle for the duration of single recording sessions. [...] Electrode voltages were amplified, bandpass filtered (150–500 Hz, four pole, 24 db/octave), sampled at 1000 Hz, and digitized. Off-line, raw traces were differentiated (to remove any remaining baseline), rectified, smoothed with a Gaussian (SD of 15 ms) and averaged. [@churchlandNeuralVariabilityPremotor2006] -->

## EMG Analyses

### Preprocessing

Preprocessing of the EMG signal per-channel is another key area for improvement. EMG signal is the convolution of motor unit action potentials terminating near the electrode sites. Ideally we could filter each channel of raw EMG to infer the signal envelope. There is precedent in the literature for Bayesian filtering of EMG signal using a Laplacian distribution. Sanger used a Laplacian distribution to filter a one-dimensional EMG signal[@sangerBayesianFilteringMyoelectric2007]. In accordance with this choice, Nazarpour found that as more motor units are recruited, the EMG distribution shifts from super-gaussian to gaussian following the central limit theorem[@nazarpourNoteProbabilityDistribution2013]. That work suggests methods for estimating high-order statistics for better filtering at low contraction levels relevant to our experiments. Such methods may prove to be more rigorous for inferring motor unit activations from our raw signal.

<!-- 

A window of EMG of length $T$ samples can be modeled as a convolution

$$
\mathbf{z} = \sum_t^T \mathbf{h} * \mathbf{s}
$$

where $\mathbf{h}$ is a motor unit activation template, which itself is a particular neural spike waveform, and $\mathbf{s}$ is the incidence of a spike, which might be modeled as a point process.  

-->  

### Calibration

With a filtered raw signal per channel, our goal is to devise mapping from EMG space to task space which are biophysically achievable by our subjects but require a degree of learning over many trials. In our preliminary task, we hardcoded mappings. Our next step would be to design a calibration task which asks subjects to actively explore the biophysical limits of EMG space that can be captured by our electrodes. This is akin to extracting features of spontaneous activity and passive viewing used in cortical BMI experiments to generate "intuitive" mappings [@Clancy2014;@sadtlerNeuralConstraintsLearning2014].

With high-dimensional EMG, we would ideally devise a principled method of extracting modes from raw EMG that accurately reflect modes of neural drive, demixing neural modes across channels. Here we used PCA as a first step. One starting point would be to align with the cortical BMI literature and use factor analysis and Kalman filtering[@sadtlerNeuralConstraintsLearning2014]. The issue, however, is how to design a task which evokes the available modes of possible EMG activity before using dimensionality reduction to generate learnable yet non-intuitive mappings.

<!-- autoencoders (farina paper) [@vujaklijaOnlineMappingEMG2018]  -->

<!-- Another direction for analysis is to study long-range correlations in EMG data within and across trials through empirical correlation functions[@crevecoeurGoldstandardApproachAddress2010]. This work may inform features of models which attempt to recover aspects of trial-to-trial learning. -->

## Task Design and Data Collection

With a working calibration task, our next goal is to use this calibration data to generate mappings to track learning. Our center-hold, reach-out task combined these two steps into one task for validation of the setup using hardcoded mappings. We can maintain the center-hold, reach-out style of the task but with data-driven mappings, as well as construct novel tasks to test predictions of our models. Scaling this task up to multiple subjects across days will provide a dataset with which we can test hypotheses concerning the evolution of complexity and correlations across learning. This will also give us an opportunity to study inter-subject variability, for which there is precedent in the literature which suggests individual strategies[@crouzierIndividualDifferencesDistribution2019].

## Modeling Control

One relevant aspect of the basic optimal feedback control model is that the optimal controller that arises from specifying a quadratic state and control cost is invariant to the target state. In spite of this, we can use the aforementioned task to test predictions of the basic LQR model with respect to state and control noise and imperfect dynamics.

We expect to validate the basic optimal control models for our setup as we've designed the learning environment specifically for the EMG signal provided by the subject acts as the input to chosen virtual dynamics, which can be chosen in accordance with our model. We can then test perturbations in our task with respect to noise, goal, and dynamics and compare subjects' responses to our models.

The question then becomes: when might subjects need to internalize a new control policy? When might they need to internalize multiple control policies? We hope to work towards answers of these questions alongside models of compositional control. Such control models could deal with, for example, target uncertainty as well as multiple competing targets[@gallivanActionPlanCooptimization2015;@gallivanParallelSpecificationCompeting2016].

<!-- 

- stochastic optimal control model comparisons
  - cost models 
  - perturbations in goal
  - go-before you know / goal uncertainty 
  - noise perturbations -- do reponses match the models?

- dynamics model fitting
  - internal model uncertainty 
  - modeled with robust optimal control?  
 
-->

<!-- (task reads out from D muscles, find modes of that data; do PCA to get K < D dimensions, controller only responds to motion in those K directions)—does behavior + motor activity follow LQR? this question has already been asked, but it hasn’t been asked for this kind of high-to-low dim mapping. It’s been asked in tasks where muscles haven’t been directly in control (Valero-Cuevas 2009).  -->

<!-- Todorov: do a task, look at muscle signal. Muscles that aren’t necessary for task have higher variability b/c they’re not being optimized for task (but does’t introduce perturbations). Also see Loeb (2012) for a negative result saying that muscle coordination is habitual rather than optimal, but it has issues (low # muscles). Can we replicate previous reaching optimality results in our set-up? What’s unique about our set-up is the PCA/dimensionality reduction in muscle activity space. This is important because you can create arbitrary muscle-cursor mappings, so you have to learn a new skill/mapping. This is different than perturbing a fundamental movement and forcing adaptation, which is what has been previously done. For our task, the participants actually have to learn a new task/mapping, rather than just do what they already know and be robust to perturbations. We test the LQR hypothesis once they’ve learned the task, because LQR isn’t a learning theory, it’s a theory about optimal control. We can see if, once people learn a new skill, their behavior is optimal wrt LQR theory. If we establish this, then we can think about how this LQR model is actually learned (enter RL). -->

## Modeling Learning

Ultimately, our goal is to adapt optimal control models which begin as coarse approximations and are updated both within and across trials. Adaptation typically refers to online alterations to control policies while learning might refer to across-trial policy changes. Our theoretical aim is to devise models of learning and movement construction which extend the optimal feedback control framework through additions of composition and error-based updates.

<!-- gradient descent stuff -->

Stemming from our work using simple gradient descent to update internal dynamics models, we would like to gain a better understanding of the loss landscape. It may be possible to compute the optimum analytically and to corrupt the dynamics matrix in a more principled way. We will also explore the action of the resulting gradient, and compute second-order derivatives, and compute derivatives with respect to the control law $K$ as a comparison. These results can then be compared with results from the reaching adaptation literature. This work can be guided by analyzing our empirical data to understand what aspects of our trajectories in EMG and task space are changing over trial.

<!-- 
- explore connections between spectral analysis perspective of optimal control and empirical correlation functions from data
- make the connection between control and dynamics in model and experiment more tightly integrated.  
- learning control via reward (RL) [@vanderkooijLearningReachTrajectory2021] -->

## Open Questions

- What is the best calibration task to find the boundaries of the available EMG space?
- What are the defining features of learning in our EMG-based task?
- Are our experiments well-modeled by the optimal control framework?
- How do subjects efficiently use error information from each trial and feedback from each time step to update their forward model and control policy/policies? How do subjects balance policy updates with model updates?
- How does a subject sample the state space to efficiently learn? Do subjects sample optimally?
- How can you empirically disentangle system identification (model estimation) and policy learning? If subjects are suboptimal, is it due to model mismatch or a suboptimal policy?
    
<!-- - On what scale (trials, timesteps) is the model altered? the policy? -->
<!-- - Replanning at every timestep is a model predictive control algorithm -->
<!-- - What prediction can we make for ID/learning every trial? -->
<!-- - how does a subject avoid "distribution mismatch" between their base policy and their optimal policy? How do they efficiently explore and use this new data to update their internal model? -->
<!-- - what exploration strategy does a subject use to avoid mismatch? -->
<!-- - What is a subject's baseline/prior model? $y_{t} = \hat{f}_0(x_t,u_t)$ or $y_{t} \propto p_0(y_t|x_{t},u_t)$ -->
<!-- - What is the base policy / prior policy? $u_t = \pi_0(\hat{x}_t)$ -->
<!-- - How do we think about learning a distribution over trajectories in control law space, or perhaps equivalently, in covariance/precision space? -->
<!-- - We might hypothesize that a subject will act as randomly as possible while minimizing cost, a maximum entropy solution that converges to an optimal controller? $\mathcal{H}(p(u_t|x_t))$ -->
<!-- - How does a subject penalize changes to their controllers? Do they follow a KL-divergence type of measurement when improving their policy? -->
<!-- - How do we best modeling learning LQR controllers trial-to-trial? -->
<!-- - how do we use existing controllers to construct movements? -->
<!-- - how do we construct controllers under dynamical and goal uncertainty? -->
<!-- - How does the observation mapping relate to the latent state covariance? The task state covariance? -->
<!-- - How do we formalize this into a probabilistic graphical model? Why would we? -->
<!-- - Would this make it easier to reason about what the goals are? -->
<!-- - Would learning $M$ become an inference problem? -->
<!-- - Would solving the control problem become an inference problem...? -->
<!-- - What noise assumptions can we make? Can we not make? -->
<!-- - How can we incorporate signal-dependent noise? -->

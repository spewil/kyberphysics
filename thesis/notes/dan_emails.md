Adrian Haith and Jordan Taylor -- good people for motor learning and expertise

## rig

I think getting data flowing from your rig plays to your experience - RL/PGM intuitions will come in time. I'd emphasise again, that it is a good strategy to shoot for a (pure) empirical paper in the short-term as a stepping-stone to a modelling paper.


## information geometry

Dan: "A statistical manifold is a manifold of probability densities with a Riemannian metric induced from the KL-divergence. The key invariance property that Alex et al highlight probably corresponds to the covariance of “natural gradients” under reparametrizations in the “information geometry” framework. Shunichi Amari has several books and reviews on this topic of “information geometry” which I think you’d be interested in. In particular, look out for the natural gradient method which has been applied in RL by Sham Kakade, Jan Peters etc to develop “natural policy gradients” and “natural actor-critic” algorithms respectively."


## inverse RL

If you are interested in inferring cognitive representations from motor output, you might want to check out inverse RL which is all about mapping from a policy to a reward function (as opposed to “normal” RL which is about mapping from a reward function to a policy). Here is an application:

https://www.ncbi.nlm.nih.gov/pubmed/19729154


## flexible policy representations

In RL, the root problem is the curse of dimensionality. Continuous control is particularly affected by this. Policy optimization can end degenerating into random search due to gradient estimation noise. All RL methods are basically ways to get around this - deep representations, imitation learning, trust regions etc. These methods sometimes lead to ok but inflexible (overfitted) policies. Thus, flexible/multi-task/transfer principles are at a premium. Progress on how the brain represents policy sets in an efficient/modular/hierarchical/relational way would be of interest. Translating such principles into inductive biases during learning even more so.


## reward landscapes

There is a lot of neuro work on understanding cost/reward functions in simple decision-making (e.g. Padoa-Schioppa) but I think there is a complete lack of understanding about how humans cognitively “map out” the reward/cost landscape in complex control problems. That is, it is taken that humans may do some model-based planning initially in some abstract/discrete problem representation which then caches a cost function for a “lower” motor controller. The problem for the lower control can then be solved more efficiently or can make use of automated solutions etc. This touches on a lot of work e.g. the cognitive/motor interface (e.g. work of Rich Ivry), interactions between model-based/model-free control, subgoaling, theoretic work of Andy Barto on how to set optimal reward functions. I think it worth thinking about but my feeling is that this could be quite challenging.


## giant goal of "cognitive AI"

From the bio point of view, part of the problem with e.g. deepRL performance on mujoco etc tasks is how unnatural the trained policies are. They often just look really weird. I think this is a manifestation of the use of coarse metrics for training/model comparison and the fact that trained policies are very sensitive to noise suggesting that they are not well-regularized and certainly not globally optimal (part of Rechts point). I think an interesting result at the interface of artificial/biological motor learning, would be to experimentally verify a computational principle in human motor performance, integrate it into an RL algorithm, and show that humans perceive the resulting policies as more “natural”. Usually, this would manifest as an increased inability to distinguish between human-generated and computer-generated policies. This adapts the approach taken in “cognitive AI” - see e.g. Science paper of Brendan Lake and BBS review of Lake/Ullman/Tenenbaum/Gershman.


## go-before-you-know
- planning stage
- execution stage
- tease apart the internal plan with the online / feedback


## VR / inductive biases

in discussing working at this intersection of HCI/BCI with EMG and using those experiments to inform learning and control algorithms, several people have pointed out the fact that you can’t get rid of a subject's priors (put there by evolution+development) or the constraints built into their motor systems, etc. I countered this by suggesting a VR environment that is completely novel to the subject in order to turn this “problem” on it’s head— what priors/constraints do subjects in fact use to accomplish/adapt to new task demands? can we design these priors into our agents?

"VR can be used to interrogate the inductive biases in learning and implicit perception-action loops in motor control. This approach is being pursued heavily in rodents/zebrafish etc. I would suggest aiming to develop a research program that could integrate VR as a second step i.e. your first paper should focus on leveraging high-dimensional EMG, then your second paper could be EMG+VR."


## RL zoo

Which of this zoo of approaches/problems, all using similar setups (x,u,r,t), is most amenable to learning how a human is so damn good at picking things up and putting them back down?

> This is worth a significant discussion:) I tend to divide control algorithms up according to their (1) representational efficiency (e.g. the options framework) or (2) their dynamical efficiency (e.g. classical search algorithms). My bias is that the human motor system is extremely efficient representationally. That is, there is a deep latent hierarchy which can be flexibly modulated at many levels. Thus, regardless of the details of the optimization process, it can be completed in very few samples. Information-wise, the motor model is such that a huge range of optimal policies have very short description lengths. I suspect that EMG is better suited to studying representational efficiencies (e.g. hierarchy, transfer, modularity). In the longer run, there might be a possibility to combine EMG with MEG (I'm in the WCHN) to get a complete neural characterization of the cognitive-motor loop whereby the MEG component could be used to study "dynamical efficiencies" (i.e. how does the brain do policy search).


## EMG dynamics

I know we’ve talked about there being temporal components to the muscle activations that usually aren’t accounted for in NMF where you’re assuming every data point in electrode space is independent. But maybe this (incorrect) independence assumption is OK if you just want a summary of electrode correlations…

> I think this is a really important issue to think carefully about as it is a high-level decision which will have many downstream ramifications throughout the project. My perspective is that, in terms of the current trends in neuro research, “static” NMF/PCA results are not terribly interesting, and people in general are moving towards analyzing population dynamics. I think you are in a great position to pursue this perspective in motor research using the relatively high temporal fidelity of EMG. For example, a straightfoward research hypothesis that could be tested would be whether the motor system constructs dynamic synergies.

This does not preclude using static PCA/NMF to generate tasks/environments as a stepping stone towards that goal of course. Just need to be aware that a task/environment optimized using static unsupervised representation learning methods may be completely irrelevant to experimental hypotheses regarding dynamic motor activity. It may make sense to use static methods in order to replicate current research in your setup. On the other hand, applying dynamic methods (e.g. LFADS) to naturalistic data would already probably lead to a paper in itself as one would expect that more motor variance could be explained and made interpretable.

## OFC modeling

A normative model to go with an empirical effect

> Learning models in motor control (e.g. “state-space models”) are quite deficient and I doubt will capture the relatively sophisticated principles you are interested in. An alternative and richer approach would be to model OFC as a function of internal model and objective function acquisition. One could imagine progressively computational lesioning OFC and fitting the result to different phases of learning. Could also apply to transfer/compositional algorithms. This is quite a common strategy for understanding e.g. RL systems.
Lets say I solve for an expert LQR (with signal-dependent noise) reaching to a point in space. The resulting policy will prefer to reduce variance in task-relevant directions compared to task-irrelevant directions (the controlled and uncontrolled manifolds respectively). One could also compute a novice LQR which tries to reduce variance in both directions e.g. with a corrupted reward function. Maybe human data fits the later early on during training and the former once they become experts. One could then generalise to modelling a smooth transition between novice and expert as a function of learning.
My view is that there is a dearth of work on how OFCs are learned in the CNS. This is because OFC is studied in goal-directed reaching movements (and perturbations therefore), a domain in which humans are already hyper-expert and thus any learning is too quick to observe. In contrast, motor learning is usually studied in visuomotor perturbations which is very hard for humans so they learn slowly but this domain is very non-ethological and thus does not lend itself to OFC. In addition, people tend to use these awful “state-space models of maximum perpendicular error”. Therefore, I think a de novo experiment approach with relatively sophisticated modeling would be a positive path to take. In addition to initial approaches using OFC, it would be cool to run DRL etc. too.
The problem with control is not a lack of efficient solvers (e.g. LQG and some non-linear variants are trivial to solve), its a lack of normative process-level theories of inference/computation.



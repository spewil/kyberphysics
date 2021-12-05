## Successor Representation

### questions

- how do SRs work without rewards?

$$
\begin{align*}
r(s,a,s') = \phi(s,a,s')^T w
\begin{align*}
$$

- SRs sit between MF and MB -- can we show (perhaps akin to Gershman 2016 in Plos) that strategies shift from MF to MB? Even if we can show this descriptively at first... then we can perturb or make some claims about a model with the ability to increase granularity of model...? Or competing systems?

## Representation Learning in RL

The RL framework can be used to learn map- pings between observed perceptual features and states, compact representations of relational and associative structures of the state space, as well as abstractions enabling transfer between tasks and environments. Momennejad2020

While in classic model-based RL learning the structure of states implies learning the probabilities of transition between adjacent states, other RL approaches can learn compact representations of the multi-step and multi-scale structure of the environment. Momennejad2020

Why use the RL framework to study how biological agents learn structures? There are at least two reasons for using RL for structure learning. First, RL is biologically plausible and offers testable hypotheses about the neural implementa- tion of structure learning and their correspondence to behavior. This is an advantage over Bayesian cognitive models that have been more commonly used to study structure learning and causal inference, but cannot offer an adequate account of neural implementation [31]. Sec- ond, while model-free RL is more broadly known, RL representation learning principles can acquire compact and predictive representations of structures, even in the absence of rewards. Momennejad2020

Classic MB agents learn a representation of relationships between states that are one step apart. [...] Combining SR with learning from replay enables the agent to precompute multi-step and multi- scale dependencies offline, increasing planning efficiency when faced with a decision later on. Momennejad2020

Intuitively, intrinsic motivation can be thought of in terms of any learning or inference approach that decomposes the environment into task-independent components, which can be later combined to estimate value once a new task or goal is introduced. It has been shown that Laplacian eigenmaps can function as intrinsic motivation. This is welcome news for a model that uses the SR. because Laplacian eigenmaps have been shown to be the equivalent of the eigenvectors of SR and linear slow feature analysis. In the context of value function estimation, Laplacian eigenmaps are also knowm as proto-value function. When computing the proto-value function, an environment is decomposed into basis functions of successor features and options, the linear combinations of which could compute any given task’s value function and hence serve as intrinsic motivation. Momennejad2020

V = phi(s)u^T (decompose reward u and successor features)

### quotes

>The SFs summarize the dynamics induced by $\pi$ in a given environment. As shown in (3), this allows for a modular representation ofQπin which the MDP’s dynamics are decoupled from its rewards, which are captured by the weights $\mathbf{w}$.

>Mathematically,  the  SR  is  a  matrix  M,  where  the  i-th  row  is  a  vector in which element Mi,j stores the expected discounted future occupancy of state j following initial state i. To understand what this means, imagine starting a trajectory in state i and counting the num-ber  of  times  each  state  j  is  encountered  subsequently,  while  expo-nentially  discounting  visits  that  occur  farther  in  the  future.  This  representation is useful because at the decision time, action values can be computed by linearly combining the SR for the current state with the one-step reward function. This obviates the MB strategy’s laborious iterative simulation of future state trajectories using MB’s one-step model, but stops short of storing the fully computed deci-sion variable, as MF learning does.

>Another  form  of  SR  hybrid  could  be  realized  using  the  MB  system (a cognitive map), or episodic memory replay, as a simulator  to  generate  data  for  training  the  SR.  This  resembles  the  family  of  Dyna  algorithms20.  Evidence  from  rodents  and  human  studies  showing  that  offline  replay  of  sequences  during  rest  and  sleep  enhances memory consolidation30 and learning new trajectories31,32. Because the SR is updated via the simulations of the MB system or episodic  memory  offline,  this  Dyna-like  hybrid  model  retains  the  SR’s advantage of fast action evaluation at the decision time (Fig. 8). Updating predictive representations via replay is in line with recent attention to the role of memory systems in planning and decision-making22,33.  These  different  realizations  of  an  SR–MB  hybrid  are  essentially  speculative  in  the  absence  of  direct evidence.  Further  work is required to adjudicate between them.

>SR is itself a sort of world  model,  not  entirely  unlike  the  sorts  of  cognitive  maps  usually  associated  with  the  hippocampus.  The  learned  representation  is a predictive model, which allows the mental simulation of distal future  events  rapidly,  at  least  in  the  aggregate.  It  differs  from  the  one-step  model  representations  learned  and  used  in  standard  MB  learning, mainly because it aggregates these predictions over many future time steps. This aggregation introduces a new free parameter: the timescale over which future events are aggregated. In theory, the prediction timescale (known as the ‘planning horizon’) is controlled by the discount factor over future state occupancies in equation (1) (see Methods), and need not, in general, be the same as the agent’s time discount preference over delayed rewards34. Instead, we predict (and leave to future work to investigate) that the planning horizon should rationally be influenced by the statistical structure of experi-ence, such as the stability or volatility of transitions and rewards in the environment.

>The SR is defined analogously to the value function; instead ofcumulating rewards (as in the value function), the SR cumulatesstate occupancies. (Gershman 2018 review j neuro)

>M(s, s􏰓) is the SR, defined as the discounted occupancy of state s􏰓, averaged over trajectories initiated in state s. The SR can intuitively be thought of as a predictive map that encodes each state in terms of the other states that will be visited in the near future. It is “optimal” in the sense that a linear function approximation architecture can exactly represent the value function if the features correspond to the SR; i.e., fd(s) 􏰑 M(s,d), where d indexes states. (Gershman 2018 review j neuro)

>Take, for example, latent learning, in which an animal is placed in a maze for several days without any reward, and then subsequently trained to navigate to a re- warded location in the maze. The key finding, first reported by Tolman (1948),
is that animals are faster at learning in the rewarded phase if they were first pretrained without reward. The SR provides a natural account for this finding (Russek et al., 2017), because the SR can be learned during pretraining without direct reinforcement. Then, during the training phase, the reward function is updated and combined with the SR to compute values. Importantly, the reward function (unlike the value function) can be learned lo- cally, and hence is more quickly learnable. (Gershman 2018 review j neuro)

>The SR is able to rapidly adjust values in response to reward changes, thanks to the way in which the value function is parsed into predictive state and reward components. (Gershman 2018 review j neuro)
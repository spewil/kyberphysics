
## algorithm for motor skill learning

- search
  - we inject inputs to do system identification, collect data in order to learn/infer the constraints inherent to the system.
  - this is finding the modes of the system, understanding its rules (holonomic / non-holonomic constraints)
- coordination
  - we develop a policy at the level of coordinating the constrained modes
  - our policy learning algorithm is itself constrained (by us, the learner) because we have limited capacity to achieve coordination
  - this is a kind of regularization on the learning process? you have limits to your coordination ability due to processing constraints
  - you're constrained in how you can mix policies/primitives, and changing this mixture is an RL-type problem, but importantly your primitives are more constrained than your high-level controller
    - this, i think, will predict some aspects of the data
  - e.g. manhattan strategy
    - flat cost landscape with constraint on l1 of mixing vector 

[@pirayLinearReinforcementLearning2019]

mixtures of experts
basis function combinations
    - basis functions as linearRL policies? 

what is complexity of mixture of gaussians (basis functions)? how can i write an expression for the complexity of the resulting mixture, or of the mixture weights themselves? the complexity will probably include aspects of each. then the trick is to constrain the mixture by placing a limit on this complexity.
- read the equations for mixtures of gaussians
- what is the entropy / mutual info of these things? 


take the composite KL-LQG problem
is the mixture of KL controllers an expanded KL cost? 
can we rewrite the default policy as a mutual info? between what and what? (something independent and something joint)



the bounded rational control thing
F = U - beta*KL(p(a|w) || p(a))
the distance between prior and posterior is now the constraint, the value because value under this posterior
can we make this posterior a mixture...? is it already a "bayesian mixture"? 





Todorov compositionality

Saxe multi-task

Gershman - different policies for different states == higher policy complexity

look at composition like chunking or options -- which policies depend on state and which don't?

policies encode state / state encodes policy -- compression in one policy vs compression of composite


--- 

mixture of gaussians is latent variable where gaussian is latent p(s'|gaussian)*p(gaussian|s)

smooth spatial contour map of policies p(policy|state) = softmax( policies, f(state) )

constrain the complexity of the weights on policies? 
on the latent distribution p() ( complexity of the distribution, entropy...? )?

--- 

we want something that is capable of producing complex combined policies (expressive combinations of actions), but is crippled to produce simpler actions

--- 

intuitions about heterarchy, composition, and complexity 

we have a a map of policies, we can produce any kind of combination of them, but we're fundamentally resource constrained such that the complexity borne out of this combination produces suboptimal composite policies, and thus suboptimal (in terms of cost without complexity)

two routes 

- one would be to add an explicit complexity cost into our policy in a way that's not just tinkering with the default policy, or tinkering with the default policy in a way that is principled? Can we pack more into the KL cost? Have multiple terms in the KL that combine to form a default policy that penalizes complexity in a principled way?
  - this is the impetus behind the generic complexity cost work
- second way would be to build on the heterarchy and penalize complexity in the "mixtures of experts" -- how complex can my mixture/composition be? I'm assuming that I have access to the necessary building blocks, but my information processing constraints mean I can't contribute enough resources to immediately construct an arbitrarily complex composite policy.
  - this is a kind of extension on top of the first complexity thing

get a handle on complexity first, then extend to constrained composition

--- 

in robotics, jan peters has done a whole thing with dynamic movement primitives, elementary nonlinear diff eqs that are then activated to construct more complex movements

https://ieeexplore.ieee.org/document/5686298 

they've also made models from demonstrated trajectories for which pieces should be produced by which primitives-- learning the switching between dynamics
https://arxiv.org/abs/1806.06063

instead, we want something more compositional, where policies can truly be mixed / blended over time depending on the current state

--- 

the genewein braun paper:
- hierarchy in terms of choosing an expert under constraint, then constraining that expert's actions

we want something more like:
- take a set of primitives (experts?)
- have the ability to compose them any which way (mix experts?)
- impose a constraint on this composition (which expert can drive at once)
  - constraints in the mixing 
  - smoothness in the switching over time (slowness in the weights?)


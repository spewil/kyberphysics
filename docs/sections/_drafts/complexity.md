
what is the question?
- how does a complexity cost play a role in motor learning?
- how do subjects penalize complexity to aid in learning new skills?

TODO
- mutual information / complexity strong understanding
	- recapitulate the basic equations (cost, softmax policy)
	- Q: what is the mathematical foundation for this conception of motor control?
- assemble basic papers


why motor?
- isn't motor just spinal modules being played like keys?
- no, it's all about the dynamics-- the rich correlations between movement variables, prediction, feedback...
- motor actions are complex and extended across time and space


 think there are a number of unique things to motor control:
- We can use this framework to distinguish between skill learning (increasing policy complexity) and adaptation (no change in policy complexity).
- In sensorimotor control, 'compression' may be more about being sloppy on the sensory end of things, rather than having a compact policy to store and retrieve.
- We can speculate that practice and expertise as convincing your brain to commit to a more complex policy (or maintain commitment to a current level of complexity).
- Certain movement disorders could be viewed as involving information bottlenecks


can we hack the default policy to include more terms? something that includes complexity?


optimal control as optimal null hypothesis, normative null hypothesis

stroke as info bottleneck 
- enslaving (spatial complexity)
- rigidity (temporal complexity?)


how does effort go down over learning (like muscle activation)?
- trading effort for complexity
- high stiffness -- low information


default policy as habits [@pirayLinearReinforcementLearning2019]

# info bottleneck / policy compression

[@gershmanRewardcomplexityTradeoffSchizophrenia2020] 

"optimal compression means knowing the state probabilities"
having some form of a model -- marginal state distribution (mean state occupancies?) SR row sums?

"the memory demand of policies acts as an information bottleneck in action selection"


--- 



---

environment as noise? 

actions as encoded signals, feedback as decoder?
output (intended) signals, corrupted by noise, "encoded" by the environment (muscle output is compressed / low dimensional) feedback
redundancy of motor output == coordination == optimal encoder of movement?
do you coordinate output to receive most predictable input...?
errors in your code induce something about the code itself-- or the code is optimal relative to error / information
how do errors change the encoding?

--- 

Sutton and Barto on softmax policies:

If the action space is discrete and not too large, then a natural kind of parameterization is to form parameterized numerical preferences h(s,a,θ) ∈ R for each state–action pair. The actions with the highest preferences in each state are given the highest probabilities of being selected, for example, according to an exponential softmax distribution:

π(a|s, θ) = exp(h(s, a, θ)) / sum_b exp(h(s, b, θ))

where exp(x) = ex, where e ≈ 2.71828 is the base of the natural logarithm. Note that the denominator here is just what is required so that the action probabilities in each state sum to one. The preferences themselves can be parameterized arbitrarily. For example, they might be computed by a deep neural network, where θ is the vector of all the connection weights of the network (as in the AlphaGo system described in Section 16.6). Or the preferences could simply be linear in features,

h(s, a, θ) = dot ( θ, x(s, a) )

using feature vectors x(s, a) ∈ R^d constructed by any of the methods described in Chapter 9.

An immediate advantage of selecting actions according to the softmax in action preferences is that the approximate policy can approach a deterministic policy, whereas with ε-greedy action selection over action values there is always an ε probability of selecting a random action. Of course, one could select according to a softmax over action values, but this alone would not allow the policy to approach a deterministic policy. Instead, the action-value estimates would converge to their corresponding true values, which would differ by a finite amount, translating to specific probabilities other than 0 and 1. If the softmax included a temperature parameter, then the temperature could be reduced over time to approach determinism, but in practice it would be difficult to choose the reduction schedule, or even the initial temperature, without more prior knowledge of the true action values than we would like to assume. Action preferences are different because they do not approach specific values; instead they are driven to produce the optimal stochastic policy. If the optimal policy is deterministic, then the preferences of the optimal actions will be driven infinitely higher than all suboptimal actions (if permited by the parameterization).

--- 

estimating mutual information
https://math.stackexchange.com/questions/2390664/algorithm-for-calculating-the-mutual-information-between-continuous-variables 

---

[@parushDopaminergicBalanceReward2011]

> we present a behavioral policy that seeks the optimal tradeoff between maximization of cumulative expected reward and minimization of cost. Here we use policy complexity as the representative of a cost. We assume that agents pay a price for a more complicated behavioral policy, and therefore try to minimize the complexity of their behavioral policy.

> The complexity of the state representation required by a policy reflects the complexity of the policy. Therefore we define policy complexity as the length of the state representation required by that policy. We can estimate the length of the representation of the state identity required by a policy by observing the length of the state that can be extracted on average given the chosen actions. This definition therefore classifies policies that require detailed rep- resentations of the state as complex. On the other hand, a policy that does not commit to a specific pair of actions and states, and therefore does not require a lengthy state representation, has low complexity. Formally, we can therefore define the state–action mutual information – MI(S; A)

mutual information is the information gained by dependence between r.v.'s: 

MI(X;Y)=Dkl(p(x,y)||p(x)p(y))

> The policy complexity is a measure of the policy commitment to the future action given the state 

how particular a state is to an action (is this only in the markov case?)

> the probability of choosing an action given a specific state p(a|s) is exponentially dependent on the state–action Q-value multiplied by the prior probability of choosing the specific action independently of the state – p(a). This prior probability gives the advantage to actions that are chosen more often, and for this rea- son was dubbed the “experience-modulated softmax policy”

can we connect this softmax to the softmax induced in linearRL, and understand it in an information theoretic / policy compression sense? (if the default policy is or isn't uniformly random)

> In cases where the a-priori probability of all actions is equal, the experience- modulated softmax policy is equivalent to the classical softmax policy.

the classical softmax here is just a softmax where value is taken to be the "preference" as S&B call it. This formula is this the "experience weighted" softmax

> We suggest that dopamine serves as the inverse of β; i.e., as the pseudo-temperature, or the tradeoff parameter between policy complexity and expected reward.

--- 

what is reduction in thermodynamic entropy?

--- 

KL control is a cost on the information added by a new policy? 
what is the KL mean in KL control? 
how is it different from the free-energy version?

three things:
- KL control (exponentiated value function, passive dynamics)
- Ortega free energy (free energy functional of utility and KL between prior and posterior, solved with Blahut-Arimoto thing)
- Tishby/Sims/gershman RDT policy compression (same as above, but simplified and different notation?)

how are these related, how are they different?

what we want:
	continuous action space (difficult)
	adaptation vs. skill learning look different
	behavior changes over learning


--- 

adrian
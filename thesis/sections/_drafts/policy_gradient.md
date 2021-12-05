## LQR Policy Gradients

Global Convergence of Policy Gradient Methods for the Linear Quadratic Regulator (Fazel, 2018)

- Model-based learning by learning the dynamics of the plant, then plan using this model.
	- Subspace System ID (Ljung 1999)
	- Coarse model (Dean, Recht 2017)
	- Plant needs to be controllable, the base policy needs to be stable
- Model-free approaches
	- Estimate (V) values or state-action (Q) values through Monte Carlo + dynamic programming
	- Directly optimize parameterized policy with simulation (policy gradient)


On the Theory of Policy Gradient Methods: Optimality, Approximation, and Distribution Shift (Agarwal 2020)

Structured Policy Iteration for Linear Quadratic Regulator (Park, 2020)

## Policy Gradient

> The Reward Hypothesis: That all of what we mean by goals and purposes can be well thought of as the maximization of the expected value of the cumulative sum of a received scalar signal (called reward).

As an RL practitioner and researcher, one’s job is to find the right set of rewards for a given problem known as reward shaping.

> Reinforcement Learning Objective: Maximize the “expected” reward following a parametrized policy.

$$
\begin{align*}
J(\theta) &= \mathbb{E}_{\tau \sim p_\theta(\tau)}\sum_t^H{r(s_t,a_t)} \\
& \approx \frac{1}{N}\sum^{N paths}_n\sum_t^H{r(s^{(n)}_t,a^{(n)}_t)}
\end{align*}
$$

This is the policy gradient objective, the future expected return in an episode of time steps $H$. The factor $a$ is a discount, $\gamma^k$ or $1/H$ for discounted and average reward objectives, respectively. This is the expectation over the roll-outs / trajectories governed by the current policy. Thus it is "on-policy".



The general (episodic) gradient update

$$
\begin{align*}
\theta_{h+1} = \theta_h + \alpha_h\nabla_\theta J(\theta=\theta_h)
\end{align*}
$$

The policy parameter gradient update step:

$$
\begin{align*}
\theta_{t+1} = \theta_t + \alpha\hat{Q}(s,a)\nabla_\theta\log{\pi_\theta}(s|a)
\end{align*}
$$

We don't know the $Q$-value weighting, but we can approximate it with $\hat{Q}$. Subtracting V(s) from Q(s, a), we get the advantage function A(s, a) which removes common value between actions. This is a specific form of the baseline in REINFORCE. The log-derivative is due to

$$
\begin{align*}
\theta_{t+1} &= \theta_t + \alpha\hat{A}(s,a)\nabla_\theta\log{\pi_\theta}(s|a) \\
&= \theta_t + \alpha\hat{A}(s,a)\frac{\nabla\pi_\theta(s|a)}{\pi_\theta(a|s)}
\end{align*}
$$



### Problems with Policy Gradient

- by definition on-policy (need to forget data very fast in order to avoid the introduction of a bias to the gradient estimator); not sample efficient
- only converge to a local maximum of which there may be many
- requires considerable knowledge about the system one wants to control to make reasonable policy definitions
- always requires a free learning rate parameter


## Sources



bayesian methods, gaussian processes in place of sampling to find distributions:
Bayesian Policy Gradient Algorithms (Ghavamzadeh 2020)

blog on RL:
https://medium.com/@jonathan_hui/rl-model-based-reinforcement-learning-3c2b6f0aa323

Jan Peters (2010), Scholarpedia, 5(11):3698.


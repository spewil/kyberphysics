## Internal Model Adaptation for Linear Quadratic Control

<!-- > Implicit adaptation seems to be driven by 436 sensory prediction error (Leow et al., 2018; Mazzoni & Krakauer, 2006; Taylor et al., 2014), which itself implies a sensory prediction which, presumably, arises as the output of a forward model. Therefore, even though changes to the forward model do not directly influence action selection, they may influence the way  in  which  the  policy  is  updated.  This  ***interdependence  between forward model learning and policy learning could lead to interesting  interactions***.  For  instance,  if  updates  to  the  controller  are  driven  by  sensory-prediction error, at some point sensory prediction error would reach zero, at which point there would no longer be any error signal to drive to changes in the controller. [@hadjiosifDidWeGet2020] -->

<!-- these might have different errors? -->
<!-- model mismatch -> riccatii K -->
<!-- gradient for K -> subomptimal K  -->
<!--  -->

In experiments within the setup described in {+@sec:experiment}, subjects are faced with a novel muscle-to-environment mapping that they must ostensibly learn in order to achieve their goals. Here I investigate the effects of approximating dynamics models within the LQR framework. This short experiment is a first step in modeling how subjects may use endpoint error in each trial to update or adjust their internal approximations of the environment's dynamics.

Our state space is denoted $x$ and our control space $u$ where $dim(x) < dim(u)$. Each trial, we move from state $x_0$ to x(N) in $N$ timesteps. Each trial, we have a goal state $x^*$ and a resulting endpoint error $e_N = |x_N - x^*|^2$. We follow the same LQR setup as defined in the previous section. We can write the controlled, closed-loop system dynamics for the final time step $N$:

$$
\begin{aligned}
x_N &= (A - BL)x_{N-1} = Cx_{N-1} \\
x_N &= Cx_{N-1} = C(Cx_{N-2}) \\
x_N &= C^Nx_0.
\end{aligned}
$$

where $C^N$ might be called the trajectory dynamic. If the trajectory dynamic $C^N$ is an approximation to the true trajectory dynamic $C^{N*}$, we can use the error of a given trajectory to find an incremental update. The error at the final time step $N$ for trial $r$ is

$$
e(r) = |C^N(r)x_{0} - x^*|^2.
$$

This error may be due to several sources. Our internal dynamics model $A$ might have error relative to the true dynamic $A^*$. Our control gain $L$ may be optimal relative to our internal model $A$ but not with respect to the true dynamic $A^*$. Finally, we might have an approximate model $A$ and a suboptimal control gain $L$. Note that since this is still deterministic system, we have yet to include any source of variability in state or control.

If we assume that our computation of the control gain $L$ is optimal for our approximate internal model $A$ (we can compute a controller given only our internal representation of the system dynamic being controlled), we can use our endpoint error to derive a gradient descent update for $A$ on trial $r$:

$$
A(r+1) = A(r) - \eta\frac{\partial{e(r)}}{\partial{A}}
$$

We might think about this as an internal simulation of trial $r$'s trajectory, and a subsequent post hoc evaluation of the movement. To compute $\delta$, we must take the gradient with respect to A of the error:

$$
\begin{aligned}
\frac{\partial{e(r)}}{\partial{A}} &= \frac{\partial{}}{\partial{A}}{|C^N(r)x_0 - x^*|^2}
\end{aligned}
$$

Since the gradient with respect to A is the same as the gradient with respect to $C$, we can compute the gradient with respect to C to find: 

$$
% 2∑𝑁𝑘=1(𝑀𝑁𝑣−𝑤)𝑇𝑀𝑘−1𝑀𝑁−𝑘𝑣
\frac{\partial{e}}{\partial{A_{ij}}} = 2\sum_{k=1}^N\left[(C^Nx_0 - x^*)^TC^{k-1}\right]_i\left[C^{N-k}x_0\right]_j
$$

{+@fig:gradient_descent} shows the LQR simulations across gradient descent updates to the $A$ matrix after it is corrupted by Gaussian noise. Each trajectory is a single run of the LQR controlled for 200 time steps. The star shows the target state, the colored circles show the endpoints of the trajectories. The red circle is the initial state. The descent is converging in endpoint error in position, velocity, and force dimensions of the state vector. Unfortunately, this optimization alters the dynamics incompatibly. The routine is also very fragile to parameter changes. This experiment highlights the difference in loss landscapes between the optimal control problem and the gradient descent simulated here. There are many directions for this work to proceed as discussed in {+@sec:next_steps}.

![Iterations of gradient descent on the $A$ matrix of an infinite-horizon LQR where the original A is corrupted with Gaussian noise. Each dotted line is a sampled trajectory using a recomputed control gain with an updated $A$ matrix. Red circles denote the initial state, the star denotes the goal state, and the colored circles denote the endpoints of each trajectory sampled at each iteration. Note that the initial solution diffuses directly towards the target, and the gradient updates for the dynamics model $A$ alter this trajectory in a nontrivial way. As discussed in the main text, the gradient descent is optimizing for a different cost than the controller optimization, and thus this divergence might be expected.](images/simulations/gradient_descent.pdf){width=75% #fig:gradient_descent}

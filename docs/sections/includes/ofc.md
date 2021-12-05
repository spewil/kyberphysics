## Optimal Feedback Control

The optimal feedback control framework remains the strongest normative model of human movement control. The first step of our theoretical work is to build from the simplest optimal feedback control models, working towards constructing our own variants of such models in order to capture aspects of our experimental findings. The first model we will investigate is the fully-observable, discrete-time, infinite-horizon linear quadratic regulator (LQR) problem with additive Gaussian noise. Given a state $x\in{\mathbb{R}^n}$ and an control input $u\in{\mathbb{R}^m}$, the state evolves in discrete time according linear dynamics

$$
x_{t+1} = Ax_t + Bu_t + w_t
$$

where $w_t\sim\mathcal{N}(0,\mathbb{I})$ The LQR problem is to find a sequence of controls $u_t$ which minimize a cost $J$

$$
J = \mathbb{E}\sum_{t=0}^{\infty}{x_t^TQx_t + u_t^TRu_t}
$$

according to some chosen state and control cost parameters $Q$ and $R$. The optimal cost-to-go or state value function for the problem is

$$
V_t(x) = \min_{u}\left[{x_t^TQx_t + u_t^TRu_t + V_{t+1}(Ax+Bu)}\right].
$$


The optimal control law $L$ which solves this problem is linear function in the state

$$
u_t^*(x) = -Lx.
$$	 

This control law is found through iterating a Riccati equation involving $A$, $B$, $Q$, and $R$ to find the optimal $V$ which is a quadratic function in state. There is a functional relationship between $V$ and $L$ that can be derived algebraically. {+@fig:control_field} shows simulated trajectories of the infinite-horizon problem from random initial positions. The vector field depicts the two-dimensional control vector. In this example, the model describes a second-order point mass dynamical system where the control input acts as a force on the particle. The state vector $x$ contains two dimensions each of position, velocity, and force of the particle, each updated via Euler integration. {+@fig:cost_field} shows the same simulated trajectories of the point mass atop the quadratic value function. The goal state in these simulations is (0.5,0.5). Note that there are many free dynamics parameters in such simulations within $A$ and $B$ which drastically alter the resulting simulations. The values here were chosen to match the motor control literature.

![Simulation of trajectories from uniform random initial positions for the simplest LQR controller. The diffusions are controlled such that their inputs are proportional to the positional error. The plain LQR controller is invariant (up to a translation) to the goal state, as explained in the text. Here the goal state is (0.5,0.5) denoted by a white star. red circles denote the initial position of the trajectory and green circles denote the endpoint after 200 increments. Arrows show the state-dependent control signal (force) vector $u^T = [f_x,f_y]$.](images/simulations/control_field.pdf){width=70% #fig:control_field}

![The same trajectory simulations as in {+@fig:control_field} atop the quadratic cost field.](images/simulations/cost_field.pdf){width=70% #fig:cost_field}

Assuming that the original system is controllable and stabilizable, the linear optimal control problem is a matter of trading off eigenvalues of the closed loop system which drive the steady-state error of the system to 0 under the control cost. This system can be made to drive to a given target $x^*$ by feeding back evolving the dynamics in terms of target error $|x-x^*|$ or by augmenting the state vector with terms which compute this error implicitly. These yield identical solutions for the control law, the latter typically being more convenient. The implication of this is that only one control law is required for the problem with a point target in the state space. If the problem were to model human movement, it might be said that we only require the internalization of a single control law up to a translation in the target's desired state. Only the error is required in this simple case. As discussed in {+@sec:next_steps}, variants of this basic model are more interesting in that they do not display this target invariance.

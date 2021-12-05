## Fluctuation Dissipation Relation Background

OU == Langevin

https://math.stackexchange.com/questions/2292050/how-is-the-ornstein-uhlenbeck-process-stationary-if-the-mean-and-variance-are-ti

~

FDR

If nothing has been said about requiring that <f(a, t)> must approach an equilibrium distribution at long times, then:
	If there is not enough friction to dampen the heating effect of the noise, we expect that the system will "run away" so that there is no long time steady state. If there is too much friction for the noise, the system will cool down and "die." In fact, not much is known in general about the long time steady state solution of an arbitrary Fokker-Planck equation. All that we can usually do is guess at a steady state solution, put it into the equation, and see if our guess is compatible with v(a) and B. If a steady-state solution is found, then it implies a relation between v(a) and B which may be called a fluctuation-dissipation theorem. (Zwanzig)

assumptions of FD:
	- autocorrelation approaches an equilibrium value at long time (<v(t)^2>)
	- friction will balance noise in the long time limit

time average, ensemble average ?

what does delta time-correlation imply?

fluctuation-dissipation happens when we take the long time limit and show a relationship between the noise "power" and the equilibrium value of the dynamics -- in case of a "tuned" noise problem, what is our long-time limit? is it the evolution of the system representing..... one trial? evolution over trials? this feels too specific...

if my dynamics is defined over one trajectory... i can look at each trial as an infinitely long (discounted) trajectory and derive a fluctuation-dissipation theorem per trial. then my gradient movement will be in terms of parameters for a single trial

i have been thinking about it like a distribution over trajectories, not a single distribution for a single trajectory... almost the same thing? a distribution from which you can sample a trajectory vs. a distribution governing the probability of a single trajectory? how is this different?


~

[Friction and Fluctuations](https://web.stanford.edu/~peastman/statmech/friction.html)

Friction is such a universal part of our experience, it seems like it must reflect something fundamental in the laws of nature. Yet if you look at the basic equations of classical or quantum mechanics, there is no sign of friction. A single isolated particle will continue forever moving in a straight line without slowing down. If two particles collide, they bounce away from each other with just as much energy as they started with. Friction, it appears, only happens to macroscopic objects.

When a system is in equilibrium, its kinetic energy is uniformly distributed among all its degrees of freedom. A macroscopic object in motion clearly is not in equilibrium. It has one degree of freedom (the center of mass motion) with far more energy than any other. If that degree of freedom interacts with others, the system will tend to move toward equilibrium. Energy will be transfered out of that one degree of freedom (so the object will slow down) and into all the others (so the object will become warmer). That is all friction really is: the tendency of systems to move toward equilibrium when different degrees of freedom are allowed to interact with each other.

A system experiencing friction is, by definition, a system out of equilibrium.

Friction is caused by the interaction with a heat bath. Let us be very clear about that. A moving object slows down because it is colliding with molecules in its environment. In the process, energy is dissipated: the object’s kinetic energy is redistributed among a huge number of microscopic degrees of freedom.

Suppose a pollen grain is initially not moving at all. In that case, collisions with water molecules will cause it to start moving. So in equilibrium, the pollen grain will be in constant motion. Its speed and direction of motion will be constantly changing, as it is jostled by the surrounding water molecules. But on average, its kinetic energy will equal the value given by the equipartition theorem.

We refer to this effect as **equilibrium fluctuations**. These two effects, fluctuations and dissipation, are inseparable from each other. They are both caused by exactly the same mechanism: the interaction of the variable with a heat bath.


~

Time and Ensemble Averages

The degrees of freedom making up the system are constantly changing. At one instant the atoms have particular positions and momenta, but the next instant they are different. We therefore define the probability of the system being in a microstate as the fraction of time it spends in that state. Averages computed using this definition of probability are called **time averages**.

Instead of looking at just one system, imagine preparing many identical systems by following the exact same procedure many times. All of these systems are in the same macrostate, but each one is in a different microstate. You have to simply imagine doing this, because in practice you have only one system in one microstate—but you do not know which one it is. We define the probability of the system being in a microstate as the fraction of these imaginary systems that are in that state. The set of all the systems is called a statistical ensemble, and averages computed with this definition of probability are called **ensemble averages**.

__Definition__
A system for which time averages and ensemble averages are equal is said to be ergodic.

__Definition__
An isolated system is in equilibrium if the probability distribution of its microstates does not change with time.

~

Langevin Equation

Essentially, there is one term that removes energy and one term that adds energy. When the system is in equilibrium, the two terms will exactly balance out so the average energy remains constant. The magnitude of the random force will of course depend on temperature: the hotter the system, the faster the water molecules will be moving, and the harder they will hit the particle. We therefore expect there should be some relationship between the temperature, the friction coefficient, and the magnitude of the random force.

x_dot = -(friction_coefficient)(x) + noise

~

Evolution of Densities

When I speak of probabilities here, I mean them in the sense of ensemble averages. Imagine preparing a huge number of systems that are all macroscopically indistinguishable from each other. The “probability” of a microstate means the fraction of those systems that are in that particular microstate. I am not assuming anything about what that probability distribution is, though. In particular, it need not correspond to equilibrium. As all the systems evolve with time, following the laws of classical mechanics, the probability density will also evolve.

Consider an ensemble of identical harmonic oscillators moving with different amplitudes and phases. Together, they define a probability density in phase space (x,p). Each one traces out an ellipse as it moves. The frequency of a harmonic oscillator is independent of its amplitude, so all of them take exactly the same amount of time to trace out one full rotation. Therefore the entire probability distribution simply rotates in phase space, returning to its starting point after one full period of oscillation.
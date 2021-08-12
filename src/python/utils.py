import numpy as np


def advance_dynamics(A, state, B, control):
    return np.dot(A, state) + np.dot(B, control)


def test_dynamics():
    # timesteps = 100
    # states = np.zeros((6, timesteps))
    # state = np.zeros((6, 1))
    # controls = np.zeros((32, timesteps))
    # controls[7, :] = np.hstack(
    #     [np.ones(timesteps // 4) * .1,
    #      np.zeros(3 * timesteps // 4)])

    # for i in range(timesteps):
    #     states[:, i] = state[:, 0]
    #     state = advance_dynamics(dynamics, state, decoder,
    #                              controls[:, i].reshape(-1, 1))
    pass

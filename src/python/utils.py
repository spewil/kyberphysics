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

def roots_of_unity(num_points, radius=1, offset=0):
    # offset in radians
    c = 2j * np.pi / num_points
    points = [
    [np.around(x.imag, decimals=2),
    np.around(x.real, decimals=2)] for x in
    [radius * np.exp((k * c) + 1j * offset) for k in range(num_points)]
    ]
    return np.array(points)

def write_array_to_disk(a, name):
    with open(name, "wb") as file:
        file.write(a.tobytes())

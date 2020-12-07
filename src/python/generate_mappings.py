import numpy as np
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt


def roots_of_unity(num_points, radius=1, offset=0):
    # offset in radians
    c = 2j * np.pi / num_points
    return [
        [np.around(x.imag, decimals=2),
         np.around(x.real, decimals=2)] for x in
        [radius * np.exp((k * c) + 1j * offset) for k in range(num_points)]
    ]


# channel_to_visualize = 12
# state_dim_to_place_channel = 1
# decoder = np.zeros(shape=(state_dimensionality, numchannels),dtype=np.float32)
# decoder[state_dim_to_place_channel,channel_to_visualize] = 1


def write_dynamics_to_disk(dynamics, decoder):
    with open("dynamics.bin", "wb") as file:
        file.write(dynamics.tobytes())

    with open("decoder.bin", "wb") as file:
        file.write(decoder.tobytes())


def generate_dynamics(num_channels=32,
                      scale_factor=0.25,
                      tau=0.1,
                      state_dimensionality=6):
    dynamics = np.eye(state_dimensionality, dtype=np.float32) * scale_factor
    dynamics[0, 2] = tau
    dynamics[1, 3] = tau
    dynamics[2, -2] = tau
    dynamics[3, -1] = tau
    dynamics[-1, -1] = 0
    dynamics[-2, -2] = 0
    decoder = np.zeros(shape=(state_dimensionality, num_channels),
                       dtype=np.float32)
    return dynamics, decoder


def generate_test_dynamics(num_channels=32,
                           channel_to_visualize=12,
                           state_dim_to_place_channel=0,
                           scale_factor=0,
                           state_dimensionality=6):
    dynamics = np.eye(state_dimensionality, dtype=np.float32) * scale_factor
    decoder = np.zeros(shape=(state_dimensionality, num_channels),
                       dtype=np.float32)
    decoder[state_dim_to_place_channel, channel_to_visualize] = 1
    return dynamics, decoder


def advance_dynamics(A, state, B, control):
    return np.dot(A, state) + np.dot(B, control)


if __name__ == '__main__':

    roots = np.array(roots_of_unity(32)).T
    dynamics, decoder = generate_dynamics(32, 0.6)
    decoder[-2:, :] = roots

    # print(roots @ np.ones((32, 1)))
    for r in roots.T:
        plt.plot(r[0], r[1], 'ko')

    timesteps = 100
    states = np.zeros((6, timesteps))
    state = np.zeros((6, 1))
    controls = np.zeros((32, timesteps))
    controls[7, :] = np.hstack(
        [np.ones(timesteps // 4) * .1,
         np.zeros(3 * timesteps // 4)])

    plt.figure()
    for c in controls:
        plt.plot(c)

    for i in range(timesteps):
        states[:, i] = state[:, 0]
        state = advance_dynamics(dynamics, state, decoder,
                                 controls[:, i].reshape(-1, 1))

    plt.figure()
    plt.plot(states[0, :], 'o', label="posx")
    plt.plot(states[1, :], 'o', label="posy")
    plt.plot(states[2, :], 'o', label="velx")
    plt.plot(states[3, :], 'o', label="vely")
    plt.legend()
    plt.show()

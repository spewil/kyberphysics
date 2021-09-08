import sys
import numpy as np
from utils import files, utils


def generate_dynamics_and_mapping(num_channels=32,
                                  state_dimensionality=6,
                                  mapping_type="circle",
                                  passive_dynamics_off=True,
                                  num_directions=8,
                                  **kwargs):
    decoder = np.zeros(shape=(state_dimensionality, num_channels),
                       dtype=np.float32)
    if mapping_type == "direct":
        decoder[0, kwargs["channel_1"]] = 1
        decoder[1, kwargs["channel_2"]] = 1

    elif mapping_type == "column":
        # number of directions == number of electrode columns
        roots = utils.roots_of_unity(num_directions).T
        roots_x = roots[0, :]
        roots_y = roots[1, :]
        # tile directions down the arm / rows -- into electrode configuration
        roots_xt = np.tile(roots_x, (num_channels // num_directions, 1))
        roots_yt = np.tile(roots_y, (num_channels // num_directions, 1))
        # print(roots_xt)
        roots_x_unrolled = np.hstack(roots_xt)
        roots_y_unrolled = np.hstack(roots_yt)
        roots = np.stack([roots_x_unrolled, roots_y_unrolled])
        # print(roots)
        decoder[-2:, :] = roots

    elif mapping_type == "circle":
        roots = utils.roots_of_unity(num_channels)
        roots_x = roots[:, 0]
        roots_y = roots[:, 1]
        # arrange into electrode configuration
        roots_x_arranged = np.hstack(roots_x.reshape(8, 4).T)
        roots_y_arranged = np.hstack(roots_y.reshape(8, 4).T)
        # collapse into electrode order
        roots = np.stack([roots_x_arranged, roots_y_arranged])
        decoder[-2:, :] = roots

    elif mapping_type == "identity":
        decoder[-2, 0] = 1
        decoder[-1, 1] = 1

    if passive_dynamics_off:
        dynamics = np.zeros((6, 6), dtype=np.float32)

    else:
        dynamics = np.eye(state_dimensionality,
                          dtype=np.float32) * kwargs["scale_factor"]
        dynamics[0, 2] = kwargs["tau"]
        dynamics[1, 3] = kwargs["tau"]
        dynamics[2, -2] = kwargs["tau"]
        dynamics[3, -1] = kwargs["tau"]
        dynamics[-1, -1] = 0
        dynamics[-2, -2] = 0

    if kwargs["save"] == True:
        files.write_array_to_disk(dynamics, kwargs["dynamics_filename"])
        files.write_array_to_disk(decoder, kwargs["decoder_filename"])

    return dynamics, decoder


def generate_identity_decoder(num_channels, state_dimensionality=6):
    decoder = np.zeros(shape=(state_dimensionality, num_channels),
                       dtype=np.float32)
    # decoder[-2, 24] = 1  # right
    decoder[-1, 57] = 1  # up
    # decoder[-2, 5] = -1  # left
    # decoder[-1, 33] = -1  # down
    return decoder


def generate_null_dynamics(state_dimenstionality=6):
    return np.zeros((state_dimenstionality, state_dimenstionality),
                    dtype=np.float32)


def generate_decoder(experiment, subject):
    # pick up experiment / session metadata
    # grab data from subject folder
    # run dim reduction on this data
    # save some plots
    # have the option here to redo the calibration?
    # construct decoder matrix
    # save matrix in the subject folder
    pass


def generate_dynamics(decay=0.9, tau=0.5):
    dynamics = np.eye(6, dtype=np.float32) * decay
    dynamics[0, 2] = tau
    dynamics[1, 3] = tau
    dynamics[2, -2] = tau
    dynamics[3, -1] = tau
    dynamics[-1, -1] = 0
    dynamics[-2, -2] = 0
    return dynamics


if __name__ == '__main__':

    # MAKE DECODER
    dynamics = generate_null_dynamics()
    decoder = generate_identity_decoder(64)

    subject_folder = utils.get_subject_folder("self_test", "spencer")

    # print(dynamics.shape)
    # print(dynamics)

    print(decoder.shape)
    # print(decoder)

    # # SAVE DECODER
    utils.write_array_to_disk(dynamics, subject_folder / "dynamics.bin")

    # _, decoder = generate_dynamics_and_mapping(num_channels=64,mapping_type="column", save=False)

    utils.write_array_to_disk(decoder, subject_folder / "decoder.bin")

    # PCA

    # compute_PCA_components("self_test_9_2_21", "spencer")

    # how the electrodes are spatially arranged
    # electrode_layout = np.arange(32).reshape(4, 8)
    # print(electrode_layout)
    # how to invert this
    # print(np.hstack(electrode_layout))
    # #                 ELBOW
    # #  FIXED                             FREE
    # #
    # #        [[ 0  1  2  3  4  5  6  7]
    # #         [ 8  9 10 11 12 13 14 15]
    # #         [16 17 18 19 20 21 22 23]
    # #         [24 25 26 27 28 29 30 31]]
    # #
    # #                 WRIST
    # if we put our mapped weights into this shape,
    # we want to "unroll" them into numerical order

    # how we want the order of directions to go
    # circle_order = np.arange(32).reshape(8, 4).T
    # print(circle_order)
    # do the same inversion
    # print(np.hstack(circle_order))

    # fig, ax = plt.subplots()  # note we must use plt.subplots, not plt.subplot
    # plt.axis("off")
    # ax.set_ylim([-1, 1])
    # ax.set_xlim([-1, 1])
    # positions = utils.roots_of_unity(32)
    # for x, y, p in zip(decoder[-2, :], decoder[-1, :], positions):
    #     ax.arrow(p[0], p[1], x * 0.1, y * 0.1)
    # plt.axis("square")
    # plt.axis("off")

    # weightsx = decoder[-2, :].reshape(4, 8)
    # weightsy = decoder[-1, :].reshape(4, 8)

    # y = np.linspace(0, 1, 4)[::-1]
    # x = np.linspace(0, 1, 8)

    # fig, ax = plt.subplots()  # note we must use plt.subplots, not plt.subplot
    # plt.axis("off")
    # ax.set_ylim([-0.1, 1.1])
    # ax.set_xlim([-0.1, 1.1])
    # for i in range(4):
    #     for j in range(8):
    #         plt.arrow(x[j], y[i], weightsx[i, j] * 0.1, weightsy[i, j] * 0.1)
    # plt.show()

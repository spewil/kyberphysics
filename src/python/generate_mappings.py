import numpy as np
# import matplotlib
# import sys
# if sys.platform == "darwin":
#     matplotlib.use("Qt4Agg")
#     print("on mac")
# else: 
#     print("on windows")
import matplotlib.pyplot as plt
import utils


def generate_dynamics_and_mapping(num_channels=32,
                      state_dimensionality=6,
                      mapping_type="circle",
                      passive_dynamics_off=True,
                      **kwargs):
    decoder = np.zeros(shape=(state_dimensionality, num_channels),
                   dtype=np.float32)
    if mapping_type == "direct":
        decoder[0,kwargs["channel_1"]] = 1
        decoder[1, kwargs["channel_2"]] = 1

    elif mapping_type == "circle":
        roots = utils.roots_of_unity(num_channels).T
        decoder[-2:, :] = roots

    if passive_dynamics_off:
        dynamics = np.zeros((6,6),dtype=np.float32)

    else:
        dynamics = np.eye(state_dimensionality, dtype=np.float32) * kwargs["scale_factor"]
        dynamics[0, 2] = kwargs["tau"]
        dynamics[1, 3] = kwargs["tau"]
        dynamics[2, -2] = kwargs["tau"]
        dynamics[3, -1] = kwargs["tau"]
        dynamics[-1, -1] = 0
        dynamics[-2, -2] = 0

    return dynamics, decoder


# if __name__ == '__main__':

# roots of unity mapping, no dynamics
dynamics, decoder = generate_dynamics_and_mapping()

# dynamics, decoder = generate_dynamics_and_mapping(passive_dynamics_off=False,scale_factor=0.9, tau=0.1)
# dynamics, decoder = generate_dynamics_and_mapping(mapping_type="direct",channel_1=20, channel_2=8)

print(dynamics)
print(decoder)

directions = [(decoder[-2,i],decoder[-1,i]) for i in range(32)]
print(directions)

electrode_layout = np.arange(32).reshape(4,8)
print(electrode_layout)
# ELBOW
            # [[ 0  1  2  3  4  5  6  7]  
# FIXED END    [ 8  9 10 11 12 13 14 15] FREE END  
            #  [16 17 18 19 20 21 22 23]
            #  [24 25 26 27 28 29 30 31]]
# WRIST
electrodes_in_directional_order = np.hstack(electrode_layout.T)
print(electrodes_in_directional_order)

# plot arrows of unity root direction for each direction
x = np.linspace(0,1,4)
y = np.linspace(0,1,8)
print(x,y)
fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
for i in range(5):
    for j in range(8):
        plt.circle()
        circle = plt.Circle((x[i], y[j]), electrode_layout[i,j], color='k')
        ax.add_artist(circle)

plt.savefig(fig, 'plotcircles.png')
# for channel_idx, direction in zip(electrodes_in_directional_order, directions):
#     plt.arrow()

utils.write_array_to_disk(dynamics, "dynamics.bin")
utils.write_array_to_disk(decoder, "decoder.bin")

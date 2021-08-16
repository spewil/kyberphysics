import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os
matplotlib.use('agg')

prefix = "/mnt/c/Users/spencer/data/experiment_1/spencer_wilson/session_2/"
suffix = ".bin"

# filename = "calibration2020-11-19T19_19_07"

filename = "59_2021_08_16_16_09"
fname = prefix+filename+suffix

data = np.fromfile(fname,dtype=np.int32)
numchannels = 64
data = data.reshape(-1,numchannels+4).T
print(data.shape)

filename = "59_V_2021_08_16_16_09"
fname = prefix+filename+suffix

data = np.fromfile(fname,dtype=np.float32)
numchannels = 64
data = data.reshape(-1,numchannels).T
print(data.shape)


# fig, ax = plt.subplots(1,1,figsize=(10,10))
# for i in range(numchannels):
# 	ax.plot(data[i,:],alpha=0.5)
# fig.savefig("data.png")

# fig, ax = plt.subplots(1,1,figsize=(10,10))
# ax.plot(data[-1,:],'k')

# fig.savefig("counter.png")
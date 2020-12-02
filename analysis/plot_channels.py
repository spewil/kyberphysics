import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os
import pathlib
matplotlib.use('agg')

prefix = "/mnt/c/Users/spencer/Documents/kyberphysics/data/"
suffix = ".bin"

# folder = "calibration/"
# filename = "calibration2020-11-19T19_19_07"

folder = "testing/spencer_64channel_nolights_nomonitor/"
path = prefix+folder

filename = "2020-11-30T16_51_29"

fname = prefix+folder+filename+suffix

data = np.fromfile(fname,dtype=np.int32)

numchannels = 8
num_channels_to_plot = 8
data = data.reshape(-1,numchannels+4).T
print(data.shape)
print(data[-1,:5])

for i in range(num_channels_to_plot):
	fig, ax = plt.subplots(1,1,figsize=(10,10))
	ax.plot(data[i,-200:],alpha=0.5)
	fig.savefig("data"+str(i)+".png")

fig, ax = plt.subplots(1,1,figsize=(10,10))
ax.plot(data[-1,:],'k')
fig.savefig("counter.png")
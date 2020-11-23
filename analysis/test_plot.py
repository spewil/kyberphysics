import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os
matplotlib.use('agg')

prefix = "/mnt/c/Users/spencer/Documents/kyberphysics/data/"
suffix = ".bin"

# folder = "calibration/"
# filename = "calibration2020-11-19T19_19_07"

folder = "testing/unplugged/"
filename = "2020-11-23T14_18_59"

fname = prefix+folder+filename+suffix

data = np.fromfile(fname,dtype=np.int32)

numchannels = 8
data = data.reshape(-1,numchannels+4).T
print(data.shape)
print(data[-1,:5])

fig, ax = plt.subplots(1,1,figsize=(10,10))
for i in range(numchannels):
	ax.plot(data[i,:],alpha=0.5)
fig.savefig("data.png")

fig, ax = plt.subplots(1,1,figsize=(10,10))
ax.plot(data[-1,:],'k')
fig.savefig("counter.png")
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os
matplotlib.use('agg')

fname = r"/mnt/c/Users/spencer/Documents/kyberphysics/data/Testing/test642020-11-13T16_05_41.bin"
fname2 = r"/mnt/c/Users/spencer/Documents/kyberphysics/data/Testing/test642020-11-13T16_05_45.bin"
# metadata = os.path.splitext(fname)[0] + '.csv'
# data = np.fromfile(fname, dtype=np.float32)

data = np.fromfile(fname,dtype=np.int32)
data2 = np.fromfile(fname2,dtype=np.int32)

# trials = np.genfromtxt(metadata)
# data = data.reshape((len(trials),-1,68))
# stack = np.vstack([data[0,:,i] + i * 15 for i,c in enumerate(range(64))])
numchannels = 64
data = data.reshape(-1,numchannels+4).T
print(data.shape)
print(data[-1:,:5])

data2 = data2.reshape(-1,68).T
print(data2.shape)
print(data2[-1:,-5:])

fig, ax = plt.subplots(1,1,figsize=(10,10))
for i in range(numchannels):
	ax.plot(data[i,:4000],alpha=0.5)
fig.savefig("data.png")

fig, ax = plt.subplots(1,1,figsize=(10,10))
ax.plot(data[-1,:5],'k')
fig.savefig("counter.png")

fig, ax = plt.subplots(1,1,figsize=(10,10))
ax.plot(data[-1,:4000],'k')
fig.savefig("counter_rest.png")

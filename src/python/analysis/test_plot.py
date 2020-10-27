import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os
matplotlib.use('agg')

fname = r"/mnt/c/Users/spencer/Documents/kyberphysics/src/workflows/Data/calibration2020-10-22T16_12_02.bin"

#fname = ''
metadata = os.path.splitext(fname)[0] + '.csv'
# data = np.fromfile(fname, dtype=np.float32)
data = np.fromfile(fname,dtype=np.int32)
trials = np.genfromtxt(metadata)
data = data.reshape((len(trials),-1,68))
stack = np.vstack([data[0,:,i] + i * 15 for i,c in enumerate(range(64))])

fig, ax = plt.subplots(1,1,figsize=(10,10))
ax.plot(stack.T)
fig.savefig("test_plot.png")
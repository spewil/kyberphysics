import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os
matplotlib.use('agg')

fname = r"/mnt/c/Users/spencer/Documents/kyberphysics/src/workflows/Data/calibration2020-10-22T16_12_02.bin"

conversion = 0.0002861 # ints to mV

#fname = ''
metadata = os.path.splitext(fname)[0] + '.csv'
# data = np.fromfile(fname, dtype=np.float32)
data = np.fromfile(fname,dtype=np.int32)
trials = np.genfromtxt(metadata)
print(trials)
data = data.reshape((len(trials),-1,68))*conversion

fig, ax = plt.subplots(1,1,figsize=(10,10))

stack = np.vstack([data[0,:,i] + i * 15 for i,c in enumerate(range(64))])
ax.plot(stack.T)

fig.savefig("test_plot.png")
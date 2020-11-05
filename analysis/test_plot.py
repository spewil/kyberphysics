import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os
matplotlib.use('agg')

fname = r"/mnt/c/Users/spencer/Documents/kyberphysics/data/Testing/test2020-11-04T17_49_33.bin"

#fname = ''
metadata = os.path.splitext(fname)[0] + '.csv'
# data = np.fromfile(fname, dtype=np.float32)

data = np.fromfile(fname,dtype=np.int32)
# trials = np.genfromtxt(metadata)
# data = data.reshape((len(trials),-1,68))
# stack = np.vstack([data[0,:,i] + i * 15 for i,c in enumerate(range(64))])
data = data.reshape(20,-1)
print(data.shape)

fig, ax = plt.subplots(1,1,figsize=(10,10))
ax.plot(data[-1,:2000])
fig.savefig("test_plot.png")
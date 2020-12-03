import numpy as np 

numchannels = 32
scale_factor = 0 

dynamics = scale_factor*np.eye(6,dtype=np.float32)

# first two emg channels 
decoder = np.zeros(shape=(numchannels,6),dtype=np.float32)
decoder[0,0] = 1
decoder[1,1] = 1

with open("dynamics.bin","wb") as file:
	file.write(dynamics.tobytes())

with open("decoder.bin","wb") as file:
	file.write(dynamics.tobytes())
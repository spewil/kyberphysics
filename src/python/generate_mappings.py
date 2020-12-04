import numpy as np 

numchannels = 32
scale_factor = 0 

dynamics = scale_factor*np.eye(6,dtype=np.float32)

decoder = np.zeros(shape=(6,numchannels),dtype=np.float32)
decoder[2,0] = 1

with open("dynamics.bin","wb") as file:
	file.write(dynamics.tobytes())

with open("decoder.bin","wb") as file:
	file.write(decoder.tobytes())
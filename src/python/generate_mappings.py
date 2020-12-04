import numpy as np 

numchannels = 32
state_dimensionality = 6
scale_factor = 0 

dynamics = scale_factor*np.eye(state_dimensionality,dtype=np.float32)

channel_to_visualize = 12
state_dim_to_place_channel = 0
decoder = np.zeros(shape=(state_dimensionality,numchannels),dtype=np.float32)
decoder[state_dim_to_place_channel,channel_to_visualize] = 1

with open("dynamics.bin","wb") as file:
	file.write(dynamics.tobytes())

with open("decoder.bin","wb") as file:
	file.write(decoder.tobytes())
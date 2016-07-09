from pylab import *
from scipy.io import wavfile
import numpy as np

sampFreq, snd = wavfile.read('440_sine.wav')

test = np.array([[0,1],[0,1],[0,0]])

print (test)
print (test.dtype)
print (test.shape)
print (test.size)
print (test.itemsize)
print (test.ndim)

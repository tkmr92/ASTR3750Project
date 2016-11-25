import numpy as np
import matplotlib.pyplot as pl

image = np.zeros([500, 500, 4])

def simImpacts(time):
    """"""
    time = int(time/1000)
    x = []
    y = []
    for i in range(time):
        x.append(np.random.rand()*500)
        y.append(np.random.rand()*500)
    return np.array(x), np.array(y)

impactx, impacty = simImpacts(4e6)

for i in range(len(impactx)):
    image[impactx[i]][impacty[i]][0] = 0.5
    image[impactx[i]][impacty[i]][1] = 0.5
    image[impactx[i]][impacty[i]][2] = 0.5
    image[impactx[i]][impacty[i]][3] = 1

pl.imshow(image)
pl.show()
